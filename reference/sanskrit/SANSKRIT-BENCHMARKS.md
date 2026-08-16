# SANSKRIT LLM BENCHMARKS — what exists, which models are best, how it's measured

*2026-08-15 · imported from the patalacheckpoints research lane. Verified research (live fetches to
arXiv/GitHub/HuggingFace/ACL) on the Sanskrit-specific benchmark landscape. Answers: which models are
known-good at Sanskrit, what tests prove it, and what gold data is downloadable. This grounds our own
model-evaluation + the science lab.*

---

## 1. THE HEADLINE (which models are best at Sanskrit)

**IndicParam** (arXiv 2512.00333) is the ONLY verified 20-model LLM leaderboard that isolates Sanskrit.
Zero-shot MCQ accuracy on 13,207 UGC-NET-derived questions:

| Model | Sanskrit % | Sanskrit–English % |
|---|---|---|
| **Gemini-2.5** | **72.4** | **80.3** |
| GPT-5 | 54.8 | 64.6 |
| DeepSeek-3.2 | 51.3 | 61.4 |
| Claude-4.5 | 47.8 | 58.1 |
| Llama-4-Scout (open) | 44.0 | 48.7 |
| Llama-3.3-70B (open) | 41.7 | 51.6 |
| gpt-oss-120b (open) | 40.2 | 48.1 |
| Qwen3-32B | 39.2 | 48.6 |
| small models (<8B) | 28–34 | 28–35 |

**Key takeaways:**
- **Gemini-2.5 is the clear Sanskrit leader** (72.4%, 80.3% on Sa–En code-mixed).
- Best open-weights: **Llama-4-Scout 44%**.
- **Small models are weak at Sanskrit** (28–34%) — relevant for cheap/free small-model routing.
- Reproducible: HF `bharatgenai/IndicParam`, GitHub `ayushbits/IndicParam`.

## 2. SANSKRIT TRANSLATION BENCHMARKS (the "how good at translating" number)

| Benchmark | What | Metric | Gold | Best result | Repo |
|---|---|---|---|---|---|
| **Sāmayik** (2305.14004) | En↔Sa contemporary prose MT | BLEU, chrF | ~53k parallel | IndicBART BLEU 27.25 | `ayushbits/Saamayik` |
| **Itihāsa** (2106.03269) | classical śloka Sa→En MT | BLEU | 93k ślokas (Rāmāyaṇa/Mahābhārata) | SOTA "perform poorly" (hard) | `rahular/itihasa` |
| **MITRA** (2601.06400) | Sa/Pāli/Buddhist → En | — | 1.74M pairs | Gemma-2-MITRA-MT SOTA | — |

**Methodology:** BLEU (word) + chrF (character — Sanskrit is morphologically rich, 1,400+ inflections).
**No public LLM-vs-LLM Sanskrit translation leaderboard exists — that's the gap our benchmark can fill.**

## 3. OTHER SANSKRIT RESOURCES
| Resource | What | Type |
|---|---|---|
| **Naamah** (2604.26456) | 102,942-sentence Sanskrit NER | NER eval |
| **Vidyut** (ambuda-org/vidyut) | Sanskrit NLP toolkit (morphology, sandhi, meter) | analyzer |
| **Sanskrit Heritage** | Sa–Fr dictionary + morphological segmenter | tool/gold |
| **DCS** (OliverHellwig) | annotated Sanskrit corpus | gold corpus |
| **Token-efficiency** (2601.06142) | Sanskrit ≈2× fewer tokens than English | cost study |

**Notable absence:** IndicGLUE + IndicXTREME exclude Sanskrit from their reported results.

## 4. WHAT THIS MEANS FOR OUR WORK
1. **Gemini-2.5 is the quality ceiling** on general Sanskrit; for *translation*, no public LLM leaderboard
   exists — our benchmark is the opening.
2. **The gold data is downloadable** (Sāmayik + Itihāsa on HF) — benchmark any model with BLEU/chrF or
   LLM-as-judge.
3. **Model choice matters a lot** — flash-class (small) models score 28-34% vs Gemini's 72%. The
   projector's "is flash's 3× saving worth the quality drop?" is exactly what a leaderboard decides.

## 5. VERIFIED SOURCES
- IndicParam: arXiv 2512.00333 · Sāmayik: 2305.14004 · Itihāsa: 2106.03269 · MITRA: 2601.06400 ·
  Naamah: 2604.26456 · Token-efficiency: 2601.06142 · IndicXTREME: 2212.05409 · IndicGLUE: ACL 2020.
