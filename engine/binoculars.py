# -*- coding: utf-8 -*-
"""Katman 1 — Binoculars (Hans ve ark., ICML 2024, arXiv:2401.12070).

Iki dil modeli kullanilir:
  observer  : temel model
  performer : ayni ailenin instruct surumu

Skor = log-perplexity / cross-perplexity.
DUSUK skor -> makine uretimi. Hicbir egitim gerektirmez; bu yuzden daha
once gorulmemis modellerin (yeni model surumleri) ciktisina da
genellesir — sinifladiricilarin en zayif oldugu nokta tam olarak budur.
"""
import os
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

OBSERVER = os.environ.get("BINO_OBSERVER", "Qwen/Qwen2.5-1.5B")
PERFORMER = os.environ.get("BINO_PERFORMER", "Qwen/Qwen2.5-1.5B-Instruct")
MAX_TOKENS = 512

_ce = torch.nn.CrossEntropyLoss(reduction="none")


def pick_device():
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


class Binoculars:
    _shared = None

    def __init__(self):
        self.device = pick_device()
        # MPS'te fp16 kararli calisiyor; CPU'da fp32 sart
        self.dtype = torch.float16 if self.device in ("mps", "cuda") else torch.float32
        self.tok = AutoTokenizer.from_pretrained(OBSERVER)
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token
        kw = dict(dtype=self.dtype, low_cpu_mem_usage=True)
        self.observer = AutoModelForCausalLM.from_pretrained(OBSERVER, **kw).to(self.device).eval()
        self.performer = AutoModelForCausalLM.from_pretrained(PERFORMER, **kw).to(self.device).eval()

    @classmethod
    def shared(cls):
        if cls._shared is None:
            cls._shared = cls()
        return cls._shared

    @classmethod
    def unload(cls):
        """Iki modeli de bellekten dusur (~6 GB geri verilir)."""
        from engine.memory import release
        if cls._shared is not None:
            inst, cls._shared = cls._shared, None
            inst.observer = inst.performer = inst.tok = None
            del inst
        release()

    @torch.inference_mode()
    def score(self, texts):
        """Metin listesi icin Binoculars skorlari (dusuk = AI)."""
        if isinstance(texts, str):
            texts = [texts]
        enc = self.tok(texts, return_tensors="pt", padding=True,
                       truncation=True, max_length=MAX_TOKENS).to(self.device)

        obs_logits = self.observer(**enc).logits
        perf_logits = self.performer(**enc).logits

        ppl = self._perplexity(enc, perf_logits)
        xppl = self._cross_perplexity(obs_logits, perf_logits, enc)
        return (ppl / np.maximum(xppl, 1e-6)).tolist()

    def _perplexity(self, enc, logits):
        """Hedef token'lar bilindigi icin burada tam dagilim gerekmez:
        gather ile yalnizca dogru token'in log olasiligi okunur."""
        labels = enc.input_ids[..., 1:]
        mask = enc.attention_mask[..., 1:].to(torch.float32)
        lg = logits[..., :-1, :]
        B = lg.shape[0]
        out = torch.empty(B, device=lg.device, dtype=torch.float32)
        for i in range(B):
            logp = F.log_softmax(lg[i], dim=-1, dtype=torch.float32)
            nll = -logp.gather(-1, labels[i].unsqueeze(-1)).squeeze(-1)
            out[i] = (nll * mask[i]).sum() / mask[i].sum().clamp(min=1)
            del logp, nll
        return out.cpu().numpy()

    def _cross_perplexity(self, p_logits, q_logits, enc):
        """Observer dagilimina gore performer'in beklenen surprizi.

        Qwen'in kelime dagarcigi 152k. Tum partiyi tek seferde float32'ye
        cevirmek 16x120x152k = ~1.2 GB gecici tensor demek; unified memory'de
        bu takas basincina ve buyuk yavaslamaya yol aciyordu. Bunun yerine
        dizi dizi, yerinde log_softmax ile hesapliyoruz.
        """
        mask = enc.attention_mask
        B = p_logits.shape[0]
        out = torch.empty(B, device=p_logits.device, dtype=torch.float32)
        for i in range(B):
            p = F.softmax(p_logits[i], dim=-1, dtype=torch.float32)
            logq = F.log_softmax(q_logits[i], dim=-1, dtype=torch.float32)
            ce = -(p * logq).sum(-1)                 # token basina capraz entropi
            m = mask[i].to(ce.dtype)
            out[i] = (ce * m).sum() / m.sum().clamp(min=1)
            del p, logq, ce
        return out.cpu().numpy()
