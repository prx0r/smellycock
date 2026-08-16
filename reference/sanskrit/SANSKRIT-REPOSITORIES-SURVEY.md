# SANSKRIT TEXT REPOSITORIES — the source survey

*2026-08-15 · imported from the patalacheckpoints research lane. A survey of online libraries, archives,
and collections of (mostly untranslated) Sanskrit works — for the acquisition/ingestion pipeline: where to
bulk-download sources, which are authoritative/citable, and their access + format + license.*

---

## EXECUTIVE SUMMARY
Dozens of Sanskrit text repositories range from large national libraries to volunteer-run collections.
- **Open bulk sources:** Muktabodha (3,000+ texts, 570+ e-texts, Kashmir Śaiva/Tantra), GRETIL
  (thousands of Unicode e-texts), Digital Library of India mirrors, Internet Archive, Google Books.
- **Authoritative/citable:** Muktabodha, IFP/EFEO, IGNCA/ASI, Central Sanskrit Univ., Cambridge, Asiatic
  Society, Sanskrit Library (Brown).
- **Most globally accessible; some Indian servers have limited hours.**

## TOP REPOSITORIES (the ones that matter for ingestion)
| Repo | Custodian | Scope | Size | Format | Access | Authority |
|---|---|---|---|---|---|---|
| **Muktabodha** | Muktabodha Inst. | Kashmir Śaivism, Śākta, Tantra, Yoga, Veda | ~3,000 texts; 570+ e-texts | PDF, TEI, HTML | Open (BY-NC) | **Very high** (IFP/UNESCO) |
| **GRETIL** | Göttingen | Sanskrit/Pali/Prakrit e-texts | thousands | TXT (Unicode) | Open | high (archival) |
| **IFP Manuscripts** | French Inst. Pondicherry | **Śaiva-Agama** corpus | ~10,000 codices | JPG, PDF | catalog open, images on request | **Very high** (UNESCO MoW) |
| **DLI mirrors** (dli.sanskritdictionary, OUDL) | IIIT-H/Osmania | scanned Sanskrit books | 10^5+ pages | TIFF/PDF | Open | moderate (scanned) |
| **Internet Archive** | IA | digital books incl. Sanskrit | thousands | PDF/DJVU/TXT | Open | high |
| **Sanskrit Library** (Brown) | Brown consortium | classical texts, morphologically tagged | 131 online | Unicode | Open | high (linguistic) |
| **IGNCA/ASI** | India govt | Indology books | 2,000+ | PDF | Open | high |
| **Granth Sañjīvanī** | Asiatic Soc. Mumbai | rare books + manuscripts | 2,000+ manuscripts | PDF/JPG | Open | very high |
| **Central Sanskrit Univ.** | India govt | Purāṇas, grammar, literature | 100+ titles | PDF | Open | high |

## BEST SOURCES BY USE
- **Bulk download (ingestion):** Internet Archive, DLI/OUDL mirrors, Muktabodha, IFP (via request),
  GRETIL, Central Sanskrit Univ.
- **Scholarly citation:** Muktabodha, IFP/EFEO, IGNCA/ASI, CSU, Sanskrit Library (Brown), Cambridge.
- **Raw e-texts:** GRETIL, GitHub `sanskrit-texts`/raw_etexts.

## NOTES FOR THE INGESTION PIPELINE
- **License:** most are non-commercial (CC BY-NC-SA) or public domain — the ingest adapters must respect
  the rights firewall (AXIOM 9).
- **OCR:** DLI/Archive scans are image-based (variable OCR quality) → the OCR integrator (S3) applies.
- **Verse recovery:** GRETIL + Muktabodha TEI e-texts are the clean source for `harvest_to_factory`
  (the P0 verse-recovery path) — clean Unicode verses, not scans.
- **The sivaqueue** (100 works) sources map to these: GRETIL/Muktabodha for the Śaiva/Tantra corpus.

*Reference: the full per-repo detail (metadata, digitization, notable contents) is in the upstream
`research/SANSKRIT-REPOSITORIES-SURVEY.md`; this is the ingestion-relevant extract.*
