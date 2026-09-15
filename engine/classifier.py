# -*- coding: utf-8 -*-
"""Katman 2 — Denetimli transformer siniflandiricilar.

Ingilizce : desklib/ai-text-detector-v1.01 (DeBERTa-v3-large, MIT, RAID lideri)
Turkce    : ads2009/turkish-ai-text-detector-* (BERTurk / ConvBERT)

Turkce modellerin model karti bos oldugu icin bunlar KOSULLU kullanilir:
eval/run_eval.py bunlari kendi test setimizde olcer, yetersizse
engine/calibration.json icinde devre disi birakilir.
"""
import os
import torch
import torch.nn as nn
from transformers import AutoConfig, AutoModel, AutoModelForSequenceClassification, AutoTokenizer

EN_MODEL = os.environ.get("EN_CLF", "desklib/ai-text-detector-v1.01")
TR_MODEL = os.environ.get("TR_CLF", "ads2009/turkish-ai-text-detector-berturk-v10")


def pick_device():
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


class _DesklibModel(nn.Module):
    """desklib model karti mimarisi: govde + mean pooling + tek cikisli linear."""

    def __init__(self, name):
        super().__init__()
        config = AutoConfig.from_pretrained(name)
        # Checkpoint anahtarlari "model.*" / "classifier.*" onekiyle kayitli.
        # from_pretrained bu oneki tanimadigi icin govde rastgele kalirdi;
        # bos govde kurup tam state_dict'i elle yukluyoruz.
        self.model = AutoModel.from_config(config)
        self.classifier = nn.Linear(config.hidden_size, 1)

    def forward(self, input_ids, attention_mask, return_pooled=False):
        hidden = self.model(input_ids, attention_mask=attention_mask)[0]
        mask = attention_mask.unsqueeze(-1).expand(hidden.size()).float()
        pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
        logits = self.classifier(pooled).squeeze(-1)
        return (logits, pooled) if return_pooled else logits


class Classifier:
    """Tek bir siniflandiriciyi sarar; p(AI) dondurur."""

    def __init__(self, name, kind="auto", ai_index=None, max_len=512):
        self.name, self.kind, self.max_len = name, kind, max_len
        self.device = pick_device()
        self.tok = AutoTokenizer.from_pretrained(name)

        if kind == "desklib":
            self.model = _DesklibModel(name)
            missing, unexpected = self.model.load_state_dict(
                self._load_state_dict(name), strict=False)
            critical = [k for k in missing if not k.endswith(".position_ids")]
            if critical:
                raise RuntimeError("desklib agirliklari eksik yuklendi: %s" % critical[:5])
            self.ai_index = None
        else:
            self.model = AutoModelForSequenceClassification.from_pretrained(name)
            self.ai_index = ai_index if ai_index is not None else self._guess_ai_index()

        # NOT: fp16 denendi ve geri alindi. DeBERTa-v3'un goreli konum
        # gomulerinde fp32 buffer'lar kaliyor; MPS matmul farkli dtype'lari
        # kabul etmeyip surecin tamamini dusuruyor. 0.85 GB kazanc icin
        # cokme riski alinmaz — bellek kazanci zaten faz faz yuklemeden geliyor.
        self.model.to(self.device).eval()

    def _load_state_dict(self, name):
        """Checkpoint'in tamamini (govde + siniflandirici kafasi) oku."""
        from huggingface_hub import hf_hub_download
        from safetensors.torch import load_file
        return load_file(hf_hub_download(name, "model.safetensors"))

    def _guess_ai_index(self):
        """id2label'dan AI sinifinin indeksini cikar; bulamazsa 1 varsay."""
        id2label = getattr(self.model.config, "id2label", {}) or {}
        for idx, label in id2label.items():
            if any(t in str(label).lower() for t in ("ai", "machine", "generated", "fake", "gpt", "yapay")):
                return int(idx)
        return 1 if len(id2label) >= 2 else 0

    @torch.inference_mode()
    def predict(self, texts, with_embeddings=False):
        """Metin listesi -> p(AI) listesi (0..1).

        with_embeddings=True ise (olasiliklar, gomuler) dondurur. Gomu ayni
        ileri gecisten alinir; Katman 4 icin ikinci bir model yuklenmez.
        """
        if isinstance(texts, str):
            texts = [texts]
        enc = self.tok(texts, return_tensors="pt", padding=True,
                       truncation=True, max_length=self.max_len).to(self.device)
        if self.kind == "desklib":
            logits, pooled = self.model(enc["input_ids"], enc["attention_mask"],
                                        return_pooled=True)
            probs = torch.sigmoid(logits.float()).cpu().tolist()
            if with_embeddings:
                return probs, pooled.float().cpu().numpy()
            return probs
        out = self.model(**enc, output_hidden_states=with_embeddings)
        probs = torch.softmax(out.logits.float(), dim=-1)[:, self.ai_index].cpu().tolist()
        if with_embeddings:
            hid = out.hidden_states[-1]
            m = enc["attention_mask"].unsqueeze(-1).expand(hid.size()).float()
            pooled = (hid * m).sum(1) / m.sum(1).clamp(min=1e-9)
            return probs, pooled.float().cpu().numpy()
        return probs


_cache = {}


def unload():
    """Yuklu tum siniflandiricilari bellekten dusur."""
    from engine.memory import release
    _cache.clear()
    release()


def get(lang):
    """Dil koduna gore siniflandirici dondur ('tr' | 'en'); yoksa None."""
    if lang in _cache:
        return _cache[lang]
    try:
        if lang == "en":
            clf = Classifier(EN_MODEL, kind="desklib", max_len=768)
        else:
            clf = Classifier(TR_MODEL, kind="auto", max_len=512)
    except Exception as e:
        print("[classifier] %s yuklenemedi: %s" % (lang, e))
        clf = None
    _cache[lang] = clf
    return clf
