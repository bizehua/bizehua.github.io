# -*- coding: utf-8 -*-
"""生成 assets/data/cards-ms.json —— 应急处置卡的马来语对照"""
import io, json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "assets", "data", "cards-ms.json")

DATA = {
  "co": {
    "title": "Kebocoran CO & Keracunan Gas",
    "level": "Risiko Sangat Tinggi",
    "feature": [
      "Gas penukar (kaya CO) bocor melalui paip, injap mata, pembakar, rongga tanur dan lain-lain",
      "Bunyi “desis” atau bau gas di zon kebocoran; pekerja mengalami sakit kepala, loya, lesu, muntah",
      "Penggera CO tetap / mudah alih berbunyi (≥24ppm)"
    ],
    "steps": [
      "Jika kebocoran atau penggera berbunyi — hentikan kerja serta-merta, berpindah ke zon selamat di arah angin atas",
      "Laporkan kepada ketua pasukan, ketua kawasan & penyelaras; aktifkan pelan kecemasan, wujudkan zon larangan",
      "Dalam zon larangan: dilarang punca api, elektrik bukan kalis letupan & kenderaan lalu",
      "Jika ada mangsa keracunan: pakai SCBA sebelum masuk, pindahkan mangsa ke kawasan udara segar",
      "Pastikan saluran pernafasan mangsa terbuka & kekalkan suhu badan; jika berhenti nafas/denyut, lakukan CPR",
      "Pasukan pencegah gas / profesional memakai kelengkapan perlindungan untuk menutup kebocoran",
      "Cari punca, lakukan penggantian gas sehingga lulus sebelum sambung pengeluaran"
    ],
    "report": "Pekerja tapak → ketua pasukan → ketua kawasan → penyelaras / stesen pencegah gas (serentak hubungi talian kecemasan kilang)",
    "forbid": [
      "Dilarang guna telefon bimbit atau suis elektrik di lokasi kebocoran",
      "Dilarang masuk zon kebocoran untuk menyelamat tanpa SCBA",
      "Dilarang menguji kebocoran dengan api terbuka — guna penggera atau air sabun"
    ]
  },
  "heat": {
    "title": "Melecur Suhu Tinggi",
    "level": "Risiko Tinggi",
    "feature": [
      "Suhu permukaan badan tanur, paip gas buangan panas, penukar haba & mesin pengeluar melebihi 200℃",
      "Percikan kapur panas / abu panas, kebocoran paip wap",
      "Kemerahan setempat, lepuh, pengelupasan kulit"
    ],
    "steps": [
      "Menjauh serta-merta dari peralatan panas & wap bocor; panggil bantuan",
      "Tanggalkan pakaian yang terkena cecair panas (gunting bahagian melekat, jangan ditarik)",
      "Bilas luka dengan air sejuk mengalir selama 15–30 minit",
      "Tutup luka dengan kain bersih; jangan sapu sebarang ubat",
      "Jika melecur luas atau pada muka / saluran pernafasan — hantar ke hospital serta-merta",
      "Jika peralatan abnormal: hentikan, putus elektrik, gantung tanda, laporkan kepada ketua pasukan"
    ],
    "report": "Pekerja tapak → ketua pasukan → ketua kawasan (jika serius, hantar ke hospital & laporkan serentak)",
    "forbid": [
      "Dilarang sapu kicap, ubat gigi, ubat ungu dan lain-lain",
      "Dilarang memecahkan lepuh atau meletak ais pada luka",
      "Dilarang membersih bahan panas tanpa menghentikan mesin"
    ]
  },
  "confined": {
    "title": "Kemalangan Kerja Ruang Terhad",
    "level": "Risiko Sangat Tinggi",
    "feature": [
      "Ruang terhad: dalam rongga tanur, penapis elektrostatik / beg, serombong, corong abu, selongsong kipas",
      "Pekerja pengsan, tidak sedarkan diri, atau penggera gas menunjukkan melebihi had",
      "Risiko kekurangan oksigen, baki CO, baki haba & habuk"
    ],
    "steps": [
      "Pengawas hubungi bantuan serta-merta — dilarang masuk bersendirian untuk menyelamat",
      "Aktifkan pelan kecemasan; pasukan penyelamat pakai SCBA & tali keselamatan sebelum masuk",
      "Sediakan pengawas luar untuk pemantauan & hubungan; kekalkan komunikasi",
      "Pindahkan mangsa ke udara segar; nilaikan kesedaran, pernafasan & denyutan",
      "Jika berhenti nafas/denyut, lakukan CPR serta-merta & hubungi kakitangan perubatan",
      "Teruskan pengudaraan & ujian gas semasa operasi untuk elak kecederaan kedua",
      "Cari punca & baiki secara tertutup mengikut prinsip “Empat Tidak Lepas”"
    ],
    "report": "Pengawas → ketua pasukan → ketua kawasan → penyelaras / pasukan kecemasan kilang (hubungi talian kecemasan)",
    "forbid": [
      "Dilarang menyelamat secara membuta tuli & masuk tanpa alat pernafasan",
      "Dilarang masuk ruang terhad tanpa kelulusan, tanpa ujian gas, tanpa pengawas",
      "Dilarang masuk semula selepas kerja terhenti tanpa ujian semula"
    ]
  },
  "fire": {
    "title": "Kebakaran & Letupan",
    "level": "Risiko Tinggi",
    "feature": [
      "Kebakaran peralatan gas, kebakaran minyak, kebakaran elektrik",
      "Asap tebal, api terbuka, bau hangit, kemungkinan hentaman letupan"
    ],
    "steps": [
      "Kebakaran awal: guna pemadam api yang betul (angkat, cabut, genggam, tekan) & berdiri di arah angin atas",
      "Jika api membesar: berpindah serta-merta; tutup injap gas & suis kuasa jika selamat",
      "Bongkok rendah, tutup hidung & mulut dengan kain basah, ikut laluan kecemasan — jangan guna lif",
      "Hubungi bomba; laporkan lokasi, bahan terbakar, saiz api & keadaan mangsa terperangkap",
      "Berkumpul di titik kumpul, kira kehadiran & pandu trak bomba ke lokasi",
      "Selepas api dipadam, kekalkan kawad untuk elak marak semula"
    ],
    "report": "Pekerja tapak → ketua pasukan → ketua kawasan → pasukan bomba kilang (hubungi talian bomba)",
    "forbid": [
      "Dilarang memadam api peralatan gas secara mengejut sebelum punca gas diputus",
      "Dilarang kembali ke dalam asap tebal untuk mengambil barang",
      "Dilarang guna air untuk memadam kebakaran elektrik & minyak"
    ]
  },
  "electric": {
    "title": "Renjatan Elektrik",
    "level": "Risiko Tinggi",
    "feature": [
      "Elektrik sementara, kabel rosak, kerja dalam persekitaran lembap, penyelenggaraan peralatan beraliran",
      "Mangsa kebas, rebah, sawan, tidak sedarkan diri"
    ],
    "steps": [
      "Putuskan kuasa serta-merta atau tolak wayar dengan bahan penebat kering",
      "Sebelum mangsa terlepas dari punca elektrik, dilarang menyentuhnya secara terus",
      "Nilai kesedaran & pernafasan: jika tiada sedar & tiada nafas, lakukan CPR serta-merta",
      "Jika ada luka melecur, rawat mengikut prosedur pertolongan melecur",
      "Laporkan & lindungi lokasi; juruelektrik menyiasat kerosakan",
      "Kerja elektrik sementara mesti kemas, ada perlindungan bocor & 1 mesin 1 suis 1 perlindungan"
    ],
    "report": "Pekerja tapak → ketua pasukan → ketua kawasan → pasukan elektrik (hubungi talian kecemasan)",
    "forbid": [
      "Dilarang menarik mangsa dengan tangan kosong",
      "Dilarang guna alatan lembap atau rosak",
      "Dilarang kakitangan bukan juruelektrik membuat penyelenggaraan elektrik"
    ]
  },
  "mech": {
    "title": "Kecederaan Mekanikal",
    "level": "Risiko Sederhana Tinggi",
    "feature": [
      "Bahagian bergerak: lif baldi, tali sawat, mesin pengeluar kapur, gearbox",
      "Anggota terhimpit, terbelit, terkena; mungkin bersama patah tulang & pendarahan"
    ],
    "steps": [
      "Hentikan mesin, putus elektrik, gantung tanda serta-merta; panggil bantuan",
      "Jika berdarah: balut dengan kain bersih & tekan untuk hentikan darah",
      "Jika disyaki patah tulang: pegunkan di tempat, jangan dipindah sewenangnya",
      "Jika anggota terputus: simpan dalam plastik bersih bertutup & sejuk, bawa bersama mangsa",
      "Kekalkan suhu badan mangsa sambil menunggu bantuan profesional",
      "Cari punca & laksanakan penutup pelindung serta sistem henti–putus–gantung tanda"
    ],
    "report": "Pekerja tapak → ketua pasukan → ketua kawasan → pasukan penyelenggaraan (hubungi talian kecemasan)",
    "forbid": [
      "Dilarang membersih tali sawat & penggelek tanpa menghentikan mesin",
      "Dilarang menanggalkan penutup pelindung semasa mesin berjalan",
      "Dilarang melintas tali sawat yang sedang bergerak"
    ]
  }
}

SECTION_MS = {
  "feature": "Ciri Risiko",
  "steps": "Langkah Tindakan",
  "report": "Aliran Laporan",
  "forbid": "Perkara Dilarang"
}


def main():
    out = {"meta": {"note": "Bahasa Melayu untuk kad tindakan kecemasan"},
           "sections": SECTION_MS,
           "cards": DATA}
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", OUT)


if __name__ == "__main__":
    main()
