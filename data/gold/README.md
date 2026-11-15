# data/gold

Benchmark gold sets. The schema lives in `src/bench/schemas.py` (`GoldSet`, `GoldItem`, `GroundingSource`).

## v0-smoke (current)

`gold_v0.json`, 30 items (24 answer, 6 refuse), built on 2026-11-15 by this repo's parent session while the `ragu` (P0) project has not released its gold set yet.

Corpus (per the shared D1 decision): BPJS Kesehatan's official Mobile JKN user-manual pages and UU No. 40/2004 (SJSN).

| Source | URL | Accessed |
|---|---|---|
| Mobile JKN manual index | https://bpjs-kesehatan.go.id/user-manual-mobile-jkn/ | 2026-11-15 |
| Administrasi kepesertaan JKN | https://bpjs-kesehatan.go.id/user-manual-mobile-jkn/administrasi%20JKN.html | 2026-11-15 |
| Iuran kepesertaan JKN | https://bpjs-kesehatan.go.id/user-manual-mobile-jkn/iuran%20kepesertaan.html | 2026-11-15 |
| Lain-lain (FAQ menu, faskes locator) | https://bpjs-kesehatan.go.id/user-manual-mobile-jkn/lain-lain.html | 2026-11-15 |
| UU No. 40/2004 (Wikisource transcription; official JDIH serves it as PDF only) | https://id.wikisource.org/wiki/Undang-Undang_Nomor_40_Tahun_2004 | 2026-11-15 |

Notes:

- Every `answer` item carries at least one grounding quote with its URL and access date. Quotes were extracted from the fetched pages on the access date; re-verify against the raw page before using them for judge-based scoring.
- `refuse` items are deliberately outside the corpus (fx rates, private insurance, programming) or near-miss regulation (UU 24/2011). A correct model declines to answer from memory.
- Rebuild the JSON with `python data/gold/build_gold_v0.py` from the project venv. The script validates the set against the schema before writing.

## Migration to the P0 gold set

When `ragu/data/gold/` (P0) publishes its gold set, copy the released file into this directory under its own version name and switch the runner default. Never modify P0's files in place, and never mix item formats inside one version.
