# -*- coding: utf-8 -*-
"""Model bellegini geri verme yardimcilari.

16 GB'lik bir makinede uc modeli ayni anda bellekte tutmak takasa yol aciyor
ve tum sistem yavasliyordu. Cozum modeli kucultmek DEGIL (dogruluk duserdi),
ayni anda kac modelin bellekte durdugunu kontrol etmek.
"""
import gc


def release():
    """Referansi kalmamis tensorleri ve MPS/CUDA onbellegini serbest birak."""
    gc.collect()
    try:
        import torch
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        pass


def usage_gb():
    """Bu surecin yaklasik bellek kullanimi (GB)."""
    try:
        import resource
        import sys
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return rss / (1024 ** 3) if sys.platform == "darwin" else rss / (1024 ** 2)
    except Exception:
        return 0.0
