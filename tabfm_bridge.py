"""TabFM (Google Research) ca regresor pentru semnalul A, prin export -> rulare -> import.

De ce trei pasi si nu un apel direct. TabFM nu potriveste parametri: la `fit` retine blocul de
antrenare ca pe un CONTEXT si il reciteste la fiecare predictie. Doua consecinte platite aici:

  1. incarcarea modelului costa 7-12 secunde, iar bratul A cere 12 potriviri per encoder (doua
     brate EN-only plus zece limbi). Un subproces per potrivire platea incarcarea de 12 ori;
  2. `tabfm[pytorch]` isi trage propriul torch, iar `ml_def` are torch 2.13 cu MPS de care depinde
     tot restul proiectului, deci nu se pot amesteca.

Deci: `finetune_xlmr.py --frozentrial --export-blocks` scrie blocurile o data, `tabfm_runner.py`
(sau notebook-ul de Colab) le citeste si produce predictiile intr-o singura rulare cu un singur
model incarcat, iar `--regressor tabfm-cache` le consuma inapoi si rularea locala merge mai departe
exact ca oricare alta: aceiasi bootstrap, acelasi raport, aceleasi coloane.

Fisierul asta tine PARTEA COMUNA celor doua capete, si e importabil din ambele medii fiindca la
nivel de modul cere numai numpy. Torch si tabfm se importa inauntrul lui `ruleaza`.

Cheia de identitate. Fiecare cerere e identificata prin blake2b peste formele si octetii lui
(Xtr, ytr, Xpredict). Capatul care rulazea TabFM RECONSTRUIESTE cererile din blocuri, deci daca ar
reconstrui fie si un singur rand altfel, cheia n-ar mai corespunde si `tabfm-cache` refuza sa
scrie. Nu e o speranta ca cele doua capete fac acelasi lucru, e o poarta.

Instalare, o singura data (Mac):
    /opt/homebrew/Caskroom/miniforge/base/envs/ml_def/bin/python -m venv ~/.local/share/tabfm-venv
    ~/.local/share/tabfm-venv/bin/pip install "tabfm[pytorch]" safetensors
"""
import contextlib
import hashlib
import json
import os
import time

import numpy as np

# Ordinea de RULARE pune limbile primele si bratele EN-only ultimele. Nu e o preferinta estetica:
# costul creste si cu blocul de PREZIS, nu doar cu contextul, iar `en_only_test` prezice toate cele
# 5624 de randuri de test deodata, deci e cea mai scumpa cerere din toate douasprezece. Si e chiar
# cea de care poarta de frontiera nu are nevoie: ea se calculeaza pe `p_multi`, adica pe cererile
# per limba. Cu ordinea asta, o sesiune care cade dupa cateva ore lasa pe disc exact partea care
# raspunde la intrebare. Ordinea nu atinge identitatea: cheia e continutul cererii, nu pozitia ei.
EN_TEST, EN_TRIAL = "en_only_test", "en_only_trial"


def req_key(Xtr, ytr, Xpredict):
    """Identitatea unei cereri. Aceeasi functie la ambele capete, deci nu poate diverge."""
    h = hashlib.blake2b(digest_size=16)
    for a in (Xtr, ytr, Xpredict):
        a = np.ascontiguousarray(a, dtype=np.float32)
        h.update(np.asarray(a.shape, np.int64).tobytes())
        h.update(a.tobytes())
    return h.hexdigest()


def proba_finita(model, n=256, d=8, seed=0):
    """Cerere sintetica minuscula, rulata O DATA inainte de cele 12 adevarate.

    Exista fiindca esecul de dtype nu se vede la incarcare, ci abia in predictii, si abia dupa
    minutele platite pe prima cerere adevarata. Masurat: in float16, activarile din FFN-ul stivei
    ICL trec de 65504 (varful reziduului e ~4300 la `icl_predictor.tf_icl.blocks.9`, iar `linear2`
    da inf), deci TOATE predictiile ies NaN. Nu e o proprietate a datelor si nu depinde de placa:
    acelasi 0 din 150 finite pe MPS si pe CUDA. In bfloat16 si float32 aceleasi date dau 150/150.

    Verifica si ca iesirea nu e constanta: un model incarcat gresit poate da zerouri finite.
    """
    from tabfm import TabFMRegressor
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d)).astype(np.float32)
    y = (X[:, 0] * 0.5 + X[:, 1] * 0.2 + rng.normal(scale=0.1, size=n)).astype(np.float32)
    reg = TabFMRegressor(model=model, n_estimators=1, max_num_features=d, random_state=42,
                         verbose=False)
    reg.fit(X, y)
    p = np.asarray(reg.predict(X[:32]), dtype=np.float64)
    return bool(np.isfinite(p).all()) and float(np.std(p)) > 1e-6


def cereri(B):
    """Reconstruieste cele 12 cereri din blocuri. Regula e copiata din `frozen_trial_gap`:

        brat EN-only:  reg(Xen_f, yen, Xml)  si  reg(Xen_f, yen, Xt_self)
        limba L:       Xtr = vstack([Xen, Xml[lang != L]]),  ytr = concat([yen, y[lang != L]])
                       Xpred = vstack([Xml[lang == L], Xt_self[langt == L], Xt_test[langt == L]])

    `Xen` si `Xen_f` sunt acelasi bloc cand `--freq-drop` e 0, si exportul refuza altceva.
    """
    Xen, yen, Xml, y, lang = B["Xen_f"], B["yen"], B["Xml"], B["y"], B["lang"].astype(str)
    Xts, Xtt, langt = B["Xt_self"], B["Xt_test"], B["langt"].astype(str)
    out = []
    for L in sorted(np.unique(lang)):
        te, tr, tt = (lang == L), (lang != L), (langt == L)
        out.append((L, np.vstack([Xen, Xml[tr]]), np.concatenate([yen, y[tr]]),
                    np.vstack([Xml[te], Xts[tt], Xtt[tt]])))
    return out + [(EN_TEST, Xen, yen, Xml), (EN_TRIAL, Xen, yen, Xts)]


def parametri_ansamblu():
    """Butoanele de ansamblu, citite din mediu. Aceeasi functie pentru rulare si pentru estimarea
    de cost, ca o estimare sa nu descrie alta configuratie decat cea care se ruleaza.
    """
    def env(nume, implicit=None):
        v = os.environ.get(nume, "").strip()
        return v if v else implicit

    norm = env("TABFM_NORM")
    crosses, svd = env("TABFM_CROSSES", 0), env("TABFM_SVD", 0)
    maxfeat = env("TABFM_MAXFEAT")
    return {"norm_methods": [x.strip() for x in norm.split(",") if x.strip()] if norm else None,
            "max_num_features": int(maxfeat) if maxfeat else None,
            "n_feature_crosses": crosses if crosses == "sqrt" else int(crosses),
            "n_svd_features": svd if svd == "sqrt" else int(svd),
            "enable_nnls": env("TABFM_NNLS", "0") not in ("0", "false", "nu"),
            "outlier_threshold": float(env("TABFM_OUTLIER", "4.0"))}


# Originalele celor cinci metode patch-uite mai jos, captate O SINGURA DATA per proces.
_PATCH_ORIG = {}

# Contextul checkpointului pe MEMBRU de ansamblu. `dir` None inseamna ca patch-ul de pe
# `_batch_forward` cheama originalul si nu face nimic altceva, deci proba de dtype, calibrarea din
# notebook si orice alta predictie din proces raman neatinse: se aprinde numai in jurul unei cereri
# adevarate, din `ruleaza`.
#
# De ce exista. `ruleaza` scrie un `.npy` la finalul FIECAREI cereri si sare peste cele gata, deci
# o deconectare pierde cel mult cererea in curs. La `TABFM_MAXFEAT=160` cererea dura 12 minute si
# atat era de pierdut. La 256 trece de 40, adica peste pragul de siguranta de 30, iar Colab-ul
# gratuit taie sesiuni la 3-4 ore: pe o rulare de ~8 ore taierea la mijlocul unei cereri e aproape
# sigura. Checkpointul de aici coboara pierderea maxima de la o cerere intreaga la UN MEMBRU.
#
# `apel` numara chemarile lui `_batch_forward` in interiorul unei cereri. La configuratia care se
# ruleaza acum e mereu una singura (`predict` -> `_predict_internal` -> `_batch_forward`), dar cu
# `TABFM_NNLS` pornit `fit` mai cheama una per fold prin `_compute_oof_preds_scaled`, si fara
# numarul asta in cheie cele doua s-ar suprascrie reciproc.
#
# `calc` numara membrii chiar CALCULATI, nu si pe cei cititi de pe disc. Nu e statistica: e ce
# verifica `proba_checkpoint`, care cere zero treceri prin model la o reluare completa.
_CKPT = {"dir": None, "apel": 0, "calc": 0}


@contextlib.contextmanager
def checkpoint_membri(dir_ckpt):
    """Aprinde checkpointul pe membru pentru blocul dinauntru. `None` = nu se schimba nimic."""
    vechi = dict(_CKPT)
    _CKPT.update(dir=dir_ckpt, apel=0, calc=0)
    try:
        yield _CKPT
    finally:
        _CKPT.update(vechi)


def _amprenta_membru(*parti):
    """Identitatea intrarii unui membru: forme, dtype si octeti.

    Aceeasi idee ca `req_key`, cu un nivel mai jos. Amprenta intra in NUMELE fisierului, si asta e
    deliberat: daca `EnsembleGenerator` ar regenera altfel membrul `i` la reluare, fisierul pur si
    simplu nu se gaseste si membrul se recalculeaza, in loc sa se citeasca in tacere numerele
    altui membru. Costa ~15 ms pentru un bloc de 15 MB, fata de minutele pe care le apara.
    """
    h = hashlib.blake2b(digest_size=8)
    for a in parti:
        if a is None:
            h.update(b"\x00None")
            continue
        a = np.ascontiguousarray(a)
        h.update(str(a.dtype).encode())
        h.update(np.asarray(a.shape, np.int64).tobytes())
        h.update(a.tobytes())
    return h.hexdigest()


def instaleaza_patch_uri(verbose=True):
    """Cele patru patch-uri de memorie plus checkpointul pe membru, verificate inainte de instalare.

    De ce stau aici si nu in notebook. Prima versiune le tinea intr-o celula de Colab, iar celula
    aia s-a desincronizat tacut de fisierul din proiect: rularea a mers cu atentia NEPATCH-UITA si
    a dat OOM, iar traceback-ul arata `model.py:129`, adica biblioteca, nu celula. Aici nu se poate
    intampla: fisierul asta se copiaza in Drive ca un tot, are deja o garda de prospetime in
    notebook, si `ruleaza` cheama functia asta singur, deci nu depinde de ce celule ai rulat.

    Cele patru, si de ce fiecare:

    1. `MultiheadAttention.forward` — CEL CARE DECIDE DACA INCAPE. `ICLearning` ruleaza tot
       contextul ca o singura secventa si atentia lui e peste RANDURI, cu 16 capete, deci matricea
       de scoruri e `[1, 16, T, T]`: la T=14107 in bfloat16 sunt **5.93 GiB**, iar drumul `math` al
       lui SDPA, ales fiindca `attn_mask` e tensor dens, tine doua copii deodata. Termenul e
       PATRATIC in T si `TABFM_MAXFEAT` nu-l atinge deloc, fiindca latimea e colapsata inainte de
       stiva ICL. Patch-ul face doua lucruri: taie `k` si `v` la prefixul de context si scapa de
       masca, ceea ce lasa SDPA sa aleaga nucleul mem-efficient care nu materializeaza nimic; si,
       ca plasa de siguranta independenta de nucleu, taie pe intervale de query.
    2. `CellEmbedder.forward` — doua `torch.where` devin operatii pe loc.
    3. `ColEmbedding.forward` — varful de 4A devine 2A: `src` e o copie privata, deci poate fi
       tampon de iesire in loc de lista de bucati plus `torch.cat`.
    4. `RowInteraction.forward` — 3A devine 2A. Aici `src` e VIEW peste intrare, deci NU se scrie
       in el; se preloca doar iesirea.

    Pragurile difera, si asta e deliberat. Cele trei de memorie trebuie sa fie **exact zero** fata
    de original. Atentia nu poate: taierea pe query e exacta algebric, dar SDPA alege alt nucleu
    pentru alta forma, deci acumularea difera in ultimii biti. Masurat pe 64 de cazuri in float32:
    7.2e-07, cu patru ordine de marime sub precizia lui bfloat16. Pragul ei e 1e-5, si caderea lui
    e FATALA: fara patch-ul de atentie, la T=14107 OOM-ul e sigur, deci nu are rost sa pornesti.

    `TABFM_ATTN_GIB` (implicit 0.5) e bugetul unei matrice de scoruri, in GiB. Peste el se taie pe
    query. Butonul asta, nu `TABFM_MAXFEAT`, e raspunsul la un OOM din stiva ICL.

    Al cincilea nu e de memorie, e de SUPRAVIETUIRE: `TabFMRegressor._batch_forward`, care primeste
    checkpoint pe membru de ansamblu. Nu se poate verifica aici fiindca are nevoie de un model
    incarcat; poarta lui e `proba_checkpoint`, chemata din `ruleaza` dupa proba de dtype. Cand
    `_CKPT["dir"]` e None — adica peste tot in afara de o cerere adevarata — cheama originalul si
    nu schimba nimic.
    """
    import math

    import torch
    import torch.nn.functional as F
    import tabfm.src.classifier_and_regressor as R
    import tabfm.src.pytorch.model as M

    # `_batch_forward` e decorat cu `@jt.typed`, dar `functools.wraps` pastreaza `__module__` pe
    # `tabfm.src.classifier_and_regressor` (verificat), deci garda de mai jos il acopera si pe el.
    tinte = (("cell", M.CellEmbedder, "forward"), ("col", M.ColEmbedding, "forward"),
             ("row", M.RowInteraction, "forward"), ("attn", M.MultiheadAttention, "forward"),
             ("ckpt", R.TabFMRegressor, "_batch_forward"))
    if _PATCH_ORIG:
        for nume, clasa, atr in tinte:                 # re-verificarea se face pe ORIGINAL
            setattr(clasa, atr, _PATCH_ORIG[nume])
    else:
        for nume, clasa, atr in tinte:
            f = getattr(clasa, atr)
            # Garda care lipsea. Daca altcineva (o celula veche de notebook) a patch-uit deja,
            # am captura patch-ul drept "original" si verificarea de mai jos ar compara patch-ul
            # cu el insusi: ar tipari "exact 0" fara sa fi verificat nimic.
            if not getattr(f, "__module__", "").startswith("tabfm"):
                raise SystemExit(
                    f"[tabfm] {clasa.__name__}.{atr} e deja inlocuit de `{f.__qualname__}` din "
                    f"`{getattr(f, '__module__', '?')}`, deci originalul nu se mai poate captura. "
                    f"Restarteaza kernelul si ruleaza din nou, fara celula veche de patch-uri.")
            _PATCH_ORIG[nume] = f

    o_cell, o_col, o_row = _PATCH_ORIG["cell"], _PATCH_ORIG["col"], _PATCH_ORIG["row"]
    o_attn, o_bf = _PATCH_ORIG["attn"], _PATCH_ORIG["ckpt"]
    buget = [float(os.environ.get("TABFM_ATTN_GIB", "").strip() or 0.5)]

    def _attn_econom(self, query, key, value, attn_mask=None, rope=None):
        b, tq, d = query.shape
        q = self.q_proj(query).view(b, tq, self.nhead, self.hd)
        k = self.k_proj(key).view(b, key.shape[1], self.nhead, self.hd)
        v = self.v_proj(value).view(b, value.shape[1], self.nhead, self.hd)
        if self.rope_base is not None:
            if rope is not None:
                q, k = rope.rotate(q), rope.rotate(k)
            else:
                q = M.rope_interleaved(q, self.rope_base)
                k = M.rope_interleaved(k, self.rope_base)
        q, k = self.query_ln(q), self.key_ln(k)
        scale = 1.442695041 / math.sqrt(self.hd) * F.softplus(self.per_dim_scale.float())
        q = q * scale.to(q.dtype)
        q, k, v = (z.transpose(1, 2) for z in (q, k, v))            # [B, N, T, D]

        # (1) Masca lui TabFM e mereu un PREFIX de chei: `[B,1,1,Tk]`, adevarata pe primele
        #     `train_size` pozitii si falsa dupa (`ICLearning.forward`: `arange(t) < train_size`).
        #     Softmax peste prefix cu restul la -inf ESTE softmax peste felia de prefix, deci se
        #     taie k si v si masca dispare. Fara masca, SDPA poate alege nucleul mem-efficient,
        #     care nu materializeaza `[Tq, Tk]` niciodata. Se aplica doar cand TOATE randurile
        #     lotului au acelasi prefix: la ICL B=1 mereu; la coloane si randuri lungimile difera
        #     intre elementele lotului si atunci se sare peste optimizare.
        if (attn_mask is not None and attn_mask.dtype == torch.bool and attn_mask.dim() == 4
                and attn_mask.shape[1] == 1 and attn_mask.shape[2] == 1):
            m = attn_mask[:, 0, 0]
            n = int(m.sum(1).max().item())
            if 0 < n and bool(m[:, :n].all()) and not bool(m[:, n:].any()):
                k, v, attn_mask = k[:, :, :n], v[:, :, :n], None

        # (2) Plasa de siguranta, independenta de ce nucleu alege SDPA: daca matricea de scoruri
        #     tot iese peste buget, se taie pe INTERVALE DE QUERY. Softmax e pe randul de query,
        #     deci feliile sunt independente si taierea e exacta.
        tk = k.shape[2]
        if b * self.nhead * tq * tk * q.element_size() > buget[0] * 2**30:
            qc = max(64, int(buget[0] * 2**30 / (b * self.nhead * tk * q.element_size())))
            o = torch.empty_like(q)
            for s in range(0, tq, qc):
                mm = attn_mask
                if mm is not None and mm.shape[2] == tq:
                    mm = mm[:, :, s:s + qc]
                o[:, :, s:s + qc] = F.scaled_dot_product_attention(
                    q[:, :, s:s + qc], k, v, attn_mask=mm, scale=1.0)
        else:
            o = F.scaled_dot_product_attention(q, k, v, attn_mask=attn_mask, scale=1.0)
        return self.out_proj(o.transpose(1, 2).reshape(b, tq, d))

    def _cell_econom(self, x, y, train_size, cat_mask=None, d=None):
        if self.row_chunk_size is None:
            cell = self._cell(x, cat_mask, d=d)
        else:
            cell = torch.cat([self._cell(x[:, s:s + self.row_chunk_size], cat_mask, d=d)
                              for s in range(0, x.shape[1], self.row_chunk_size)], dim=1)
        if self.is_classifier:
            y_clean = torch.clamp(y.long(), 0, self.y_embedder_lookup.num_embeddings - 1)
            y_emb = self.y_embedder_lookup(y_clean)
        else:
            y_emb = self.y_embedder_lookup(y[..., None].to(cell.dtype))
        t = x.shape[1]
        tm = (torch.arange(t, device=x.device)[None, :] < train_size[:, None])[..., None, None]
        cell.add_(y_emb[:, :, None, :] * tm.to(cell.dtype))
        if d is not None:
            hc = cell.shape[2]
            colmask = (torch.arange(hc, device=cell.device)[None, :] < d[:, None])[:, None, :, None]
            cell.masked_fill_(~colmask, 0)
        return cell

    def _col_econom(self, x, train_size):
        b, t, hc, e = x.shape
        src = x.permute(0, 2, 1, 3).reshape(b * hc, t, e)
        ts = train_size.repeat_interleave(hc)
        mask = (torch.arange(t, device=x.device)[None, :] < ts[:, None])[:, None, None, :]
        cc = self.col_chunk_size
        if cc is None or src.shape[0] <= cc:
            out = self._stage(src, mask)
        else:
            # `src` e o copie privata (permute + reshape pe necontiguu copiaza), deci se poate
            # folosi drept tampon de iesire: feliile sunt disjuncte si `_stage` da tensor nou.
            # Garda pe data_ptr acopera cazul degenerat hc == 1, unde reshape chiar iese view.
            out = src if src.data_ptr() != x.data_ptr() else torch.empty_like(src)
            for s in range(0, src.shape[0], cc):
                out[s:s + cc] = self._stage(src[s:s + cc], mask[s:s + cc])
        return out.reshape(b, hc, t, e).permute(0, 2, 1, 3)

    def _row_econom(self, x, d=None):
        b, t, hc, e = x.shape
        src = x.reshape(b * t, hc, e)
        mask = None
        if d is not None:
            d_padded = d.to(torch.long) + self.num_cls
            valid = torch.arange(hc, device=x.device)[None, :] < d_padded[:, None]
            mask = valid.repeat_interleave(t, dim=0)[:, None, None, :]
        rc = self.row_chunk_size
        if rc is None or src.shape[0] <= rc:
            out = self._stage(src, mask)
        else:
            # aici `src` e VIEW peste x, deci NU se scrie in el. Se preloca iesirea, ca sa
            # dispara lista de bucati a lui torch.cat.
            oc = hc if self.output_full else self.num_cls
            out = torch.empty((src.shape[0], oc, e), dtype=x.dtype, device=x.device)
            for s in range(0, src.shape[0], rc):
                out[s:s + rc] = self._stage(src[s:s + rc],
                                            None if mask is None else mask[s:s + rc])
        if self.output_full:
            return out.reshape(b, t, hc, e)
        return out.reshape(b, t, -1)

    def _un_membru(self, X_batch, y_batch, cat_mask_batch, ds_batch_val):
        """Un singur membru prin model. Copiat cuvant cu cuvant din corpul buclei originale."""
        orig_batch_size = X_batch.shape[0]
        orig_seq_len = X_batch.shape[1]
        train_size_val = y_batch.shape[1]
        if y_batch.shape[1] < X_batch.shape[1]:
            y_batch = np.pad(y_batch, ((0, 0), (0, X_batch.shape[1] - y_batch.shape[1])),
                             mode="constant", constant_values=-100.0)
        out = R._predict_step_pytorch(self.model, X_batch, y_batch, train_size_val,
                                      ds_batch_val, cat_mask_batch)
        return out[:orig_batch_size, train_size_val:orig_seq_len, :]

    def _bf_ckpt(self, Xs, ys, cat_masks=None, ds=None):
        """`_batch_forward` cu checkpoint pe membru. Vezi `_CKPT` pentru de ce.

        Bucla de aici reproduce drumul PyTorch al originalului. Se poate, si e ieftin, fiindca la
        capetele ei totul e numpy: `_predict_step_pytorch` intoarce `out_t.float().cpu().numpy()`,
        iar dupa taiere un membru e `[1, T_test, 1]` float32, adica 2-22 KB pe cererile de aici.
        Se scrie membrul INTREG, nu media partiala a celor terminati: media ar cere un contor de
        ponderi ca sa se poata relua, ar rupe `enable_nnls` (care are nevoie de membrii separati)
        si ar arunca ablatia pe `n_estimators`, care asa iese gratis din fisierele de pe disc.
        """
        d = _CKPT["dir"]
        if d is None or not isinstance(self.model, torch.nn.Module):
            return o_bf(self, Xs, ys, cat_masks, ds)

        apel = _CKPT["apel"]
        _CKPT["apel"] = apel + 1
        bs = getattr(self, "batch_size", 1) or Xs.shape[0]
        nb = math.ceil(Xs.shape[0] / bs)
        if nb > 1:
            Xs_s, ys_s = np.array_split(Xs, nb), np.array_split(ys, nb)
            cm_s = np.array_split(cat_masks, nb) if cat_masks is not None else [None] * nb
            ds_s = np.array_split(ds, nb) if ds is not None else [None] * nb
        else:
            Xs_s, ys_s, cm_s, ds_s = [Xs], [ys], [cat_masks], [ds]

        os.makedirs(d, exist_ok=True)
        iesiri, t0, n = [], time.time(), len(Xs_s)
        for i, (Xb, yb, cmb, dsb) in enumerate(zip(Xs_s, ys_s, cm_s, ds_s)):
            fp = _amprenta_membru(Xb, yb, cmb, dsb)
            cale = os.path.join(d, f"a{apel}_m{i}_{fp}.npy")
            forma = (Xb.shape[0], Xb.shape[1] - yb.shape[1])
            if os.path.exists(cale):
                v = np.load(cale)
                if v.ndim == 3 and tuple(v.shape[:2]) == forma:
                    iesiri.append(v)
                    print(f"[tabfm]   membru {i + 1}/{n} de pe disc", flush=True)
                    continue
                # Amprenta se potriveste dar forma nu: fisier scris pe jumatate sau alt `apel`.
                # Se recalculeaza, nu se ghiceste.
                print(f"[tabfm]   membru {i + 1}/{n}: checkpoint cu forma {v.shape} in loc de "
                      f"{forma} + (L,); il recalculez", flush=True)
            t = time.time()
            out = _un_membru(self, Xb, yb, cmb, dsb)
            _CKPT["calc"] += 1
            # Scris atomic: Drive-ul montat cade la mijlocul unei scrieri, si un `.npy` trunchiat
            # ar fi mai rau decat unul lipsa, fiindca ar trece de verificarea de existenta.
            tmp = cale + ".tmp.npy"           # `.npy` la coada: altfel `np.save` il adauga singur
            np.save(tmp, out)
            os.replace(tmp, cale)
            iesiri.append(out)
            print(f"[tabfm]   membru {i + 1}/{n} in {time.time() - t:.0f}s "
                  f"(cerere {(time.time() - t0) / 60:.0f}m)", flush=True)
        return np.concatenate(iesiri, axis=0)

    def _dif_atentie():
        """Toate formele de masca pe care le produce TabFM, cu si fara taiere pe query."""
        torch.manual_seed(0)
        rau, pastrat = 0.0, buget[0]
        for d_model, nhead, rb in [(32, 4, None), (32, 4, 100000.0)]:
            at = M.MultiheadAttention(d_model, nhead, rb).eval()
            with torch.no_grad():
                for p in at.parameters():
                    p.normal_(0, 0.3)
            for B, Tq, Tk in [(1, 40, 40), (3, 40, 40), (2, 40, 7), (1, 5, 40)]:
                q = torch.randn(B, Tq, d_model)
                k, v = torch.randn(B, Tk, d_model), torch.randn(B, Tk, d_model)
                pref = torch.zeros(B, Tk, dtype=torch.bool)
                pref[:, :max(1, Tk // 2)] = True
                varia = torch.zeros(B, Tk, dtype=torch.bool)
                for i in range(B):
                    varia[i, :max(1, Tk - i * 3)] = True   # prefixe DIFERITE: taierea se sare
                rar = torch.rand(B, Tk) > 0.4               # masca rarefiata, nu e prefix
                rar[:, 0] = True
                for mk in (None, pref[:, None, None, :], varia[:, None, None, :],
                           rar[:, None, None, :]):
                    for gib in (1.0, 1e-9):                 # 1e-9 forteaza taierea pe query
                        buget[0] = gib
                        with torch.no_grad():
                            a = o_attn(at, q, k, v, mk, rope=None)
                            z = _attn_econom(at, q, k, v, mk, rope=None)
                        rau = max(rau, (a - z).abs().max().item())
        buget[0] = pastrat
        return rau

    def _dif_memorie():
        """Originalul si varianta economa pe intrari mici, pe toate drumurile."""
        torch.manual_seed(0)
        rau, e = 0.0, 16
        for rcs in (None, 3):
            ce = M.CellEmbedder(embed_dim=8, max_classes=3, is_classifier=False).eval()
            with torch.no_grad():
                ce.fourier_frequencies.normal_()
                ce.fourier_frequencies_cat.normal_()
            ce.row_chunk_size = rcs
            x, y = torch.randn(2, 7, 5), torch.randn(2, 7)
            ts, dd = torch.tensor([4, 5]), torch.tensor([5, 3])
            for cm, dv in [(None, None), (None, dd), (torch.rand(2, 5) > 0.5, dd)]:
                with torch.no_grad():
                    a = o_cell(ce, x, y, ts, cm, d=dv)
                    z = _cell_econom(ce, x, y, ts, cm, d=dv)
                rau = max(rau, (a.float() - z.float()).abs().max().item())
        for cc in (None, 3, 100):
            for hc in (7, 1):                       # hc == 1 e cazul in care reshape iese view
                co = M.ColEmbedding(e, 2, 2, e * 2, 4).eval()
                co.col_chunk_size = cc
                x, ts = torch.randn(2, 9, hc, e), torch.tensor([5, 7])
                with torch.no_grad():
                    a, z = o_col(co, x, ts), _col_econom(co, x, ts)
                rau = max(rau, (a.float() - z.float()).abs().max().item())
        for full in (True, False):
            for rc in (None, 4, 100):
                ri = M.RowInteraction(e, 2, 2, e * 2, 3, output_full=full).eval()
                ri.row_chunk_size = rc
                x = torch.randn(2, 9, 7, e)
                for dv in (None, torch.tensor([4, 2])):
                    with torch.no_grad():
                        a, z = o_row(ri, x, dv), _row_econom(ri, x, dv)
                    rau = max(rau, (a.float() - z.float()).abs().max().item())
        return rau

    dat = _dif_atentie()
    if dat >= 1e-5:
        raise SystemExit(
            f"[tabfm] patch-ul de atentie difera de original cu {dat:.3e}, peste pragul 1e-5. "
            f"Versiunea de tabfm s-a schimbat si patch-ul nu mai e valid pentru ea. Nu pornesc: "
            f"fara el, stiva ICL cere [1, nhead, T, T], adica ~6 GiB la T=14107, de doua ori.")
    M.MultiheadAttention.forward = _attn_econom

    dif = _dif_memorie()
    if dif == 0.0:
        M.CellEmbedder.forward = _cell_econom
        M.ColEmbedding.forward = _col_econom
        M.RowInteraction.forward = _row_econom
    # Se instaleaza neconditionat: cat timp `_CKPT["dir"]` e None, patch-ul cheama originalul si
    # nu poate schimba niciun numar. Ce chiar se intampla cand e aprins e verificat de
    # `proba_checkpoint`, care are nevoie de model si deci ruleaza in `ruleaza`, nu aici.
    R.TabFMRegressor._batch_forward = _bf_ckpt
    if verbose:
        print(f"[tabfm] patch-uri: atentie {dat:.1e} (prag 1e-5, buget {buget[0]} GiB), "
              f"memorie {'exact 0' if dif == 0.0 else f'{dif:.3e} NEINSTALATE'}, "
              f"checkpoint pe membru instalat", flush=True)
    if dif != 0.0 and verbose:
        print(f"[tabfm]   cele 3 patch-uri de memorie NU s-au instalat: alta versiune de tabfm. "
              f"Varful creste cu ~50%; daca da OOM, scade TABFM_MAXFEAT.", flush=True)
    return {"atentie": dat, "memorie": dif, "attn_gib": buget[0], "ckpt": True}


def proba_checkpoint(model, verbose=True):
    """Poarta checkpointului pe membru: dovedeste ca o RELUARE da acelasi numar, nu unul apropiat.

    Cele patru patch-uri de memorie se verifica fata de original pe tensori mici, sincron. Asta nu
    se poate: intrebarea nu e daca aritmetica unui membru e aceeasi, ci daca membrul `i` regenerat
    maine din `EnsembleGenerator` e ACELASI cu membrul `i` de azi. Raspunsul nu se poate citi din
    cod — depinde de faptul ca `random.Random(random_state)` e consumat in aceeasi ordine — deci se
    masoara, o data, pe date sintetice, inainte de orele de GPU.

    Aceeasi predictie, de patru ori:

        p0  checkpoint stins             drumul original, reperul
        p1  checkpoint, director gol     trebuie sa scrie cate un fisier per membru
        p2  dupa stergerea ULTIMULUI     cadere la mijlocul unei cereri: recalculeaza exact 1
        p3  cu toate fisierele pe disc   reluare completa: ZERO treceri prin model

    Cerinta e `array_equal`, adica exact, nu cu toleranta: p2 si p3 citesc de pe disc chiar
    numerele scrise de p1. Numaratoarea de membri calculati (`_CKPT["calc"]`) e cea care distinge
    o reluare adevarata de una care doar a recalculat totul in tacere si a iesit la fel.

    Ansamblul de proba imita configuratia reala: aceleasi `norm_methods` si acelasi `crosses`, deci
    membrii ies de latimi DIFERITE (par 8 coloane, impar 8+2), exact cazul care umple lotul la
    latimea celui mai lat.
    """
    import glob
    import shutil
    import tempfile

    from tabfm import TabFMRegressor
    ans = parametri_ansamblu()
    rng = np.random.default_rng(7)
    n, d, k = 256, 12, 3
    X = rng.normal(size=(n, d)).astype(np.float32)
    y = (X[:, 0] * 0.5 + X[:, 1] * 0.2 + rng.normal(scale=0.1, size=n)).astype(np.float32)
    Xp = rng.normal(size=(24, d)).astype(np.float32)

    def _prezice():
        reg = TabFMRegressor(model=model, n_estimators=k, max_num_features=8,
                             norm_methods=ans["norm_methods"],
                             n_feature_crosses=ans["n_feature_crosses"],
                             n_svd_features=ans["n_svd_features"],
                             enable_nnls=False, outlier_threshold=ans["outlier_threshold"],
                             random_state=42, verbose=False)
        reg.fit(X, y)
        return np.asarray(reg.predict(Xp), dtype=np.float64)

    p0 = _prezice()                                   # `_CKPT["dir"]` e None: drumul original
    tmp = tempfile.mkdtemp(prefix="tabfm_ckpt_")
    try:
        with checkpoint_membri(tmp) as c:
            p1, c1 = _prezice(), c["calc"]
        fise = sorted(glob.glob(os.path.join(tmp, "*.npy")))
        if len(fise) != k or c1 != k:
            raise SystemExit(f"[tabfm] checkpoint pe membru: {len(fise)} fisiere si {c1} membri "
                             f"calculati pentru {k} membri. Patch-ul nu scrie ce trebuie.")
        os.remove(fise[-1])                           # cadere la mijlocul cererii
        with checkpoint_membri(tmp) as c:
            p2, c2 = _prezice(), c["calc"]
        with checkpoint_membri(tmp) as c:
            p3, c3 = _prezice(), c["calc"]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if c2 != 1 or c3 != 0:
        raise SystemExit(
            f"[tabfm] checkpoint pe membru: dupa stergerea unui singur fisier s-au recalculat {c2} "
            f"membri (asteptat 1), iar cu toate pe disc {c3} (asteptat 0). Amprentele nu se "
            f"potrivesc, deci `EnsembleGenerator` NU regenereaza aceiasi membri la reluare si "
            f"checkpointul n-ar salva nimic. Nu pornesc.")
    for nume, q in (("p1", p1), ("p2", p2), ("p3", p3)):
        if not np.array_equal(p0, q):
            raise SystemExit(
                f"[tabfm] checkpoint pe membru: {nume} difera de drumul original cu "
                f"{np.abs(p0 - q).max():.3e}. Reluarea ar schimba cifra care se raporteaza. "
                f"Nu pornesc.")
    if verbose:
        print(f"[tabfm] checkpoint pe membru: {k} membri scrisi, reluare partiala 1 recalculat, "
              f"reluare completa 0, toate patru bit-identice", flush=True)
    return True


def ruleaza(blocuri, dest, device=None, n_estimators=None, max_rows=None, dtype=None):
    """Ruleaza TabFM pe toate cererile, cu UN SINGUR model incarcat. Scrie dupa fiecare cerere.

    `dest` e un director: un `.npy` per cheie plus `manifest.txt`. Scrisul incremental inseamna ca o
    deconectare de Colab sau o intrerupere locala nu pierde decat cererea in curs, iar o reluare
    sare peste ce exista deja.

    Sub `dest/_ckpt/<cheie>/` sta al doilea nivel de protectie, cel din INTERIORUL unei cereri: un
    `.npy` per membru de ansamblu, scris pe masura ce membrii se termina. La `TABFM_MAXFEAT=160` o
    cerere dura 12 minute si primul nivel ajungea; la 256 trece de 40, peste pragul de siguranta de
    30, si o sesiune Colab taiata la mijloc ar arde tot. Cu nivelul al doilea pierderea maxima e un
    membru. Fisierele raman pe disc dupa ce cererea se incheie (cateva zeci de KB fiecare) fiindca
    din ele iese gratis ablatia pe `n_estimators`: media primilor k membri. `TABFM_CKPT=0` il
    stinge, si atunci comportarea e exact cea de dinainte.

    `dtype`: bfloat16 e implicitul lor si e gandit pentru Ampere in sus; implicitul de aici e
    bfloat16 pe CUDA si float32 in rest, si se poate forta cu TABFM_DTYPE. float16 e REFUZAT, nu
    e o optiune mai ieftina: vezi `proba_finita`. Daca dtype-ul nu e cerut explicit si nu trece
    proba (bf16 pe Turing, unde cuBLAS cere 8.0), rularea coboara singura pe float32 si o anunta.

    Butoanele de ansamblu (TABFM_NORM, TABFM_MAXFEAT, TABFM_CROSSES, TABFM_SVD, TABFM_NNLS,
    TABFM_OUTLIER) sunt descrise la locul lor mai jos, langa `cfg`. Toate intra in `setari.json`.

    `n_estimators` costa TIMP, nu memorie. `TabFMRegressor` are `batch_size=1`, deci membrii
    ansamblului trec prin model unul cate unul (`_batch_forward` in classifier_and_regressor.py);
    varful de memorie e al unui singur membru indiferent cati ceri. Butoanele de memorie sunt
    latimea lui X, numarul de randuri de context si TABFM_CHUNK.

    `TABFM_CHUNK`: marimea chunk-ului de randuri pentru activari. Exista fiindca implicitul lor,
    `_ROW_CHUNK_SIZE = 4096` din `src/pytorch/model.py`, e ales explicit "for memory safety on a
    40 GB GPU", iar pe un T4 de 14.5 GB `predict` da OOM la 400 de coloane: TabFM ruleaza tot
    contextul ca o singura secventa, deci activarile cresc cu randuri x coloane.

    Butonul e sigur pentru cifre, si asta e important: comentariul lor spune ca "chunking is exact
    (identical outputs)", iar codul confirma, `torch.cat(parts, dim=1)` reasambleaza acelasi tensor.
    Deci scaderea lui schimba numai varful de memorie si putin timpul, NU rezultatul. Pe 14.5 GB,
    1024 e valoarea care a mers.

    `TABFM_ATTN_GIB`: bugetul unei matrice de scoruri de atentie, in GiB, implicit 0.5. E butonul
    pentru OOM-ul din stiva ICL, unde `TABFM_MAXFEAT` nu ajuta cu nimic fiindca latimea e deja
    colapsata acolo. Vezi `instaleaza_patch_uri`.
    """
    import torch
    from tabfm import TabFMRegressor
    from tabfm.src.pytorch.tabfm_v1_0_0 import load

    device = device or os.environ.get("TABFM_DEVICE", "cpu")
    n_estimators = int(n_estimators or os.environ.get("TABFM_ESTIMATORS", "8"))
    if max_rows is None:
        mr = os.environ.get("TABFM_MAX_ROWS", "").strip()
        max_rows = int(mr) if mr else None
    # dtype. TabFM e antrenat si documentat pentru bfloat16; float32 e varianta de referinta.
    # float16 NU e o a treia optiune degradata, e o rulare moarta: vezi `proba_finita`. Refuzul de
    # aici e explicit fiindca esecul lui e tacut pana la prima cerere, si arata ca o problema de
    # date ("finite 0"), nu ca o problema de precizie.
    cerut = dtype if isinstance(dtype, str) else (None if dtype is None else str(dtype).split(".")[-1])
    cerut = cerut or os.environ.get("TABFM_DTYPE", "").strip() or None
    fortat = cerut is not None
    cerut = cerut or ("bfloat16" if device == "cuda" else "float32")
    if cerut == "float16":
        raise SystemExit(
            "[tabfm] float16 nu merge cu TabFM: reziduul stivei ICL ajunge la ~4300 si `linear2` "
            "trece de 65504, deci toate predictiile ies NaN (masurat: 0 din 150 finite, la fel pe "
            "MPS si pe CUDA). Foloseste bfloat16 (Ampere in sus) sau float32.")
    dtype = getattr(torch, cerut)

    os.makedirs(dest, exist_ok=True)

    # Poarta de setari. Cheia unei cereri acopera (Xtr, ytr, Xpredict), adica INTRAREA, nu si cum a
    # fost rulata. Fara verificarea de aici, o reluare cu alt `n_estimators` ar sari peste fisierele
    # existente si ar amesteca tacut doua setari in acelasi set de predictii, iar r-ul care iese
    # n-ar corespunde niciunei configuratii. Setarile se scriu la prima rulare si se compara la
    # fiecare reluare; ca sa rulezi altfel, dai alt `dest`.
    # Butoanele de ansamblu. Toate intra in `setari.json` si sunt comparate la reluare, deci nu se
    # pot amesteca doua configuratii in acelasi `dest`. Ce fac, si ce costa:
    #
    #   TABFM_NORM      lista de normalizari peste care se impart membrii ("none", "power",
    #                   "quantile", "quantile_rtdl", "robust"). Implicit ["none", "power"].
    #                   GRATIS pe GPU: `EnsembleGenerator` cicleaza cei `n_estimators` membri
    #                   peste lista, nu adauga treceri. Costa doar CPU la preprocesare.
    #   TABFM_MAXFEAT   cate coloane vede un membru. Sub latimea reala, fiecare membru ia alt
    #                   subesantion, deci membrii se decoreleaza SI costa mai putin, fiindca in
    #                   coloane costul e supra-patratic. Butonul cu cel mai bun raport.
    #   TABFM_CROSSES   "sqrt" adauga sqrt(n) produse de perechi. Alocarea lor e "split": doar
    #   TABFM_SVD       membrii impari primesc coloanele in plus, cei pari raman pe latimea de
    #                   baza. Deci costul e ~jumatate din ce pare.
    #   TABFM_NNLS      pondereaza membrii cu NNLS in loc sa-i medieze. Costa aproape inca un
    #                   pasaj complet: `_compute_oof_preds_scaled` mai face o trecere peste toti
    #                   membrii. Pe blocurile astea (N ~13.5k) foloseste UN singur split de
    #                   validare, nu 5 folduri, fiindca N/5 trece de `min_rows_for_single_val_split`.
    #                   Splitul se ia din Xtr, deci nu atinge limba tinuta afara: curat sub LOLO.
    #   TABFM_OUTLIER   pragul de z la care se taie cozile. Implicit 4.0.
    ans = parametri_ansamblu()
    norm, maxfeat = ans["norm_methods"], ans["max_num_features"]
    crosses, svd = ans["n_feature_crosses"], ans["n_svd_features"]
    nnls, outlier = ans["enable_nnls"], ans["outlier_threshold"]
    if nnls and max_rows is not None:
        raise SystemExit("[tabfm] TABFM_NNLS si TABFM_MAX_ROWS nu merg impreuna (tabfm le refuza "
                         "explicit in TabFMRegressor.__init__).")

    cfg = {"n_estimators": n_estimators, "max_rows": max_rows, "dtype": str(dtype),
           "n_cereri": len(cereri(blocuri)), **ans}
    cp = os.path.join(dest, "setari.json")
    if os.path.exists(cp):
        vechi = json.load(open(cp))
        dif = {k: (vechi.get(k), cfg[k]) for k in cfg if vechi.get(k) != cfg[k]}
        # dtype nu intra in refuz: pe alt hardware e legitim altul, si nu schimba ce se calculeaza,
        # doar precizia cu care. Se anunta, atat.
        dif.pop("dtype", None)
        if dif:
            raise SystemExit(f"{cp}: setarile difera de rularea care a scris deja aici: {dif}. "
                             f"Predictiile s-ar amesteca. Foloseste alt `dest`.")
        dt_vechi = vechi.get("dtype")
    else:
        dt_vechi = None
    # Scrisul lui `setari.json` se face DUPA proba de dtype, mai jos: dtype-ul care ajunge pe disc
    # trebuie sa fie cel cu care s-a rulat, nu cel cerut, fiindca proba poate cobori pe float32.

    reqs = cereri(blocuri)
    chunk = os.environ.get("TABFM_CHUNK", "").strip()
    ckpt_pornit = os.environ.get("TABFM_CKPT", "1").strip().lower() not in ("0", "false", "nu")

    def incarca(dt):
        m = load(model_type="regression", device=device, dtype=dt)
        if chunk:
            r, n = int(chunk), 0
            for mod in m.modules():
                if hasattr(mod, "row_chunk_size"):
                    mod.row_chunk_size = r; n += 1
                if hasattr(mod, "ffn_chunk_size"):
                    mod.ffn_chunk_size = max(2 * r, 512); n += 1
            if n == 0:
                raise SystemExit("TABFM_CHUNK cerut, dar niciun modul nu are `row_chunk_size`. "
                                 "Alta versiune de tabfm: verifica src/pytorch/model.py.")
        return m

    # Patch-urile de memorie se instaleaza AICI, nu intr-o celula de notebook, si `ruleaza` nu
    # porneste fara cel de atentie. Vezi `instaleaza_patch_uri`: fara el, stiva ICL cere
    # [1, nhead, T, T] si la T=14107 placa da OOM la prima cerere, dupa ce ai platit incarcarea.
    instaleaza_patch_uri()

    t0 = time.time()
    model = incarca(dtype)
    # Poarta de dtype. Cade in cateva secunde pe date sintetice, nu dupa minutele primei cereri
    # adevarate. bfloat16 e implicitul lor, dar GEMM-ul bf16 cere Ampere (8.0) in cuBLAS, deci pe
    # un T4 (7.5) poate sa crape sau sa iasa neifinit. Daca dtype-ul n-a fost cerut explicit,
    # coborarea la float32 e automata; daca a fost cerut, se opreste, ca sa nu se schimbe tacut
    # precizia sub o cifra care se raporteaza.
    try:
        bun = proba_finita(model)
        eroare = None
    except Exception as e:                                    # bf16 nesuportat pe Turing crapa aici
        bun, eroare = False, f"{type(e).__name__}: {e}"
    if not bun:
        motiv = eroare or "predictii neifinite sau constante pe date sintetice"
        if fortat:
            raise SystemExit(f"[tabfm] proba de sanatate a cazut pe {device}/{dtype}: {motiv}. "
                             f"dtype a fost cerut explicit, deci nu cobor singur. Scoate "
                             f"TABFM_DTYPE ca sa cada automat pe float32.")
        if dtype == torch.float32:
            raise SystemExit(f"[tabfm] float32 nu trece proba pe {device}: {motiv}. Nu e o "
                             f"problema de precizie: verifica instalarea si checkpointul.")
        print(f"[tabfm] ATENTIE: {dtype} nu trece proba pe {device} ({motiv}); trec pe float32.\n"
              f"[tabfm]   Atentie la memorie: checkpointul are 1.65 miliarde de parametri, deci in\n"
              f"[tabfm]   float32 greutatile singure ocupa 6.14 GiB, fata de 3.07 in bfloat16, iar\n"
              f"[tabfm]   fiecare tensor de etapa [1, T, HC, 256] se dubleaza. Pe o placa de 15 GiB\n"
              f"[tabfm]   asta nu incape la latimi utile: daca urmeaza un OOM, nu scadea\n"
              f"[tabfm]   n_estimators (nu e butonul), ci TABFM_MAXFEAT, sau treci pe o placa cu\n"
              f"[tabfm]   bfloat16 in hardware (capability 8.0 in sus).", flush=True)
        del model
        if device == "cuda":
            torch.cuda.empty_cache()
        dtype = torch.float32
        model = incarca(dtype)
        if not proba_finita(model):
            raise SystemExit(f"[tabfm] nici float32 nu trece proba pe {device}. Nu e o problema "
                             f"de precizie: verifica instalarea si checkpointul.")
    # Poarta checkpointului. Cade in cateva secunde pe date sintetice, ca si cea de dtype, si din
    # acelasi motiv: daca reluarea n-ar da acelasi numar, asta trebuie stiut inainte de ore de GPU,
    # nu dupa prima deconectare.
    if ckpt_pornit:
        proba_checkpoint(model)

    cfg["dtype"] = str(dtype)                                 # dupa proba, ca sa se scrie ce a mers
    if dt_vechi is None:
        with open(cp, "w") as f:
            json.dump(cfg, f, indent=1)
    elif dt_vechi != cfg["dtype"]:
        print(f"[tabfm] ATENTIE: dtype {dt_vechi} -> {cfg['dtype']} fata de ce e deja pe disc",
              flush=True)
    if chunk:
        print(f"[tabfm] chunk de randuri {chunk} (implicit 4096, ales pentru 40 GB)", flush=True)
    print(f"[tabfm] model pe {device}/{dtype} in {time.time()-t0:.0f}s | {len(reqs)} cereri, "
          f"n_estimators={n_estimators}, max_rows={max_rows}, chunk={chunk or 'implicit'}",
          flush=True)
    print(f"[tabfm] ansamblu: norm={norm or ['none', 'power']}, max_num_features={maxfeat or 'tot'}"
          f", crosses={crosses}, svd={svd}, nnls={nnls}, outlier={outlier}", flush=True)
    unde = os.path.join(dest, "_ckpt") if ckpt_pornit else "STINS (TABFM_CKPT=0)"
    print(f"[tabfm] checkpoint pe membru: {unde}", flush=True)

    man = []
    for i, (nume, Xtr, ytr, Xp) in enumerate(reqs, 1):
        k = req_key(Xtr, ytr, Xp)
        man.append(f"{k}  {nume}  ctx={Xtr.shape} pred={Xp.shape}")
        p = os.path.join(dest, f"{k}.npy")
        if os.path.exists(p):
            print(f"[tabfm] {i:2d}/{len(reqs)} {nume:14s} deja pe disc, sar", flush=True)
            continue
        # NaN: `TransformToNumerical` nu are contract documentat pe NaN, iar coloanele de suprafata
        # sunt NaN pe `ja` si `si`. Mediana se calculeaza pe ANTRENARE, conventia bratului Ridge.
        med = np.nanmedian(Xtr, axis=0)
        med = np.where(np.isfinite(med), med, 0.0)
        A = np.where(np.isfinite(Xtr), Xtr, med).astype(np.float32)
        P = np.where(np.isfinite(Xp), Xp, med).astype(np.float32)
        b = np.asarray(ytr, np.float32)     # float32, nu float64: vezi nota de mai jos
        if max_rows is not None and len(A) > max_rows:
            sel = np.random.default_rng(42).choice(len(A), max_rows, replace=False)
            print(f"[tabfm] ATENTIE: context subesantionat {len(A)} -> {max_rows}", flush=True)
            A, b = A[sel], b[sel]
        t = time.time()
        # Contextul se aprinde in jurul lui `fit` SI al lui `predict`, nu doar al celui de-al
        # doilea: cu `TABFM_NNLS` pornit `fit` face si el treceri prin model, si acelea merita la
        # fel de mult sa nu se piarda. La reluare `fit` se reface intreg (preprocesarea pe CPU,
        # cateva minute), fiindca membrii trebuie regenerati ca sa se stie carui membru ii apartine
        # fiecare fisier; ce se sare e partea de GPU, adica toata cheltuiala.
        with checkpoint_membri(os.path.join(dest, "_ckpt", k) if ckpt_pornit else None):
            reg = TabFMRegressor(model=model, n_estimators=n_estimators,
                                 max_num_features=maxfeat or A.shape[1],
                                 norm_methods=norm, n_feature_crosses=crosses, n_svd_features=svd,
                                 enable_nnls=nnls, outlier_threshold=outlier,
                                 random_state=42, verbose=False)
            reg.fit(A, b)
            pred = np.asarray(reg.predict(P), dtype=np.float64)
        if len(pred) != len(P) or not np.isfinite(pred).all():
            raise SystemExit(f"[tabfm] {nume}: {len(pred)} predictii pentru {len(P)} randuri, "
                             f"finite {np.isfinite(pred).sum()}")
        np.save(p, pred)
        print(f"[tabfm] {i:2d}/{len(reqs)} {nume:14s} ctx={A.shape} pred={P.shape} "
              f"in {time.time()-t:.0f}s (total {(time.time()-t0)/60:.0f}m)", flush=True)
    with open(os.path.join(dest, "manifest.txt"), "w") as f:
        f.write("\n".join(man) + "\n")
    print(f"-> {dest}")


# `ytr` se trimite in float32, nu float64. `tabfm/src/classifier_and_regressor.py:1801` face
# `.to(device)` INAINTE de verificarea de dtype de pe linia urmatoare, iar MPS nu accepta float64,
# deci un y float64 opreste rularea pe MPS inainte sa ajunga la conversia lor. Complexitatea e in
# [0, 1], deci float32 e cu mult peste precizia necesara.
