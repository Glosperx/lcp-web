# E1: debitul embedding-ului, masurat

XLM-R base, cfg last4, float32, 200 de tinte MLSP alese aleator (seed 42).
Total treceri E1: 5624 MLSP + 8423 EN = 14047. Niciun cache `.npy` inainte.

| device | 200 itemi | itemi/s | E1 complet, estimat |
|---|---|---|---|
| mps | 2.7s | 74.31 | 3.2 min |
| cpu | 3.9s | 51.72 | 4.5 min |

Raport mps/cpu: 1.44x
