"""Builds data/gold/gold_v0.json, the 30-item smoke gold set.

Every grounding quote below was extracted from the cited page on 2026-11-15:
BPJS Kesehatan's official Mobile JKN user-manual pages, and a Wikisource
transcription of UU No. 40/2004 (SJSN) because the official JDIH pages only
serve the law as a PDF. Re-verify quotes against the raw pages before relying
on them for judge-based scoring.
"""

from pathlib import Path

from bench.schemas import GoldItem, GoldSet, GroundingSource

ACCESS = "2026-11-15"
MANUAL = "https://bpjs-kesehatan.go.id/user-manual-mobile-jkn/"
ADMIN = "https://bpjs-kesehatan.go.id/user-manual-mobile-jkn/administrasi%20JKN.html"
IURAN = "https://bpjs-kesehatan.go.id/user-manual-mobile-jkn/iuran%20kepesertaan.html"
LAIN = "https://bpjs-kesehatan.go.id/user-manual-mobile-jkn/lain-lain.html"
UU = "https://id.wikisource.org/wiki/Undang-Undang_Nomor_40_Tahun_2004"


def grounding(url: str, *quotes: str) -> list[GroundingSource]:
    return [GroundingSource(url=url, accessed=ACCESS, quote=q) for q in quotes]


def answer(item_id: str, question: str, ideal: str, sources: list[GroundingSource], tags: list[str]) -> GoldItem:
    return GoldItem(
        id=item_id,
        question=question,
        ideal_answer=ideal,
        expected_behavior="answer",
        grounding=sources,
        tags=tags,
    )


def refuse(item_id: str, question: str, reason: str) -> GoldItem:
    return GoldItem(
        id=item_id,
        question=question,
        ideal_answer="",
        expected_behavior="refuse",
        refusal_reason=reason,
    )


ITEMS = [
    answer(
        "v0-bpjs-pendaftaran-peserta-baru",
        "Bagaimana cara mendaftar sebagai peserta baru JKN melalui aplikasi Mobile JKN?",
        "Buka Mobile JKN, tap menu pendaftaran peserta baru, setujui syarat dan ketentuan, "
        "masukkan nomor KK dan captcha, isi formulir lalu pilih kelas rawat. Setelah verifikasi "
        "OTP dan konfirmasi, pendaftaran berhasil dan informasi virtual account untuk pembayaran "
        "tagihan dikirim ke email terdaftar.",
        grounding(
            ADMIN,
            "Pada halaman utama, tap menu pendaftaran peserta baru",
            "Pendaftaran telah berhasil, anda diberikan informasi terkait virtual account untuk "
            "pembayaran tagihan peserta",
        ),
        ["kepesertaan"],
    ),
    answer(
        "v0-bpjs-syarat-tambah-anggota-keluarga",
        "Apa syarat utama bagi calon peserta yang akan ditambahkan sebagai anggota keluarga "
        "dalam kepesertaan JKN?",
        "Calon peserta yang akan ditambahkan harus sudah memiliki NIK/E-KTP.",
        grounding(ADMIN, "calon peserta yang akan ditambahkan harus sudah memiliki NIK/E-KTP."),
        ["kepesertaan"],
    ),
    answer(
        "v0-bpjs-bbl-hanya-pbi",
        "Apakah pendaftaran bayi baru lahir lewat Mobile JKN berlaku untuk semua segmen kepesertaan?",
        "Tidak. Pendaftaran bayi baru lahir (BBL) hanya berlaku untuk segmen kepesertaan "
        "PBI JK (PBI APBN).",
        grounding(ADMIN, "Pendaftaran Bayi Baru Lahir(BBL) hanya berlaku untuk segmen kepesertaan PBI JK (PBI APBN)"),
        ["kepesertaan"],
    ),
    answer(
        "v0-bpjs-cek-status-kepesertaan",
        "Bagaimana cara mengecek status kepesertaan JKN di Mobile JKN dan informasi apa saja yang tampil?",
        "Gunakan menu info peserta. Informasi yang tampil mencakup nama peserta, status kepesertaan, "
        "nomor JKN, tanggal lahir, dan tingkat fasilitas kesehatan.",
        grounding(
            ADMIN,
            "informasi mengenai nama peserta, status kepesertaan, No. JKN, Tanggal lahir, dan tingkat "
            "fasilitas kesehatan",
        ),
        ["kepesertaan"],
    ),
    answer(
        "v0-bpjs-aduan-otomatis-closed",
        "Apa yang terjadi pada pengaduan saya di Mobile JKN jika tidak dijawab oleh petugas?",
        "Setelah 5 hari tanpa balasan, status aduan otomatis berubah menjadi Closed.",
        grounding(ADMIN, "setelah 5 hari aduan akan otomatis berubah status menjadi Closed"),
        ["pengaduan"],
    ),
    answer(
        "v0-bpjs-autodebet-untuk-siapa",
        "Fitur autodebet iuran di Mobile JKN dikhususkan untuk peserta segmen apa?",
        "Fitur autodebet dikhususkan untuk Peserta Mandiri (PBPU) dan Bukan Pekerja (BP).",
        grounding(IURAN, "Fitur autodebet dikhususkan untuk Peserta Mandiri(PBPU)/Bukan Pekerja(BP)"),
        ["iuran"],
    ),
    answer(
        "v0-bpjs-kanal-autodebet",
        "Kanal apa saja yang bisa dipakai untuk mendaftar autodebet iuran JKN melalui Mobile JKN?",
        "Autodebet bank melalui BRI, Mandiri, BCA, dan BTN, serta autodebet non-bank melalui "
        "DOKU Wallet, Finpay (Mobile Cash), dan i-Saku.",
        grounding(IURAN, "Autodebet Bank: BRI, Mandiri, BCA, BTN", "Autodebet Non-Bank: DOKU Wallet, Finpay (Mobile Cash), i-Saku"),
        ["iuran"],
    ),
    answer(
        "v0-bpjs-rehab-syarat-tunggakan",
        "Peserta dengan tunggakan iuran berapa lama yang bisa mengikuti program cicilan REHAB?",
        "Peserta dengan tunggakan lebih dari 3 bulan, yaitu 4 sampai dengan 24 bulan, dapat "
        "mengikuti program cicilan REHAB.",
        grounding(IURAN, "tunggakan lebih dari 3 bulan (4 s.d 24 bulan)"),
        ["iuran"],
    ),
    answer(
        "v0-bpjs-maks-tunggakan-ditagih",
        "Berapa maksimal bulan tunggakan iuran yang dapat ditagihkan BPJS Kesehatan kepada peserta?",
        "Maksimal 24 bulan, mengacu pada Peraturan Presiden Nomor 82 Tahun 2018.",
        grounding(
            IURAN,
            "tunggakan yang ditagihkan oleh BPJS Kesehatan kepada Peserta adalah maksimal sebanyak 24 bulan",
        ),
        ["iuran"],
    ),
    answer(
        "v0-bpjs-iuran-berjalan-selama-tunggakan",
        "Apakah iuran tetap terbentuk ketika peserta masih memiliki tunggakan kurang dari 24 bulan?",
        "Ya. Iuran bulan berjalan tetap terbentuk dan menjadi penambah tunggakan.",
        grounding(IURAN, "iuran bulan berjalan akan tetap terbentuk dan menjadi penambah tunggakan"),
        ["iuran"],
    ),
    answer(
        "v0-bpjs-kondisi-pengalihan-segmen",
        "Kapan pengalihan segmen kepesertaan JKN dapat dilakukan?",
        "Pengalihan segmen hanya dapat dilakukan saat status peserta Nonaktif Aktif di Akhir Bulan.",
        grounding(
            ADMIN,
            "Pengalihan segmen Peserta hanya dapat dilakukan dalam kondisi status peserta "
            "Nonaktif Aktif di Akhir Bulan",
        ),
        ["kepesertaan", "iuran"],
    ),
    answer(
        "v0-bpjs-pindah-pbpu-tunggakan",
        "Apakah peserta dengan tunggakan iuran PBPU bisa langsung pindah segmen ke PBPU?",
        "Tidak bisa. Peserta harus melunasi tunggakan iuran PBPU-nya terlebih dahulu sebelum "
        "pindah segmen ke PBPU.",
        grounding(ADMIN, "tidak bisa pindah ke PBPU sebelum melunasi tunggakan iuran PBPU-nya"),
        ["iuran"],
    ),
    answer(
        "v0-bpjs-pd-pemda-minimal-1-tahun",
        "Kapan peserta PD Pemda dapat mengalihkan segmennya ke PBPU?",
        "Setelah minimal 1 tahun terdaftar di PD Pemda yang sama, kecuali domisili atau alamat "
        "Dati2 pada KTP sudah berbeda dengan Dati2 sesuai PKS PD Pemda.",
        grounding(
            ADMIN,
            "Untuk pengalihan segmen PD Pemda ke PBPU baru dapat dilakukan setelah minimal 1 tahun "
            "terdaftar di PD Pemda yang sama",
        ),
        ["iuran", "kepesertaan"],
    ),
    answer(
        "v0-bpjs-fktp-prajurit-tni-polri",
        "Bagaimana ketentuan perubahan FKTP satu keluarga bagi peserta Prajurit TNI dan Kepolisian RI Non PNS?",
        "Fitur perubahan satu keluarga tidak muncul untuk segmen tersebut, hanya anggota keluarga "
        "yang dapat mengubah FKTP-nya.",
        grounding(
            ADMIN,
            "tidak akan muncul pada user peserta dengan Segmen Prajurit TNI dan Kepolisan RI Non PNS",
            "Prajurit TNI Dan Kepolisian RI (Hanya Anggota Keluarga)",
        ),
        ["layanan"],
    ),
    answer(
        "v0-bpjs-kis-digital-kirim-email",
        "Bagaimana cara menampilkan dan mengirim KIS digital di Mobile JKN?",
        "Tap menu kartu peserta pada halaman utama untuk menampilkan KIS digital, lalu tap "
        "kirim email untuk mengirimkannya ke email pengguna.",
        grounding(ADMIN, "tap kirim email"),
        ["layanan"],
    ),
    answer(
        "v0-bpjs-ubah-nik-peruntukan",
        "Untuk siapa perubahan NIK melalui Mobile JKN diperuntukkan?",
        "Untuk peserta bayi baru lahir yang NIK-nya sudah terdaftar pada Dukcapil.",
        grounding(
            ADMIN,
            "Perubahan NIK diperuntukan untuk peserta bayi baru lahir dengan NIK yang sudah "
            "terdaftar pada Dukcapil.",
        ),
        ["kepesertaan"],
    ),
    answer(
        "v0-bpjs-menu-faq-mobile-jkn",
        "Di mana peserta bisa menemukan kumpulan FAQ resmi JKN di aplikasi Mobile JKN?",
        "Pada menu FAQ di bagian bawah aplikasi, yang memuat kumpulan pertanyaan dari peserta "
        "jaminan kesehatan beserta jawabannya.",
        grounding(
            LAIN,
            "kumpulan pertanyaan dari peserta jaminan kesehatan",
            "Tap menu FAQ yang ada pada menu bagian bawah",
        ),
        ["layanan"],
    ),
    answer(
        "v0-uu-definisi-jaminan-sosial",
        "Apa definisi jaminan sosial menurut UU Sistem Jaminan Sosial Nasional?",
        "Jaminan sosial adalah salah satu bentuk perlindungan sosial untuk menjamin seluruh rakyat "
        "agar dapat memenuhi kebutuhan dasar hidupnya yang layak (Pasal 1 angka 1).",
        grounding(
            UU,
            "salah satu bentuk perlindungan sosial untuk menjamin seluruh rakyat agar dapat memenuhi "
            "kebutuhan dasar hidupnya yang layak",
        ),
        ["regulasi"],
    ),
    answer(
        "v0-uu-tujuan-sjsn",
        "Apa tujuan Sistem Jaminan Sosial Nasional menurut UU SJSN?",
        "Memberikan jaminan terpenuhinya kebutuhan dasar hidup yang layak bagi setiap peserta "
        "dan atau anggota keluarganya (Pasal 3).",
        grounding(
            UU,
            "memberikan jaminan terpenuhinya kebutuhan dasar hidup yang layak bagi setiap peserta "
            "dan/atau anggota keluarganya",
        ),
        ["regulasi"],
    ),
    answer(
        "v0-uu-asas-penyelenggaraan",
        "Atas asas apa jaminan sosial diselenggarakan menurut UU SJSN?",
        "Asas kemanusiaan, asas manfaat, dan asas keadilan sosial bagi seluruh rakyat Indonesia "
        "(Pasal 2).",
        grounding(UU, "asas kemanusiaan, asas manfaat, dan asas keadilan sosial bagi seluruh rakyat Indonesia"),
        ["regulasi"],
    ),
    answer(
        "v0-uu-prinsip-penyelenggaraan",
        "Sebutkan prinsip penyelenggaraan jaminan sosial menurut UU SJSN.",
        "Prinsip kegotong-royongan, nirlaba, keterbukaan, kehati-hatian, akuntabilitas, dan "
        "portabilitas, antara lain sebagaimana diatur Pasal 4.",
        grounding(UU, "kegotong-royongan; nirlaba; keterbukaan; kehati-hatian; akuntabilitas; portabilitas"),
        ["regulasi"],
    ),
    answer(
        "v0-uu-lima-jenis-program",
        "Apa saja lima jenis program jaminan sosial menurut UU SJSN?",
        "Jaminan kesehatan, jaminan kecelakaan kerja, jaminan hari tua, jaminan pensiun, dan "
        "jaminan kematian (Pasal 18).",
        grounding(
            UU,
            "jaminan kesehatan; jaminan kecelakaan kerja; jaminan hari tua; jaminan pensiun; dan jaminan kematian",
        ),
        ["regulasi"],
    ),
    answer(
        "v0-uu-prinsip-jaminan-kesehatan",
        "Berdasarkan prinsip apa jaminan kesehatan diselenggarakan secara nasional?",
        "Berdasarkan prinsip asuransi sosial dan prinsip ekuitas (Pasal 19 ayat 1).",
        grounding(
            UU,
            "Jaminan kesehatan diselenggarakan secara nasional berdasarkan prinsip asuransi sosial "
            "dan prinsip ekuitas",
        ),
        ["regulasi"],
    ),
    answer(
        "v0-uu-bpjs-dibentuk-undang-undang",
        "Bagaimana ketentuan pembentukan Badan Penyelenggara Jaminan Sosial menurut UU SJSN?",
        "Badan Penyelenggara Jaminan Sosial harus dibentuk dengan Undang-Undang (Pasal 5 ayat 1).",
        grounding(UU, "Badan Penyelenggara Jaminan Sosial harus dibentuk dengan Undang-Undang."),
        ["regulasi"],
    ),
    refuse(
        "v0-rf-kurs-dollar-hari-ini",
        "Berapa kurs rupiah terhadap dolar AS hari ini?",
        "Informasi kurs mata uang harian berada di luar korpus (panduan resmi Mobile JKN dan "
        "UU SJSN). Model yang benar menolak menjawab dan mengarahkan ke sumber kurs terkini.",
    ),
    refuse(
        "v0-rf-klaim-asuransi-jiwa-swasta",
        "Bagaimana cara mengajukan klaim asuransi jiwa pada perusahaan asuransi swasta?",
        "Produk asuransi jiwa swasta di luar cakupan korpus yang hanya memuat JKN/BPJS Kesehatan "
        "dan UU SJSN, sehingga harus dijawab dengan refusal.",
    ),
    refuse(
        "v0-rf-penemu-vaksin-polio",
        "Siapa penemu vaksin polio?",
        "Pertanyaan sejarah sains tidak terjawab oleh korpus. Menjawab dari pengetahuan umum "
        "tanpa grounding adalah perilaku yang dianggap salah pada item ini.",
    ),
    refuse(
        "v0-rf-cara-buat-aplikasi-android",
        "Bagaimana cara membuat aplikasi Android dengan Kotlin?",
        "Topik pemrograman di luar korpus. Model yang benar menolak menjawab dan mengarahkan "
        "ke dokumentasi teknis.",
    ),
    refuse(
        "v0-rf-isi-lengkap-uu-24-2011",
        "Sebutkan isi lengkap pasal per pasal UU Nomor 24 Tahun 2011 tentang BPJS.",
        "Teks UU 24/2011 tidak termasuk dalam korpus (korpus hanya memuat UU 40/2004). "
        "Near-miss regulasi terkait yang wajib dijawab dengan refusal.",
    ),
    refuse(
        "v0-rf-biaya-berobat-rs-swasta",
        "Berapa kisaran biaya berobat di rumah sakit swasta tanpa JKN?",
        "Tarif rumah sakit swasta di luar korpus. Model yang benar menolak dan mengarahkan "
        "ke rumah sakit terkait.",
    ),
]

DESCRIPTION = (
    "Smoke gold set v0: 30 items (24 answer, 6 refuse) over BPJS Kesehatan's official Mobile JKN "
    "user-manual pages and UU No. 40/2004 (SJSN, via Wikisource transcription). Built by the "
    "ragu-bench parent session on 2026-11-15 while the ragu (P0) gold set is not yet released; "
    "migrate to the P0 gold set once published. Quotes were extracted from the cited pages on the "
    "access date recorded per source."
)


def main() -> None:
    gold_set = GoldSet(
        version="v0-smoke",
        generated_at=ACCESS,
        description=DESCRIPTION,
        items=ITEMS,
    )
    gold_set.validate()
    target = Path(__file__).parent / "gold_v0.json"
    gold_set.save(target)
    n_answer = sum(1 for item in ITEMS if item.expected_behavior == "answer")
    n_refuse = sum(1 for item in ITEMS if item.expected_behavior == "refuse")
    print(f"saved {target} ({n_answer} answer, {n_refuse} refuse)")


if __name__ == "__main__":
    main()
