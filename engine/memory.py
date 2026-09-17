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


# ---------------------------------------------------------------------------
# Surec kilidi
#
# 16 Eylul'de tum sistem takasa girdi (takas 21.6 GB, yuk ortalamasi 20).
# Sebep tek bir surecin cok bellek yemesi degildi: olcum arka planda kosarken
# ayni anda ayri bir surecte hiz testi baslatildi. Her biri tek basina sigiyor,
# ikisi birden sigmiyor. Bu kilit, ikinci agir surecin sessizce baslamasini
# engeller.
# ---------------------------------------------------------------------------

import os

_LOCK_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "data", ".model_lock")


def _alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def free_gb():
    """Yeni bir surecin gercekten kullanabilecegi bellek (GB).

    macOS'ta "Pages free" yaniltici: isletim sistemi bos bellegi onbellek
    icin kullandigindan bu deger saglikli bir makinede de 0.1 GB gorunur.
    Geri kazanilabilir sayfalar (inactive + purgeable + speculative) de
    sayilmali, yoksa kontrol her zaman reddeder ve ise yaramaz.
    """
    try:
        import subprocess
        out = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=5).stdout
        size, vals = 4096, {}
        for line in out.splitlines():
            if "page size of" in line:
                size = int(line.split("page size of")[1].split()[0])
                continue
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            v = v.strip().rstrip(".")
            if v.isdigit():
                vals[k.strip()] = int(v)
        usable = (vals.get("Pages free", 0)
                  + vals.get("Pages speculative", 0)
                  + vals.get("Pages inactive", 0)
                  + vals.get("Pages purgeable", 0))
        return usable * size / (1024 ** 3)
    except Exception:
        return -1.0


def pressure():
    """Takas baskisi (GB). Yuksekse sistem zaten zorlaniyordur."""
    try:
        import re
        import subprocess
        out = subprocess.run(["sysctl", "-n", "vm.swapusage"],
                             capture_output=True, text=True, timeout=5).stdout
        m = re.search(r"used\s*=\s*([\d.]+)M", out)
        return float(m.group(1)) / 1024 if m else 0.0
    except Exception:
        return 0.0


def acquire(name="agir-is", need_gb=5.0, force=False):
    """Agir bir is baslatmadan once cagrilir.

    Baska bir agir is kosuyorsa ya da bos bellek yetersizse RuntimeError atar.
    force=True yalnizca kullanici acikca istediginde kullanilmalidir.
    """
    if os.path.exists(_LOCK_PATH):
        try:
            with open(_LOCK_PATH) as f:
                pid_s, owner = (f.read().strip().split("|", 1) + [""])[:2]
            pid = int(pid_s)
        except Exception:
            pid, owner = -1, "?"
        if pid > 0 and pid != os.getpid() and _alive(pid):
            raise RuntimeError(
                "Baska bir agir is zaten calisiyor: '%s' (pid %d).\n"
                "Iki model yigini ayni anda 16 GB'a sigmaz — sistem takasa girer.\n"
                "Once onun bitmesini bekleyin ya da 'kill %d' ile durdurun."
                % (owner, pid, pid))
        os.remove(_LOCK_PATH)          # sahipsiz kilit

    free, swap = free_gb(), pressure()
    if not force and 0 <= free < need_gb:
        raise RuntimeError(
            "Kullanilabilir bellek yetersiz: %.1f GB var, ~%.1f GB gerekiyor.\n"
            "Acik uygulamalari kapatin ya da bilgisayari yeniden baslatin."
            % (free, need_gb))
    # Takas TEK BASINA red sebebi degil: macOS takasi tembel bosaltir, bu
    # yuzden gecmis bir yuklenmeden kalan 10 GB'lik takas saglikli bir
    # sistemde de gorunur. Belirleyici olan kullanilabilir bellek. Takas
    # ancak bellek de sinirdayken (istenenin 1.5 katindan azken) anlamli bir
    # uyari sayilir — o zaman gercekten baski altindayiz demektir.
    if not force and swap > 8.0 and 0 <= free < need_gb * 1.5:
        raise RuntimeError(
            "Bellek sinirda (%.1f GB) ve sistem takas kullaniyor (%.1f GB).\n"
            "Simdi agir is baslatmak bilgisayari kilitleyebilir.\n"
            "Bilgisayari yeniden baslatin ya da acik uygulamalari kapatin."
            % (free, swap))

    os.makedirs(os.path.dirname(_LOCK_PATH), exist_ok=True)
    with open(_LOCK_PATH, "w") as f:
        f.write("%d|%s" % (os.getpid(), name))
    return True


def release_lock():
    try:
        if os.path.exists(_LOCK_PATH):
            with open(_LOCK_PATH) as f:
                pid = int(f.read().split("|")[0])
            if pid == os.getpid():
                os.remove(_LOCK_PATH)
    except Exception:
        pass
