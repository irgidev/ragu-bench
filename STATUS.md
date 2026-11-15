# STATUS — ragu-bench

State sinkron antar sesi dalam proyek ini. Bagian Changelog append-only. Konflik ownership: pemilik menang, yang lain minta lewat catatan di Changelog dan tunggu sesi induk.

## Milestone

- M0 skeleton (repo + CI hijau + schema kontrak + README + STATUS): SELESAI (2026-11-15)
- M1 harness + 2 model pada smoke gold set v0: SIAP DIKERJAKAN JALUR-A (menunggu key + plafon untuk live run)
- M2 matriks penuh + router 3 strategi: BELUM (run besar menunggu plafon dari user)
- M3 report + rilis tag v0.1.0: BELUM

## Keputusan lokal

- Kandidat model awal (final diputuskan JALUR-A bersama user, dicatat ulang saat run): API murah = Gemini Flash class atau GPT-4o-mini class; API kuat = model tier atas satu vendor yang sama; lokal = Llama 3.1 8B instruct atau Qwen 2.5 7B via Ollama; LLM Indonesia (Sahabat-AI) bila akses weights/API ada, kalau tidak ada dicatat apa adanya di README.
- Adapter tunggal OpenAI-compatible (OpenAI, Gemini compatible endpoint, OpenRouter, Ollama punya endpoint yang sama) daripada satu SDK per vendor, kecuali ditemukan hambatan teknis; keputusan akhir dicatat di Changelog.
- Gold set v0 milik sesi induk P1 (`data/gold/gold_v0.json`). Saat P0 merilis gold set, copy file baru ke `data/gold/` dengan versi sendiri. DILARANG mengubah atau memicah file milik P0 di `ragu/`.
- Deps pinned saat pertama kali dipakai oleh jalur pemiliknya (Python 3.14 lokal dan CI), langsung di `pyproject.toml`.
- Skor groundedness v0 deterministik (heuristik, tanpa biaya API); metode ditulis di REPORT.md. LLM-judge hanya bila plafon biaya dari user mengizinkan.

## Ownership file

| Path | Pemilik |
|---|---|
| `src/bench/schemas.py`, `tests/test_schemas.py` | sesi induk P1 |
| `data/gold/**` | sesi induk P1 |
| `README.md`, `LICENSE`, `pyproject.toml` (struktur), `.github/`, `STATUS.md`, `prompts/SUB-*.md` | sesi induk P1 |
| `src/bench/models/**`, `src/bench/runner.py`, `tests/test_models_*.py`, `tests/test_runner_*.py`, `results/runs/**` | JALUR-A |
| `src/bench/metrics/**`, `src/bench/router/**`, `tests/test_metrics_*.py`, `tests/test_router_*.py`, `results/*.md`, `results/*.png`, `results/REPORT.md` | JALUR-B |

JALUR-B boleh mengimpor API publik milik JALUR-A tetapi tidak boleh mengubah file milik JALUR-A. Perubahan schema (`schemas.py`) diusulkan lewat catatan Changelog, diintegrasikan sesi induk.

## Catatan biaya API

- Belum ada run berbayar per 2026-11-15. Plafon benchmark ditunggu dari user sebelum run besar (M2). Estimasi smoke run M1 (2 model x 30 item, output pendek): jauh di bawah USD 1, aman terhadap rentang Rp 100-300 ribu yang disarankan dokumen proyek.
- Harga resmi tiap model dicatat dengan tanggal cek di `RunRecord.price_checked_on` dan tabel README.

## Changelog (append-only)

- 2026-11-15 sesi-P1-induk: M0 dibuat (skeleton, CI, schema kontrak, README, STATUS). Repo publik `irgidev/ragu-bench`, dua run CI pertama hijau (commit skeleton dan commit gold set).
- 2026-11-15 sesi-P1-induk: Smoke gold set `v0-smoke` dibangun di `data/gold/gold_v0.json` (30 item: 24 answer + 6 refuse) dari korpus D1: halaman resmi user-manual Mobile JKN bpjs-kesehatan.go.id (administrasi kepesertaan, iuran, lain-lain) dan UU No. 40/2004 via transkrip Wikisource (JDIH resmi hanya menyajikan PDF yang tak ter-fetch). Semua item answer memuat kutipan + URL + tanggal akses 2026-11-15; 4 test integritas gold set ikut CI. Builder: `data/gold/build_gold_v0.py`. Gold set P0 dicek read-only masih kosong.
- 2026-11-15 sesi-P1-induk: Pemecahan paralel sesuai PROMPT-INTI bagian 7. JALUR-A (harness + models + runner + results/runs) dan JALUR-B (metrics + router + results/*.md|png + REPORT). Sub-prompt: `prompts/SUB-P1-A-HARNESS-MODELS.md`, `prompts/SUB-P1-B-METRICS-ROUTER-REPORT.md`. Ownership per tabel di atas. Push hanya oleh sesi induk P1.
- 2026-11-15 sesi-P1-induk: Menunggu dari user: (1) API key LLM di `.env` untuk live smoke run M1, (2) plafon biaya benchmark sebelum run besar M2. Tanpa key, JALUR-A tetap jalan dengan mock tests.
