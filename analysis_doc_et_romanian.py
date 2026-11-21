"""Eye-tracking gain on Romanian, for the documentation (11 Oct 2026).

Paired bootstrap over contexts (2,000 resamples, seed 0) of r(with eye-tracking) - r(without), on all
1,587 RoLCP labels (data/RoLCP.csv, column complexity). Predictions of the earlier Romanian-only pipeline:
output/et_pca_w20.csv (with eye-tracking, weight 0.20) and output/exp_lemmafreq.csv (without). Join on
(text_name, token, text) as in score_rolcp.py. Prints aggregates only. Output: output/doc_et_romanian.txt."""
import csv, numpy as np
from collections import defaultdict
R='/Users/alexandrucojoaca/Documents/GitHub/ia-sahistii/'
norm=lambda s:(s or '').strip()
def pred(f): return {int(r['datapointID']):float(r['answer']) for r in csv.DictReader(open(R+f))}
pw, p0 = pred('output/et_pca_w20.csv'), pred('output/exp_lemmafreq.csv')
test={int(r['datapointID']):(norm(r['text_name']),norm(r['token']),norm(r['text'])) for r in csv.DictReader(open(R+'data/test_set.csv'))}
full={}
for r in csv.DictReader(open(R+'data/RoLCP.csv')):
    c=norm(r.get('complexity'))
    if c: full[(norm(r['text_name']),norm(r['token']),norm(r['text']))]=float(c)
ids=[d for d in test if test[d] in full]
print('joined', len(ids), 'of', len(test))
a=np.array([pw[d] for d in ids]); b=np.array([p0[d] for d in ids]); y=np.array([full[test[d]] for d in ids])
ctx=np.array([test[d][2] for d in ids])
r=lambda p,yy: np.corrcoef(p,yy)[0,1]
print(f'r with ET {r(a,y):.4f}  without {r(b,y):.4f}  diff {r(a,y)-r(b,y):+.4f}')
u,inv=np.unique(ctx,return_inverse=True); groups=[np.flatnonzero(inv==k) for k in range(len(u))]
rng=np.random.default_rng(0); D=[]
for _ in range(2000):
    idx=np.concatenate([groups[k] for k in rng.integers(0,len(groups),len(groups))])
    D.append(r(a[idx],y[idx])-r(b[idx],y[idx]))
D=np.array(D); print(f'contexts {len(u)}  paired 95% CI [{np.percentile(D,2.5):+.4f}, {np.percentile(D,97.5):+.4f}]  P(>0) {np.mean(D>0):.1%}')
