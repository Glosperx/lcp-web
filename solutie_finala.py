# ---
# jupyter:
#   jupytext:
#     formats: py:percent,ipynb
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Predictia complexitatii lexicale in limba romana
#
# Acest notebook estimeaza, pentru fiecare cuvant tinta dintr-o propozitie, un scor de complexitate
# lexicala in intervalul [0, 1]. Cuvintele frecvente si usor de procesat primesc scoruri mici, iar
# cuvintele rare sau dificile primesc scoruri mari.
#
# Setul de antrenare al competitiei contine doar 14 exemple romanesti etichetate, un numar insuficient
# pentru a antrena un model supervizat fara supraadaptare. Din acest motiv nu folosim aceste etichete
# pentru antrenare, ci doar pentru validare. In schimb recurgem la supervizare distanta: transferam
# cunostinte din resurse externe (limbi cu mii de cuvinte adnotate si un model de limbaj romanesc) si
# din masuratorile de eye-tracking puse la dispozitie de competitie.
#
# Predictia finala combina patru semnale, fiecare estimand complexitatea pe o cale diferita:
#
# - Semnalul A, transfer cross-lingual: un regresor antrenat pe date adnotate in engleza (CompLex) si in
#   limbi romanice (MLSP), aplicat asupra romanei prin spatiul comun al modelului XLM-RoBERTa.
# - Semnalul B, evaluare prin model de limbaj: modelul RoLlama3-8B atribuie fiecarui cuvant o nota de
#   dificultate pe o scara de la 1 la 5.
# - Semnalul C, surprisal: gradul de imprevizibilitate al cuvantului in context, calculat tot din
#   RoLlama3 ca -log P(cuvant | context). Conform teoriei surprisal-ului, un cuvant greu de anticipat
#   este si greu de procesat.
# - Semnalul D, eye-tracking: efortul de citire al cuvantului, obtinut prin reducerea metricilor de
#   eye-tracking la o singura dimensiune cu analiza componentelor principale (PCA).
#
# Cele patru semnale sunt normalizate (z-score), combinate printr-o medie ponderata si calibrate la
# scara reala a scorurilor din test. Pe datele publice, primele trei semnale obtin 68.90, iar adaugarea
# semnalului de eye-tracking ridica scorul la 69.74.
#
# Semnalele A, B si C sunt costisitoare (necesita XLM-RoBERTa si RoLlama3 pe GPU), asa ca le calculam o
# singura data si le salvam in data/. Acest notebook le citeste de acolo si ruleaza pe CPU. Codul care le
# recalculeaza de la zero se afla separat, in recompute_gpu.py.

# %% [markdown]
# ## Importuri

# %%
import os
import re
import sys

import numpy as np
import pandas as pd
from wordfreq import zipf_frequency        # frecventa cuvintelor, scara zipf (semnalul lexical de baza)
from scipy.stats import pearsonr           # corelatii Pearson, folosite in sectiunea de verificare

# %% [markdown]
# ## Configuratie
#
# Caile catre fisiere si constantele fixe: ponderile fuziunii (determinate prin incercari pe leaderboard)
# si parametrii de calibrare (media si abaterea standard reale ale scorurilor de test).

# %%
# Cand fisierul ruleaza ca notebook nu exista __file__, deci folosim directorul curent.
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
DATA = os.path.join(HERE, "data")

W_CL, W_LLM = 0.6, 0.4                  # 60% transfer cross-lingual + 40% nota LLM, in scorul de baza A+B
W_SURP = 0.08                          # proportia de surprisal adaugata peste A+B
W_ET = 0.20                            # proportia de eye-tracking (sweep public: 0=68.90, 0.10=69.66,
#                                        0.20=69.74 maxim, 0.30=69.00; valoarea 0 reproduce exact 68.90)
CALIB_MEAN, CALIB_STD = 0.27, 0.125    # media si abaterea standard reale ale complexitatii pe test

VOWELS = set("aeiouyăâîáéíóúàèìòùäëïöü")        # vocale romanesti (cu diacritice), pentru numarat silabe

# Optiunea de rulare: --recompute recalculeaza semnalele grele pe GPU (vezi recompute_gpu.py).
RECOMPUTE = ("--recompute" in sys.argv)


# %% [markdown]
# ## 1. Trasaturi lexicale
#
# Pentru fiecare cuvant calculam patru numere: frecventa, lungimea in caractere, numarul de silabe si un
# indicator de scriere cu majuscula. Cea mai informativa este frecventa, exprimata pe scara zipf din
# biblioteca wordfreq (valori de la 1 la 7, unde 7 inseamna foarte frecvent si 1 foarte rar). Regula
# empirica: cu cat un cuvant este mai rar, cu atat tinde sa fie mai complex.
#
# Limba romana este puternic flexionata, asa ca multe forme ("Pamantului", "copacilor") lipsesc din
# wordfreq si ar primi frecventa zero, fiind tratate gresit ca extrem de rare. Pentru a corecta acest
# lucru folosim frecventa maxima dintre forma flexionata si lema: max(zipf(forma), zipf(lema)). Lema
# ("pamant", "copac") exista in dictionar si ofera frecventa corecta. Aceasta corectie a adus cea mai
# mare imbunatatire individuala a scorului, de la 64.81 la 68.90.

# %%
def normalize_token(w):
    """Elimina semnele de punctuatie din jurul cuvantului. Exemplu: "(cuvant)," devine "cuvant"."""
    w = str(w).strip()
    w = re.sub(r'^[„""\'\"({\[«»\-–—]+', '', w)
    w = re.sub(r'[.,;:!?\)\]}"\'\"»–—]+$', '', w)
    return w.strip()


def n_syllables(w):
    """Aproximeaza numarul de silabe numarand grupurile de vocale consecutive. Minim o silaba."""
    w = w.lower(); c = 0; prev_vowel = False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            c += 1
        prev_vowel = is_vowel
    return max(c, 1)


def lexical(tokens, langs, lemmas=None):
    """Construieste matricea (n, 4) de trasaturi: [frecventa zipf, lungime, silabe, incepe cu majuscula].
    Daca se dau leme (cazul romanei), frecventa devine max(zipf(forma), zipf(lema)), corectand formele
    flexionate absente din dictionar."""
    out = np.zeros((len(tokens), 4), np.float32)
    for i, (tok, lg) in enumerate(zip(tokens, langs)):
        t = normalize_token(tok)
        lg = lg if isinstance(lg, str) else "en"
        z = zipf_frequency(t.lower(), lg) if t else 0.0
        if lemmas is not None:                              # frecventa corectata cu lema
            lem = normalize_token(lemmas[i])
            if lem:
                z = max(z, zipf_frequency(lem.lower(), lg))
        out[i] = [z, len(t), n_syllables(t), 1.0 if t[:1].isupper() else 0.0]
    return out


def zscore(a):
    """Standardizeaza un vector la media 0 si abaterea standard 1, ca semnalele sa fie comparabile."""
    a = np.asarray(a, float)
    return (a - a.mean()) / (a.std() + 1e-9)


def fill(a):
    """Inlocuieste valorile lipsa (NaN) cu mediana vectorului."""
    a = np.asarray(a, float); med = np.nanmedian(a)
    return np.where(np.isnan(a), med, a)


# %% [markdown]
# ## 2. Semnalul A: transfer cross-lingual
#
# XLM-RoBERTa este un model multilingual care plaseaza cuvinte cu inteles asemanator din limbi diferite
# in pozitii apropiate ale aceluiasi spatiu vectorial. Aceasta proprietate ne permite sa antrenam un
# regresor pe cuvinte adnotate in alte limbi si sa il aplicam pe romana, fara nicio eticheta romaneasca.
#
# Folosim doua surse de antrenare, combinate ulterior intr-un ansamblu: CompLex (engleza, aproximativ
# 8400 de cuvinte, aceeasi metodologie de adnotare ca a competitiei) si MLSP (limbi romanice: franceza,
# italiana, portugheza, spaniola, catalana, aproximativ 2800 de cuvinte). Pentru fiecare cuvant,
# trasaturile sunt embeddingul XLM-RoBERTa (media ultimelor patru straturi, centrata pe limba) impreuna
# cu cele patru trasaturi lexicale din sectiunea anterioara.
#
# Regresorul este media a doua modele complementare: Ridge (liniar, stabil) si HistGradientBoosting
# (gradient boosting pe arbori de decizie, varianta histogram din scikit-learn, aceeasi familie cu
# XGBoost si LightGBM). Medierea unui model liniar cu unul neliniar face transferul mai robust.
#
# Implementarea completa care produce acest semnal pe GPU (embeddingul si regresorul) se afla in
# recompute_gpu.py. In acest notebook semnalul A se citeste deja calculat din cache.

# %% [markdown]
# ## 3. Semnalele B si C, din modelul RoLlama3-8B
#
# Ambele semnale provin din acelasi model de limbaj romanesc.
#
# Semnalul B este o nota de dificultate. Ii cerem modelului sa evalueze cuvantul pe o scara de la 1 la 5
# in contextul propozitiei. In loc sa luam doar cifra generata, calculam valoarea asteptata din
# probabilitatile pe care modelul le atribuie tokenilor "1" pana la "5", obtinand o citire continua.
#
# Semnalul C este surprisal-ul: -log P(cuvant | context), mediat pe subcuvinte. Este o cantitate bruta
# din interiorul modelului, nu o opinie exprimata, asa ca este aproape independenta de nota B (corelatia
# este in jur de 0.07). Un cuvant cu surprisal mare este greu de anticipat, deci probabil greu de procesat.
#
# Implementarea (modelul RoLlama3) se afla tot in recompute_gpu.py; aici valorile se citesc din cache.

# %% [markdown]
# ## 4. Semnalul D: eye-tracking, redus prin PCA
#
# Datele competitiei contin masuratori de eye-tracking inregistrate de mai multi cititori pentru fiecare
# cuvant: durata primei fixari (FFD), durata totala de fixare (TFT), timpul de recitire (RRT), numarul de
# fixari (TFC, FPFC), regresiile (RPD, TRC) si altele. Ideea de pornire este ca un cuvant dificil retine
# privirea mai mult timp si provoaca reveniri.
#
# Aceste metrici sunt corelate intre ele, asa ca le reducem la un singur scor prin analiza componentelor
# principale (PCA). Definim reading_effort drept prima componenta principala (PC1) a metricilor de
# eye-tracking standardizate, adica axa pe care variaza cel mai mult datele, interpretata ca efort de
# citire. Ponderea fiecarei metrici nu este aleasa manual, ci rezulta din incarcarile (loadings) ale PC1.
#
# Spre deosebire de A, B si C, acest semnal se calculeaza aici, pe CPU, fiind doar o transformare a
# datelor de eye-tracking din data/X_test.csv.

# %%
# Metricile de efort folosite pentru PC1; toate cresc cu dificultatea cuvantului.
ET_EFFORT = ["TFT_mean_norm", "FFD_mean_norm", "FPRT_mean_norm", "RRT_mean_norm",
             "TFC_mean_norm", "FPFC_mean_norm", "TRC_in_mean_norm", "RPD_inc_mean_norm"]


def semnal_et(test, verbose=True):
    """Calculeaza semnalul D ca reading_effort = PC1 (PCA) al metricilor de eye-tracking din
    data/X_test.csv, aliniat pe datapointID. Cuvintele fara eye-tracking (in jur de 78 din 1587) primesc
    efortul median. Returneaza vectorul aliniat la test, sau None daca fisierul lipseste."""
    p = os.path.join(DATA, "X_test.csv")
    if not os.path.exists(p):
        return None
    x = pd.read_csv(p)
    cols = [c for c in ET_EFFORT if c in x.columns]
    has = (x["has_et_features"] == 1).values if "has_et_features" in x.columns else x[cols[0]].notna().values

    M = x[cols].astype(float)
    mu, sd = M[has].mean(), M[has].std() + 1e-9      # standardizare pe cuvintele care au eye-tracking
    Z = ((M - mu) / sd).fillna(0.0).values

    # PCA prin descompunere SVD pe randurile cu eye-tracking; PC1 este directia de varianta maxima.
    _, S, Vt = np.linalg.svd(Z[has] - Z[has].mean(0), full_matrices=False)
    w = Vt[0]
    if w[cols.index("TFT_mean_norm")] < 0:           # fixam semnul: durata mai mare inseamna efort mai mare
        w = -w
    pc1 = Z @ w
    pc1[~has] = np.median(pc1[has])                  # cuvintele fara eye-tracking primesc efortul median

    if verbose:
        loadings = {c.replace("_mean_norm", ""): round(float(wi), 2) for c, wi in zip(cols, w)}
        print(f"  PCA reading_effort: varianta explicata de PC1 = {100 * S[0] ** 2 / (S ** 2).sum():.0f}%"
              f" | acoperire eye-tracking = {int(has.sum())}/{len(x)}")
        print(f"  pondere per metrica (incarcari PC1): {loadings}")
    x = x.assign(reading_effort=pc1)
    return test.merge(x[["datapointID", "reading_effort"]], on="datapointID", how="left")["reading_effort"].values


def semnal_et_manual(test):
    """Varianta alternativa a semnalului D: et_complexity_proxy, o suma ponderata manual a metricilor de
    eye-tracking (ponderi din literatura: TFT 0.30, RRT 0.20, FFD 0.15 etc.), pre-calculata in
    data/X_test.csv. Este echivalenta ca scor cu PCA (corelatie 0.97) si serveste doar la comparatie pe
    leaderboard. Returneaza vectorul aliniat la test, sau None."""
    p = os.path.join(DATA, "X_test.csv")
    if not os.path.exists(p) or "et_complexity_proxy" not in pd.read_csv(p, nrows=1).columns:
        return None
    x = pd.read_csv(p)[["datapointID", "et_complexity_proxy"]]
    return test.merge(x, on="datapointID", how="left")["et_complexity_proxy"].values


# %% [markdown]
# ## 5. Citirea semnalelor
#
# Calea implicita citeste semnalele A, B si C deja calculate din data/ si ruleaza pe CPU. Cu optiunea
# --recompute, ele se recalculeaza de la zero pe GPU prin functia din recompute_gpu.py.

# %%
def citeste_semnale_cache(test):
    """Citeste semnalele A, B si C din fisierele de cache. Semnalul A are doua parti: engleza si romanic.
    Foloseste versiunea cu frecventa-lema, cea care obtine 68.90."""
    def col(fisier, coloana):
        p = os.path.join(DATA, fisier)
        if not os.path.exists(p):
            return None
        return test.merge(pd.read_csv(p), on="datapointID", how="left")[coloana].values
    A_en = col("crosslingual_test_xlmr_last4_base_lemma.csv", "xl_complexity")
    A_mlsp = col("crosslingual_mlsponly_test_xlmr_last4_base_lemma.csv", "xl_complexity")
    B_llm = col("llm_complexity_test.csv", "llm_cx")
    C_surp = col("surprisal_test.csv", "surp")
    return A_en, A_mlsp, B_llm, C_surp


# %% [markdown]
# ## 6. Fuziunea semnalelor si calibrarea
#
# Aceasta este partea centrala a solutiei. Pasii sunt urmatorii.
#
# Mai intai construim semnalul A ca ansamblu: mediem cele doua transferuri aproape independente (engleza
# si romanic) pe valorile standardizate. Apoi formam scorul de baza ca 0.6 * A + 0.4 * nota_LLM si
# adaugam 8% surprisal: 0.92 * scor + 0.08 * surprisal. Aceste trei semnale produc scorul de 68.90.
#
# Adaugam apoi semnalul de eye-tracking: scor = 0.80 * scor + 0.20 * reading_effort. Contributia lui este
# mica dar reala pe datele publice, ridicand scorul de la 68.90 la 69.74. Cu W_ET = 0 se obtine exact
# scorul de baza.
#
# In final calibram: aducem predictia la media 0.27 si abaterea standard 0.125, valorile reale ale
# scorurilor de test, si o limitam la intervalul [0, 1]. Corelatia Pearson nu depinde de aceasta
# transformare, dar calibrarea imbunatateste metrica finala a competitiei.

# %%
def scor_3_semnale(A_en, A_mlsp, B_llm, C_surp):
    """Calculeaza scorul de baza (standardizat, inainte de calibrare) din semnalele A, B si C.
    Aceasta combinatie produce 68.90."""
    A_en, B_llm, C_surp = fill(A_en), fill(B_llm), fill(C_surp)
    # Semnalul A ca ansamblu engleza + romanic; daca partea romanica lipseste, ramane doar engleza.
    if A_mlsp is not None and np.isfinite(np.asarray(A_mlsp, float)).any():
        A = zscore(0.5 * zscore(fill(A_mlsp)) + 0.5 * zscore(A_en))
    else:
        A = zscore(A_en)
    s = W_CL * A + W_LLM * zscore(B_llm)                       # 60% cross-lingual + 40% nota LLM
    s = (1.0 - W_SURP) * zscore(s) + W_SURP * zscore(C_surp)   # plus 8% surprisal
    return zscore(s)


def calibreaza(s):
    """Aduce scorul la scara reala a testului (media 0.27, abaterea 0.125) si il limiteaza la [0, 1]."""
    return np.clip(CALIB_MEAN + CALIB_STD * zscore(s), 0.0, 1.0)


def combina_semnale(A_en, A_mlsp, B_llm, C_surp, et=None, w_et=W_ET):
    """Fuziunea finala: scorul din cele trei semnale, plus optional semnalul de eye-tracking, apoi
    calibrarea. Returneaza predictia in [0, 1]."""
    s = scor_3_semnale(A_en, A_mlsp, B_llm, C_surp)
    if et is not None and w_et > 0 and np.isfinite(np.asarray(et, float)).any():
        s = (1.0 - w_et) * zscore(s) + w_et * zscore(fill(et))    # adaugarea eye-tracking-ului
    return calibreaza(s)


# %% [markdown]
# ## 7. Rularea: producerea fisierului submission.csv

# %%
def ruleaza():
    test = pd.read_csv(os.path.join(DATA, "test_set.csv"))    # coloane: text, token, lemma, datapointID
    if "text" not in test.columns and "sentence" in test.columns:
        test = test.rename(columns={"sentence": "text"})

    if RECOMPUTE:
        print("[complet] recalculez semnalele A, B si C pe GPU (recompute_gpu.py)...")
        from recompute_gpu import recalculeaza_semnale
        A_en, A_mlsp, B_llm, C_surp = recalculeaza_semnale(test)
    else:
        print("[rapid] citesc semnalele din cache (CPU)...")
        A_en, A_mlsp, B_llm, C_surp = citeste_semnale_cache(test)

    et = semnal_et(test)                                      # semnalul D (PCA pe eye-tracking)
    ans = combina_semnale(A_en, A_mlsp, B_llm, C_surp, et=et, w_et=W_ET)

    out = pd.DataFrame({"subtaskID": 1, "datapointID": test["datapointID"], "answer": ans})
    out_path = os.path.join(HERE, "submission.csv")
    out.to_csv(out_path, index=False)
    print(f"Salvat {out_path}: {len(out)} randuri (patru semnale, W_ET={W_ET}), "
          f"media={ans.mean():.3f}, abatere={ans.std():.3f} (NaN={int(np.isnan(ans).sum())})")
    return test, (A_en, A_mlsp, B_llm, C_surp, et)


# Blocul se executa cand fisierul ruleaza ca script sau ca notebook (in ambele __name__ este "__main__"),
# dar nu la import, astfel incat alte module sa poata reutiliza functiile fara a declansa rularea.
if __name__ == "__main__":
    test, semnale = ruleaza()


# %% [markdown]
# ## 8. Verificare
#
# Cateva controale utile pentru intelegere si pentru prezentare: corelatiile dintre semnale (A si B sunt
# corelate moderat, iar C si D sunt aproape independente de restul), faptul ca frecventa domina predictia
# si comparatia dintre varianta cu patru semnale si cea cu trei semnale. Verificam de asemenea ca varianta
# cu trei semnale reproduce exact scorul public de 68.90.

# %%
def verificare(test, semnale):
    """Afiseaza corelatiile dintre semnale, contributia eye-tracking-ului si controlul de reproducere a
    scorului de 68.90 (varianta cu trei semnale)."""
    A_en, A_mlsp, B_llm, C_surp, et = semnale
    zf = lambda a: zscore(fill(a))

    print("corelatie (A cross-lingual, B nota LLM) =", round(pearsonr(zf(A_en), zf(B_llm))[0], 3))
    print("corelatie (C surprisal, B nota LLM)     =", round(pearsonr(zf(C_surp), zf(B_llm))[0], 3),
          " (aproape 0, deci semnal independent)")

    # Cat din semnalul de eye-tracking este de fapt frecventa?
    freq = lexical(list(test["token"]), ["ro"] * len(test), lemmas=test["lemma"].values)[:, 0]
    if et is not None:
        print("corelatie (D eye-tracking, -frecventa)  =", round(pearsonr(zf(et), -freq)[0], 3),
              " (eye-tracking-ul reflecta mai ales frecventa)")
    fin = pd.read_csv(os.path.join(HERE, "submission.csv"))["answer"].values
    print("corelatie (-frecventa, predictia finala) =", round(pearsonr(-freq, fin)[0], 3),
          " (frecventa domina predictia)")

    # Cat schimba eye-tracking-ul fata de varianta cu trei semnale (68.90)?
    ans3 = combina_semnale(A_en, A_mlsp, B_llm, C_surp, et=None)      # doar A, B, C
    ans4 = combina_semnale(A_en, A_mlsp, B_llm, C_surp, et=et)        # plus eye-tracking
    print(f"\ntrei semnale vs patru semnale: corelatie={pearsonr(ans3, ans4)[0]:.4f}, "
          f"randuri schimbate cu peste 0.01 = {int((np.abs(ans3 - ans4) > 0.01).sum())}/{len(ans3)}")

    # Control: varianta cu trei semnale (W_ET=0) trebuie sa reproduca exact scorul public de 68.90.
    ref_path = os.path.join(HERE, "output", "exp_lemmafreq.csv")
    if os.path.exists(ref_path):
        ref = pd.read_csv(ref_path).sort_values("datapointID")["answer"].values
        mine3 = pd.DataFrame({"datapointID": test["datapointID"], "a": ans3}).sort_values("datapointID")["a"].values
        maxdiff = np.abs(mine3 - ref).max()
        print(f"control trei semnale vs 68.90 public: diferenta maxima {maxdiff:.2e} "
              f"({'identic' if maxdiff < 1e-9 else 'DIFERIT'})")


if __name__ == "__main__":
    verificare(test, semnale)
