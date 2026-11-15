# -*- coding: utf-8 -*-
"""为 standards.json 追加马来语字段 nameMs / reqMs / vetoMs / summaryMs / focusMs"""
import json, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, "assets", "data", "standards.json")

BOARD_MS = {
    "hr": {
        "name": "Pengurusan Personel",
        "summary": "Organisasi, personel, kehadiran, gaji & prestasi serta latihan — mengukuhkan asas organisasi dan tenaga kerja kawasan.",
        "focus": "Organisasi, personel, kehadiran, gaji & prestasi, latihan",
    },
    "equipment": {
        "name": "Pengurusan Peralatan",
        "summary": "Pemeriksaan, daftar, alat ganti, penyelenggaraan, sistem, prestasi dan kebersihan — tujuh dalam satu bagi menjamin kestabilan sistem tanur Maerz.",
        "focus": "Pemeriksaan, daftar, alat ganti, penyelenggaraan, sistem, prestasi, kebersihan",
    },
    "safety": {
        "name": "Pengurusan Keselamatan",
        "summary": "Tanggungjawab, prosedur, latihan, bahaya, ruang terhad, kecemasan, semakan, PPE, peralatan khas dan kontraktor — teras pembinaan kawasan kerja standard.",
        "focus": "Tanggungjawab, prosedur, latihan, bahaya, ruang terhad, kecemasan, semakan, PPE, kontraktor",
    },
    "process": {
        "name": "Pengurusan Teknologi Proses",
        "summary": "Prosedur operasi, rekod pengeluaran dan pengurusan kemalangan — memastikan proses tanur berkembar Maerz terkawal.",
        "focus": "Prosedur operasi, rekod pengeluaran, pengurusan kemalangan",
    },
}

# key: (board_id, no) -> (nameMs, vetoMs, reqMs)
ITEM_MS = {
    ("hr", 1): ("Pengurusan Organisasi", "Tiada carta organisasi ditampal",
        "Struktur organisasi jelas; carta organisasi (dwibahasa) ditampal di lokasi sesuai tanpa kerosakan dan tidak terlindung; tanggungjawab jawatan jelas dengan deskripsi tugas dwibahasa yang lengkap dan format seragam; kemas kini dokumen dalam 7 hari bekerja selepas perubahan bilangan atau struktur organisasi."),
    ("hr", 2): ("Pengurusan Pekerja", "",
        "Pengurusan disiplin kerja patuh, berasas dan berdokumen; pengurusan pekerja keluar ikut sistem & aliran; ada rekod ganjaran dan hukuman yang sah; senarai dan rekod kehadiran pekerja luar (kontraktor) lengkap."),
    ("hr", 3): ("Pengurusan Kehadiran", "Tiada rekod permohonan cuti",
        "Laksana aliran permohonan dan lapor cuti dengan tegas serta ada rekod; ketidakhadiran diurus; cuti sakit, cuti kahwin, cuti bersalin/pasangan, cuti kematian dan cuti bencana disertakan dokumen sokongan; rekod kertas sepadan dengan sistem kehadiran ERP."),
    ("hr", 4): ("Gaji & Prestasi", "Tiada peraturan agihan/potongan bonus",
        "Ada peraturan agihan dan potongan bonus; pengurusan prestasi semua pekerja berdokumen, ada bimbingan dan teguran kesilapan serta tandatangan pengesahan pekerja; keputusan prestasi dipamer secara telus; aliran rayuan prestasi lancar dan rekod rayuan difailkan lengkap."),
    ("hr", 5): ("Pengurusan Latihan", "Tiada daftar atau rekod",
        "Wujudkan fail latihan dengan konsep satu orang satu fail; ada rekod latihan, slaid kursus, borang kehadiran, senarai peserta bulanan dan bahan latihan; disimpan kemas dan teratur; pekerja baru mempunyai rekod latihan masuk serta latihan mentor (师带徒)."),

    ("equipment", 6): ("Pemeriksaan Peralatan", "Tiada kad pemeriksaan",
        "Ada standard pemeriksaan, standard pelinciran gris dan standard teknikal penyelenggaraan; ada pelan pemeriksaan dan dilaksana mengikut pelan dengan rekod difailkan; ada sistem pembahagian tiga pihak, pemeriksaan profesional memberi latihan, semakan dan penilaian kepada pemeriksaan jawatan; kerosakan peralatan ada rekod dan pelan pembaikan/penggantian; suhu dan tekanan peralatan ditulis dengan nombor; ada prosedur operasi berserta latihan dan penilaian."),
    ("equipment", 7): ("Daftar Peralatan", "Tiada daftar peralatan",
        "Peralatan utama mempunyai daftar; kren overhead, hoist elektrik, motor dan gearbox semuanya berdaftar; daftar dikemas kini berkala, penggantian dan pembaikan ada rekod; penilaian risiko dibuat ke atas peralatan kritikal; ada daftar alatan; daftar bernombor dan bertarikh kemas kini serta ada penyedia, penyemak dan pelulus dengan tarikh."),
    ("equipment", 8): ("Alat Ganti Peralatan", "Tiada daftar",
        "Alat ganti sampingan mesin ada daftar, penggunaan ada rekod dan ada penanggungjawab; alat ganti di tapak disusun kemas; penggunaan ada rekod dan stok sampingan sepadan dengan daftar; ada rekod penyelenggaraan harian; ada pelan permohonan alat ganti dan rekod semakan pelan."),
    ("equipment", 9): ("Penyelenggaraan & Pembaikan", "Analisis kemalangan (kerosakan) tidak dibuat seperti ditetapkan",
        "Ada pelan penyelenggaraan dan laporan penyelenggaraan; ada pelan pembaikan harian, mingguan dan bulanan; kemalangan peralatan ada laporan analisis dan rekod pembelajaran, dikesan dari tiga aspek: pemeriksaan jawatan, pemeriksaan profesional dan rondaan mesin; langkah pembetulan ada rekod penutupan; ada ringkasan status operasi bulanan; ada standard kerja pembaikan berserta latihan dan rekod semakan pelaksanaan."),
    ("equipment", 10): ("Sistem Peralatan", "Tidak menerima pakai sistem peralatan syarikat",
        "Sistem peralatan syarikat diterima pakai dan dilatih; ada sistem penilaian dalaman yang dilaksanakan."),
    ("equipment", 11): ("Prestasi Peralatan", "Tiada prestasi peralatan",
        "Prestasi ketua pengeluaran, ketua pasukan pengeluaran dan operator mengandungi penilaian prestasi peralatan; ketua pemeriksaan dan pemeriksa profesional ada penilaian prestasi peralatan setiap bulan; ketua penyelenggaraan, ketua pasukan penyelenggaraan dan krew penyelenggaraan turut dinilai aspek peralatan."),
    ("equipment", 12): ("Kebersihan Peralatan", "Warna asal dan cat peralatan tidak kelihatan",
        "Peralatan menampakkan warna asal, cat berkilat; badan stesen hidraulik, paip dan instrumen bebas habuk dan kotoran; peralatan bebas habuk dan ada tanda pembersihan."),

    ("safety", 13): ("Pembahagian Tanggungjawab Keselamatan", "Tiada sistem tanggungjawab keselamatan & ganjaran/hukuman bertulis",
        "Wujudkan sistem tanggungjawab keselamatan kawasan; senaraikan peralatan, kemudahan dan alat pengeluaran; tanggungjawab keselamatan diagih hingga ke setiap jawatan (ketua kawasan, ketua pasukan, pekerja, pelatih, kontraktor) supaya semua kemudahan keselamatan ada penanggungjawab; tandatangan ikrar keselamatan pengeluaran."),
    ("safety", 16): ("Prosedur Operasi Selamat", "Tiada prosedur operasi selamat",
        "Ada daftar prosedur operasi selamat; prosedur, papan kawasan dan papan ikrar keselamatan ditampal di dinding; pekerja menguasai prosedur jawatan masing-masing; ada rekod semakan; tiada perbuatan melanggar peraturan di tapak."),
    ("safety", 17): ("Latihan Keselamatan", "Tiada fail latihan keselamatan",
        "Fail latihan keselamatan satu salinan bagi setiap orang; rekod dan daftar latihan lengkap; ada rekod latihan masuk kilang dan latihan keselamatan khas; ada bahan latihan keselamatan; fail latihan diisi lengkap dan betul."),
    ("safety", 18): ("Mesyuarat Keselamatan", "",
        "Taklimat keselamatan serah tugas syif: bahaya yang belum dibaiki dan kerja penyelenggaraan tertunggak diterangkan kepada pasukan ganti; mesyuarat pra-syif mengenal pasti kerja berisiko tinggi, menetapkan langkah keselamatan dan mengadakan ikrar keselamatan bersama; mesyuarat pasca-syif mengira kehadiran, menilai pelaksanaan langkah dan mengumumkan “tiga pelanggaran”; aktiviti keselamatan mingguan sekali seminggu; mesyuarat keselamatan bulanan peringkat kawasan dan pasukan; kehadiran, kandungan dan rekod lengkap."),
    ("safety", 23): ("Pengurusan Bahaya", "Tiada daftar bahaya",
        "Kenal pasti, kumpulkan, nilaikan bahaya dan tentukan langkah kawalan; semakan sekali setahun dan simpan versi terkini; tentukan bahaya utama dan kawal secara berperingkat; wujudkan dan lengkapkan daftar bahaya serta laksana langkah pengurusan keselamatan; semak kelengkapan penyelamat dan penyelenggaraannya, rakaman berterusan parameter penting, kelulusan kerja berbahaya dan semakan semasa kerja."),
    ("safety", 25): ("Kerja Ruang Terhad", "Tiada daftar ruang terhad",
        "Wujudkan daftar ruang terhad dan daftar kerja ruang terhad kawasan; sebelum kerja beri taklimat keselamatan, taklimat teknikal, latihan dan peperiksaan kepada ketua kerja, pengawas, pekerja dan pasukan penyelamat; laksana kelulusan kerja (pelan kerja, langkah keselamatan, pelan kecemasan, borang kerja, daftar keluar-masuk); semakan keselamatan sebelum, semasa dan selepas kerja; lengkapkan pemfailan dokumen."),
    ("safety", 30): ("Jadual Betul / Salah", "Tiada jadual betul/salah jawatan",
        "Ada jadual operasi betul vs salah dan ditampal di dinding; jadual lengkap dan wajib bagi jawatan berisiko tinggi; pekerja menguasai kandungan jadual."),
    ("safety", 31): ("Kemalangan & Pelan Kecemasan", "Tiada pelan kecemasan; berlaku kemalangan cedera ringan ke atas",
        "Sediakan pelan tindak balas kecemasan dan edarkan ke jawatan dengan rekod pemfailan; latihan amali pelan tindakan tapak sekurang-kurangnya setiap enam bulan; sediakan kelengkapan penyelamat yang mencukupi & layak dan wujudkan daftar (lokasi, kuantiti, penanggungjawab, telefon); semak dan selenggara kemudahan kecemasan secara berkala; latihan kecemasan setahun sekali bagi kakitangan berkaitan, jawatan kritikal ≥2 kali setahun dan ≥2 jam setiap kali; wujudkan daftar kemalangan berserta laporan siasatan, rekod pengenaan tanggungjawab dan rekod susulan langkah pencegahan; failkan bahan latihan serta-merta (teks pelan, skrip, rekod latihan, kehadiran, rekod proses, ringkasan penilaian, bahan visual); jika ada masalah, kemas kini pelan dalam seminggu dan latih serta uji semua pekerja dalam 8 hari."),
    ("safety", 32): ("Pengurusan Tapak & Susun Atur", "",
        "Kawasan sentiasa bersih, ada pengurusan susun atur tetap, kebersihan berzon dan berpenanggungjawab; wujudkan carta rangkaian pengurusan tapak, tanggungjawab diagih ke setiap jawatan supaya semua kawasan ada penanggungjawab; bahan, alat ganti dan perkakas disusun kemas dengan papan tanda yang jelas; pejabat, bilik mesyuarat, bilik operasi dan bilik rehat tersusun; stor, jalan, koridor tali sawat, gudang bahan dan kawasan hijau diurus mengikut standard."),
    ("safety", 43): ("Senarai Semak Keselamatan", "Tiada daftar semakan keselamatan",
        "Senarai semak mesti ada lima elemen: item semakan, standard, keadaan, masa dan pemeriksa; meliputi ketua kawasan, ketua syif (ketua pasukan), jawatan, semakan bersama kawasan dan semakan khas; sediakan pelan semakan tahunan dan bulanan serta laksana mengikut pelan; ketua kawasan syif siang memeriksa sekurang-kurangnya tiga jawatan sehari dan tandatangan silang; ketua pasukan memeriksa setiap jawatan sekali setiap syif; pekerja memeriksa peranti keselamatan dan alat jawatan tidak kurang 3 kali setiap syif, rondaan berterusan di bahagian “dua utama satu besar”; wujudkan daftar pembaikan bahaya — yang boleh dibaiki tentukan langkah, masa dan penanggungjawab, yang tidak boleh dibaiki laporkan naik dan susul semak; keputusan semakan dikait dengan ganjaran dan hukuman."),
    ("safety", 50): ("Pengurusan PPE", "Tiada daftar PPE",
        "Ada daftar PPE, pengagihan ada rekod dan tandatangan pekerja; laksana mengikut standard agihan, lebihan ada rekod tukar baru ganti lama; pemakaian PPE di tapak mematuhi keperluan."),
    ("safety", 51): ("Peralatan Khas & Kelengkapan Kecemasan", "Tiada daftar peralatan khas",
        "Wujudkan daftar peralatan khas: kren overhead, kren, dandang, bekas tekanan dan lif; wujudkan daftar kelengkapan kecemasan: alat pernafasan udara, penggera gas, pemadam api, injap keselamatan dan tolok tekanan; daftar dikemas kini tepat pada masa."),
    ("safety", 52): ("Pengurusan Kontraktor", "Tiada daftar pengurusan kontraktor",
        "Wujudkan dan lengkapkan daftar pengurusan kontraktor; sebelum masuk kerja beri taklimat keselamatan dan latihan (kontraktor jangka panjang sekali setahun, ulang semula jika persekitaran berubah, projek penyelenggaraan singkat dimaklumkan sebelum kerja); sebelum kerja sahkan langkah keselamatan pihak pembinaan, semasa kerja adakan pengawasan, selepas kerja semak pembersihan dan pemulihan kemudahan keselamatan; permit kerja berbahaya kontraktor; pekerja luar dimasukkan ke dalam pengurusan keselamatan harian kawasan."),

    ("process", 56): ("Prosedur Operasi", "",
        "Ada prosedur operasi proses/teknikal seperti《Prosedur Operasi Teknikal Tanur Kapur Maerz》; ada rekod latihan prosedur; sebelum peralatan atau proses baru beroperasi, prosedur dikemukakan untuk kelulusan dan dikemas kini; pekerja pindah jawatan dilatih dan diuji bagi prosedur jawatan baru."),
    ("process", 57): ("Rekod Pengeluaran", "",
        "Proses pengeluaran ada rekod (rekod operasi kawalan utama, rekod suhu badan tanur dan lain-lain), semakan proses ada rekod, keabnormalan proses ada semakan dan langkah pembetulan yang dilaksana."),
    ("process", 58): ("Pengurusan Kemalangan", "",
        "Ada daftar kemalangan kualiti proses; kemalangan proses dan kemalangan kualiti ada laporan analisis dan langkah pembetulan; kemalangan kualiti proses ada rekod latihan."),
}


def main():
    with io.open(P, encoding="utf-8") as f:
        data = json.load(f)
    miss = 0
    for b in data["boards"]:
        m = BOARD_MS.get(b["id"])
        if m:
            b["nameMs"] = m["name"]
            b["summaryMs"] = m["summary"]
            if b.get("focus"):
                b["focusMs"] = m["focus"]
        for it in b["items"]:
            t = ITEM_MS.get((b["id"], it["no"]))
            if not t:
                miss += 1
                print("MISSING", b["id"], it["no"], it["name"])
                continue
            it["nameMs"] = t[0]
            if it.get("veto"):
                it["vetoMs"] = t[1]
            it["reqMs"] = t[2]
    with io.open(P, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("done, missing =", miss)


if __name__ == "__main__":
    main()
