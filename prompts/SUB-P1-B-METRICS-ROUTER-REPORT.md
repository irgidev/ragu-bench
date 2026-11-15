# SUB-P1-B — JALUR-B `ragu-bench` (Metrics + Router + Report)

## 0. Konteks dan bacaan wajib (berurutan, sebelum menulis apa pun)

Kamu adalah sesi JALUR-B di proyek `ragu-bench`, bekerja di bawah sesi induk P1. Baca penuh:

1. `C:\Documents\Desktop\Project\self\CONTEXT_TRANSFER.md`
2. `C:\Documents\Desktop\Project\self\prompts\PROMPT-INTI-P1-RAGU-BENCH.md`
3. `C:\Documents\Desktop\Project\self\ragu-bench\STATUS.md` (keputusan lokal + tabel ownership + catatan biaya)
4. `C:\Documents\Desktop\Project\self\ragu-bench\src\bench\schemas.py` (kontrak data lintas jalur)
5. `C:\Documents\Desktop\Project\self\ragu-bench\data\gold\README.md` dan `data\gold\gold_v0.json` (gold set v0, 30 item)
6. `C:\Documents\Desktop\Project\self\ragu-bench\prompts\SUB-P1-B-METRICS-ROUTER-REPORT.md` (file ini)
7. Contoh keluaran JALUR-A di `results/runs/*.json` bila sudah ada; kalau belum, kerjakan bagian 2 langkah 1-2 yang tidak membutuhkan run data.

Status proyek saat ini: M0 selesai (repo `irgidev/ragu-bench`, CI hijau, schema + gold v0 committed). Venv: `ragu-bench/.venv` dari Python 3.14 AppData (lihat bagian 6 CONTEXT_TRANSFER).

## 1. Ownership (file yang boleh kamu tulis, hanya ini)

- `src/bench/metrics/**` — scoring groundedness deterministik, refusal correctness, agregasi latensi/biaya
- `src/bench/router/**` — policy murah-dulu, sinyal eskalasi, simulasi 3 strategi dari run JSON
- `tests/test_metrics_*.py`, `tests/test_router_*.py`
- `results/*.md` (leaderboard, tabel strategi), `results/*.png` (grafik matplotlib), `results/REPORT.md`
- `pyproject.toml`, HANYA entri `[project.optional-dependencies].viz` (matplotlib, pinned exact saat dipakai)
- Bagian Changelog `STATUS.md` (append-only)

Boleh MENGIMPOR (bukan mengubah) API publik JALUR-A: `bench.models`, `bench.runner`. DILARANG menyentuh: `src/bench/schemas.py` (usulkan perubahan lewat catatan Changelog), `src/bench/models/**`, `src/bench/runner.py`, `data/gold/**`, `README.md`, `.github/`, `results/runs/**` (read-only untukmu), file CONTEXT_TRANSFER.md, folder proyek lain (terutama `ragu/` milik P0), `github-profile/`.

## 2. Tugas (M2, lalu M3)

1. **Metrics** (`src/bench/metrics/`):
   - Groundedness v0 DETERMINISTIK, tanpa biaya API: jawaban dinilai dari dukungan terhadap kutipan grounding (lexical/coverage heuristik pada `GoldItem.grounding`). Definisikan metode persisnya, tulis di docstring dan REPORT. Metode di-fixed SEBELUM scoring, jangan diutak-atik setelah melihat hasil (D9).
   - `refusal_correct`: gold `refuse` + model refused = benar; gold `answer` + refused = salah; dst. Sertakan penanganan item ber-`error`.
   - Agregasi per `RunRecord` (baca `results/runs/*.json`): quality/grounded accuracy, correct-refusal rate, p50/p95 latensi, biaya rata-rata per kueri dari `input_tokens × price_usd_per_1m_input` dst. Konversi IDR: catat kurs, sumber kurs, dan tanggalnya di REPORT. DILARANG mengarang kurs.
2. **Router** (`src/bench/router/`): policy murni `escalate(signals) -> bool` + unit tests tanpa jaringan. Sinyal keyakinan: self-check terstruktur (model murah menilai keyakinannya sendiri, hasilnya ada di run JSON JALUR-A) dan skor retrieval surrogate (mis. keyword overlap pertama-korpus; korpus lengkap bukan non-goal-mu, jangan bangun retrieval penuh). Simulasikan 3 strategi dari run data: murah-selalu, mahal-selalu, router (item ter-eskalasi memakai jawaban model kuat; biaya = iuran model murah + tambahan model kuat). Laporkan kualitas setara, % eskalasi, biaya relatif.
3. **Leaderboard + tabel strategi** (`results/*.md`): DIGENERATE dari run JSON oleh script committed (bukan diketik tangan), sehingga angka reproduksi dari `results/runs/`. Tabel per model dan per strategi dengan kolom sesuai PROMPT-INTI bagian 3, termasuk tanggal run, versi gold set, region endpoint.
4. **Grafik biaya-kualitas** (`results/*.png`, matplotlib): committed, digenerate script yang sama.
5. **`results/REPORT.md`** (Bahasa Inggris): rekomendasi "untuk use case X pakai model Y karena angka Z", metode scoring yang di-fixed, versi gold set, tanggal run, region, kurs yang dipakai, dan limitations (gold set 30 item smoke, heuristik v0, satu mesin satu waktu).
6. **M3**: setelah matriks dan router lengkap, finalisasi REPORT. Angka README final disuplai lewat `results/*.md` dan di-copy oleh sesi induk (README milik induk). Tag `v0.1.0` dibuat oleh induk.

## 3. Aturan biaya

Metrics heuristik v0 dan simulasi router dari run data TIDAK memakai API (gratis). Self-check tambahan atau LLM-judge menambah biaya: hanya bila plafon dari user tercatat di STATUS.md. Kalau tidak ada, catat di REPORT bahwa judge LLM tidak dipakai dan alasannya.

## 4. Standar engineering

Artefak Bahasa Inggris. Laporan ke user Bahasa Indonesia. Conventional Commits, commit kecil pada path milikmu. Deps pinned exact terpasang di venv lokal (py3.14), CI tetap hijau. Ruff bersih, type hints, tanpa emoji, tanpa angka karangan (D9): setiap angka di leaderboard/REPORT harus bisa dijesulkan ke `results/runs/*.json`.

## 5. Yang dilarang keras

- `git push` dalam bentuk apa pun (push hanya oleh sesi induk P1). Commit lokal boleh.
- Mengubah `results/runs/**`, gold set, atau file milik P0 di `ragu/`.
- Menuliskan angka benchmark sebelum run data ada. Tabel kosong boleh, tabel karangan tidak.

## 6. DoD JALUR-B

- pytest + ruff hijau lokal dan CI.
- Metrics + router + tests selesai (bisa dikerjakan tanpa menunggu run data).
- Leaderboard, tabel strategi, dan PNG digenerate dari run JSON (setelah JALUR-A menghasilkan run), REPORT.md terisi dengan rekomendasi tier berbasis angka.
- Keputusan tercatat di Changelog STATUS.md (metode groundedness, definisi sinyal eskalasi, kurs yang dipakai).
- Laporan ringkas Bahasa Indonesia ke user di akhir sesi.
