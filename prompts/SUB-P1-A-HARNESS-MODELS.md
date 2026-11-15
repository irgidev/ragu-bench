# SUB-P1-A — JALUR-A `ragu-bench` (Model harness + runner)

## 0. Konteks dan bacaan wajib (berurutan, sebelum menulis apa pun)

Kamu adalah sesi JALUR-A di proyek `ragu-bench`, bekerja di bawah sesi induk P1. Baca penuh:

1. `C:\Documents\Desktop\Project\self\CONTEXT_TRANSFER.md`
2. `C:\Documents\Desktop\Project\self\prompts\PROMPT-INTI-P1-RAGU-BENCH.md`
3. `C:\Documents\Desktop\Project\self\ragu-bench\STATUS.md` (keputusan lokal + tabel ownership + catatan biaya)
4. `C:\Documents\Desktop\Project\self\ragu-bench\src\bench\schemas.py` (kontrak data lintas jalur)
5. `C:\Documents\Desktop\Project\self\ragu-bench\data\gold\README.md` dan `data\gold\gold_v0.json` (gold set v0, 30 item)
6. `C:\Documents\Desktop\Project\self\ragu-bench\prompts\SUB-P1-A-HARNESS-MODELS.md` (file ini)

Status proyek saat ini: M0 selesai (repo `irgidev/ragu-bench`, CI hijau, schema + gold v0 committed). Milestone berikutnya M1, lalu bagian M2 milikmu. Venv: `ragu-bench/.venv` dari Python 3.14 AppData (lihat bagian 6 CONTEXT_TRANSFER).

## 1. Ownership (file yang boleh kamu tulis, hanya ini)

- `src/bench/models/**` — adapter model OpenAI-compatible + profil kandidat
- `src/bench/runner.py` — runner gold set
- `tests/test_models_*.py`, `tests/test_runner_*.py`
- `results/runs/**` — keluaran run JSON (RunRecord)
- `pyproject.toml`, HANYA entri `[project.optional-dependencies].api` (dep adapter, pinned exact)
- Bagian Changelog `STATUS.md` (append-only)

DILARANG menyentuh: `src/bench/schemas.py` (usulkan perubahan lewat catatan Changelog), `src/bench/metrics/**`, `src/bench/router/**`, `data/gold/**`, `README.md`, `results/*.md`, `results/*.png`, `.github/`, file CONTEXT_TRANSFER.md, folder proyek lain (terutama `ragu/` milik P0), `github-profile/`.

## 2. Tugas M1 (harness + 2 model pada gold v0)

1. **Adapter tunggal OpenAI-compatible** (`src/bench/models/`): satu kelas dengan parameter `base_url`, `api_key`, `model`, `endpoint_region`. Harus jalan untuk OpenAI, Gemini compatible endpoint (`generativelanguage.googleapis.com/v1beta/openai/`), OpenRouter, dan Ollama lokal (`http://localhost:11434/v1`). Ukur TTFT dari streaming dan total latency per kueri; ambil token usage dari respons bila tersedia; flag `refused` dari heuristik teks jawaban (jawaban menyatakan tidak punya informasi / di luar cakupan). Dokumentasikan definisi heuristik refusal di docstring.
2. **Profil kandidat** (`src/bench/models/profiles.py`): tier murah API, tier kuat API, lokal Ollama (Llama 3.1 8B instruct atau Qwen 2.5 7B), LLM Indonesia (Sahabat-AI) bila akses ada. Nama model final kamu putuskan (sesuai PROMPT-INTI bagian 2) dan catat di Changelog. Kalau LLM Indonesia tidak memungkinkan baik API maupun weights lokal, catat apa adanya di Changelog agar induk menuliskannya di README. DILARANG mengarang hasil.
3. **Runner** (`src/bench/runner.py`): baca gold set (default `data/gold/gold_v0.json`, bisa override path untuk migrasi ke gold set P0 nanti), panggil model per item, tangani error per item (isi `error` di `ModelAnswer`, jangan matikan run), tulis `results/runs/<run_id>.json` via `RunRecord.save`. `run_id` memuat nama model + tanggal. Isi `endpoint_region`, harga resmi per 1M token input/output (USD) dan `price_checked_on` (tanggal cek halaman harga resmi).
4. **Tests tanpa jaringan**: mock transport untuk adapter dan runner (respons sintetis, kasus error, kasus refusal). CI harus hijau tanpa API key.
5. **Live smoke run M1**: 2 model pada gold v0, HANYA bila `.env` sudah berisi key DAN STATUS.md bagian "Catatan biaya API" mencatat plafon dari user. Setelah run selesai: commit `results/runs/*.json`, tulis catatan di Changelog agar JALUR-B merender leaderboard (DoD M1 "dua baris leaderboard terisi" dihitung JALUR-B dari run JSON-mu).

## 3. Tugas M2 (bagianmu)

Matriks penuh semua kandidat pada gold set aktif (v0 atau gold set P0 bila induk sudah men-copy-nya ke `data/gold/`) + run eskalasi router. Run eskalasi memakai policy dari `bench.router.policy` milik JALUR-B (import saja, jangan ubah filenya). Run besar (matriks penuh) WAJIB menunggu plafon biaya dari user tercatat di STATUS.md oleh induk. Estimasi biaya run tulis di Changelog SEBELUM menjalankan.

## 4. Aturan biaya dan API key

- Key hanya lewat `.env` (gitignored, contoh di `.env.example`). DILARANG menulis key di kode, commit, atau STATUS.md.
- Smoke run (≤ 2 model × 30 item, output pendek, estimasi < USD 1) boleh jalan bila key ada dan plafon sudah dicatat di STATUS.md.
- Kalau belum ada key/plafon: kerjakan adapter, runner, dan tests dengan mock sampai hijau, lalu lapor ke user bahwa live run menunggu key + plafon. Jangan berhenti total karena key.

## 5. Standar engineering

Artefak (kode, komentar, docstring, run metadata) Bahasa Inggris. Laporan ke user Bahasa Indonesia. Conventional Commits, commit kecil pada path milikmu. Deps pinned exact yang benar-benar terpasang di venv lokal (py3.14) dan CI tetap hijau. Ruff bersih, type hints, tanpa emoji, tanpa klaim tanpa pengukuran (aturan D9 CONTEXT_TRANSFER).

## 6. Yang dilarang keras

- `git push` dalam bentuk apa pun (push hanya oleh sesi induk P1). Commit lokal boleh.
- Mengubah gold set (`data/gold/**`) atau file milik P0 di `ragu/`. Bila gold set P0 sudah rilis, catat di Changelog dan tunggu induk men-copy-nya.
- Mengubah `schemas.py` tanpa persetujuan induk.

## 7. DoD JALUR-A

- pytest + ruff hijau lokal dan CI tanpa API key.
- Adapter dan runner jalan; live smoke run 2 model menghasilkan `results/runs/*.json` committed (bila key tersedia), dengan harga + tanggal cek terisi.
- Keputusan tercatat di Changelog STATUS.md: profil model final, heuristik refusal, kanal endpoint tiap model.
- Laporan ringkas Bahasa Indonesia ke user di akhir sesi.
