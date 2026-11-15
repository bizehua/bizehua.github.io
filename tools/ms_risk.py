# -*- coding: utf-8 -*-
import io, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, "pages", "risk-library.html")

PAIRS = [
    ('<title>工艺风险知识库 · 危险源管理</title>',
     '<title>工艺风险知识库 · Pangkalan Risiko Proses</title>'),
    ('<div class="breadcrumb"><a href="../index.html">首页</a><span>›</span><a href="safety.html">安全管理</a><span>›</span>工艺风险知识库</div>',
     '<div class="breadcrumb"><a href="../index.html">首页 Utama</a><span>›</span><a href="safety.html">安全管理 Keselamatan</a><span>›</span>工艺风险知识库 Pangkalan risiko</div>'),
    ('<h1 style="font-size:21px;font-weight:800">⚠️ 工艺风险知识库</h1>\n    <p class="ms" style="font-size:14px;font-weight:600;margin-top:6px">Pangkalan Risiko Proses</p>',
     '<h1 style="font-size:21px;font-weight:800">⚠️ 工艺风险知识库 <span class="ms" style="font-size:14px">Pangkalan Risiko Proses</span></h1>'),
    ('<span class="badge danger">否决项：无危险源台账</span>',
     '<span class="badge danger">否决项 Item veto：无危险源台账 Tiada daftar bahaya</span>'),
    ('员工抽查不掌握每人次扣分。\n    </p>',
     '员工抽查不掌握每人次扣分。\n      <span class="ms">Berdasarkan Jadual Pengenalan Risiko HIRARC kawasan (dinilai 2025-09, semakan tahunan), daftar kelulusan kerja berbahaya dan daftar pembaikan bahaya bulanan — meliputi <b>16 jenis risiko</b>. Pengenalan bahaya tidak lengkap, langkah keselamatan tidak dilaksana, kerja berbahaya tanpa kelulusan akan dinilai mengikut klausa 23–24; pekerja yang tidak menguasai akan ditolak markah setiap orang.</span>\n    </p>'),
    ('<h2>隐患治理数据看板</h2><span class="sub" id="statSub">条目按区域与责任班组分布 · 可按月份切换</span>',
     '<h2>隐患治理数据看板<span class="ms">Papan Data Pembaikan Bahaya</span></h2><span class="sub" id="statSub">条目按区域与责任班组分布 · 可按月份切换<span class="ms">Taburan mengikut zon &amp; pasukan · boleh tukar bulan</span></span>'),
    ('<span class="f-label">统计月份</span>',
     '<span class="f-label">统计月份 Bulan</span>'),
    ('<p class="muted" style="font-size:12px;margin-bottom:6px">典型隐患条目 Bahaya tipikal</p>',
     '<p class="muted" style="font-size:12px;margin-bottom:6px">典型隐患条目 Bahaya tipikal</p>'),
    ('<p class="strong" style="margin-bottom:10px">按隐患区域分布 <span class="muted" style="font-weight:400">Mengikut zon</span></p>',
     '<p class="strong" style="margin-bottom:10px">按隐患区域分布 <span class="muted" style="font-weight:400">Mengikut zon</span></p>'),
    ('<p class="strong" style="margin-bottom:10px">按责任班组分布 <span class="muted" style="font-weight:400">Mengikut pasukan</span></p>',
     '<p class="strong" style="margin-bottom:10px">按责任班组分布 <span class="muted" style="font-weight:400">Mengikut pasukan</span></p>'),
    ('<h2>风险清单与管控措施</h2><span class="sub">点击分类筛选，支持关键词搜索</span>',
     '<h2>风险清单与管控措施<span class="ms">Senarai Risiko &amp; Langkah Kawalan</span></h2><span class="sub">点击分类筛选，支持关键词搜索<span class="ms">Klik kategori untuk tapis, sokongan carian kata kunci</span></span>'),
    ('<span class="f-label">风险类别</span>', '<span class="f-label">风险类别 Kategori</span>'),
    ('<span class="f-label">风险等级</span>', '<span class="f-label">风险等级 Tahap</span>'),
    ('placeholder="搜索风险 / 作业活动 / 隐患…"',
     'placeholder="搜索风险 / 作业活动 / 隐患… Cari risiko / aktiviti…"'),
    ('<h2>八类危险作业许可</h2><span class="sub">危险作业无审批、安全措施不落实按条款23~24考核</span>',
     '<h2>八类危险作业许可<span class="ms">Permit 8 Jenis Kerja Berbahaya</span></h2><span class="sub">危险作业无审批、安全措施不落实按条款23~24考核<span class="ms">Kerja berbahaya tanpa kelulusan atau langkah keselamatan tidak dilaksana dinilai mengikut klausa 23–24</span></span>'),
    # 8 cards
    ('<h3 style="font-size:14.5px">动火作业</h3><p class="b-desc">特级/一级/二级分级审批</p><span class="b-go">审批表下载 →</span>',
     '<h3 style="font-size:14.5px">动火作业<span class="ms">Kerja Api</span></h3><p class="b-desc">特级/一级/二级分级审批<span class="ms">Kelulusan 3 peringkat</span></p><span class="b-go">审批表下载 Muat turun →</span>'),
    ('<h3 style="font-size:14.5px">受限空间作业</h3><p class="b-desc">先通风、再检测、后作业</p><span class="b-go">专题页 →</span>',
     '<h3 style="font-size:14.5px">受限空间作业<span class="ms">Ruang Terhad</span></h3><p class="b-desc">先通风、再检测、后作业<span class="ms">Ventilasi → uji → kerja</span></p><span class="b-go">专题页 Halaman →</span>'),
    ('<h3 style="font-size:14.5px">高处作业</h3><p class="b-desc">2m以上分级管理</p><span class="b-go">审批表下载 →</span>',
     '<h3 style="font-size:14.5px">高处作业<span class="ms">Kerja Ketinggian</span></h3><p class="b-desc">2m以上分级管理<span class="ms">Berperingkat dari 2m</span></p><span class="b-go">审批表下载 Muat turun →</span>'),
    ('<h3 style="font-size:14.5px">起重 / 吊装</h3><p class="b-desc">执行起重十不吊</p><span class="b-go">审批表下载 →</span>',
     '<h3 style="font-size:14.5px">起重 / 吊装<span class="ms">Mengangkat</span></h3><p class="b-desc">执行起重十不吊<span class="ms">10 larangan mengangkat</span></p><span class="b-go">审批表下载 Muat turun →</span>'),
    ('<h3 style="font-size:14.5px">动土作业</h3><p class="b-desc">地下设施交底确认</p><span class="b-go">审批表下载 →</span>',
     '<h3 style="font-size:14.5px">动土作业<span class="ms">Kerja Galian</span></h3><p class="b-desc">地下设施交底确认<span class="ms">Sahkan kemudahan bawah tanah</span></p><span class="b-go">审批表下载 Muat turun →</span>'),
    ('<h3 style="font-size:14.5px">断路作业</h3><p class="b-desc">交通组织与警戒</p><span class="b-go">审批表下载 →</span>',
     '<h3 style="font-size:14.5px">断路作业<span class="ms">Potong Jalan</span></h3><p class="b-desc">交通组织与警戒<span class="ms">Atur trafik &amp; kawad</span></p><span class="b-go">审批表下载 Muat turun →</span>'),
    ('<h3 style="font-size:14.5px">抽堵盲板</h3><p class="b-desc">煤气眼睛阀高风险作业</p><span class="b-go">审批表下载 →</span>',
     '<h3 style="font-size:14.5px">抽堵盲板<span class="ms">Plat Buta</span></h3><p class="b-desc">煤气眼睛阀高风险作业<span class="ms">Injap mata gas — risiko tinggi</span></p><span class="b-go">审批表下载 Muat turun →</span>'),
    ('<h3 style="font-size:14.5px">临时用电</h3><p class="b-desc">一机一闸一保护</p><span class="b-go">审批表下载 →</span>',
     '<h3 style="font-size:14.5px">临时用电<span class="ms">Elektrik Sementara</span></h3><p class="b-desc">一机一闸一保护<span class="ms">1 mesin 1 suis 1 perlindungan</span></p><span class="b-go">审批表下载 Muat turun →</span>'),
    # JS labels
    ('''(key === "year" ? "2026年1-9月隐患治理台账合计（累计4438项，每月440~541项，逐项登记、整改、验收、销号）"''',
     '''(key === "year" ? "2026年1-9月隐患治理台账合计（累计" + st.total + "项，每月440~541项，逐项登记、整改、验收、销号）"'''),
    ('''Jumlah daftar Jan–Sep 2026 (4,438 item; 440–541 item sebulan; daftar, baiki, sah & tutup satu per satu)''',
     '''Jumlah daftar Jan–Sep 2026 (" + st.total + " item; 440–541 item sebulan; daftar, baiki, sah & tutup satu per satu)'''),
    ('''2026年1-9月合计 · 条目按区域与责任班组分布''',
     '''2026年1-9月合计 · 条目按区域与责任班组分布'''),
    ('''Jumlah Jan–Sep 2026 · taburan zon & pasukan''',
     '''Jumlah Jan–Sep 2026 · taburan zon & pasukan'''),
    ('var chips = [{ key: "year", label: "全年汇总 (1-9月)" }]',
     'var chips = [{ key: "year", label: "全年汇总 Jumlah (1-9月)" }]'),
    ('''{ key: String(m.month), label: m.label.replace("2026年", "") + " (" + m.total + "项)" }''',
     '''{ key: String(m.month), label: m.label.replace("2026年", "") + " (" + m.total + "项)" }'''),
    ('var cats = [{ id: "all", name: "全部", color: "" }]',
     'var cats = [{ id: "all", name: "全部 Semua", color: "" }]'),
    ('var levelName = { all: "全部等级", "极高": "极高", "高": "高", "中": "中" };',
     'var levelName = { all: "全部等级 Semua", "极高": "极高 Sangat Tinggi", "高": "高 Tinggi", "中": "中 Sederhana" };'),
    ('\'<div class="rc-row"><b>风险类别：</b>', '\'<div class="rc-row"><b>风险类别 Kategori：</b>'),
    ('\'<div class="rc-row"><b>作业活动：</b>', '\'<div class="rc-row"><b>作业活动 Aktiviti：</b>'),
    ('\'<div class="rc-row"><b>产生原因：</b>', '\'<div class="rc-row"><b>产生原因 Punca：</b>'),
    ('\'<div class="rc-row"><b>可能导致：</b>', '\'<div class="rc-row"><b>可能导致 Kesan：</b>'),
    ('\'<div class="rc-row"><b>管控措施：</b>', '\'<div class="rc-row"><b>管控措施 Kawalan：</b>'),
    ('''"共 " + list.length + " 项风险（全库 " + data.risks.length + " 项）｜ " + data.meta.note;''',
     '''"共 " + list.length + " 项风险（全库 " + data.risks.length + " 项）｜ " + data.meta.note +
          '<span class="ms">Jumlah ' + list.length + " risiko (keseluruhan " + data.risks.length + ")</span>";'''),
    ('''<div>风险数据加载失败，请确认 assets/data/risks.json 文件存在。</div>''',
     '''<div>风险数据加载失败，请确认 assets/data/risks.json 文件存在。<span class="ms">Gagal memuat data risiko; pastikan fail wujud.</span></div>'''),
    ('''<p class="muted" style="font-size:11px;margin-top:6px">数据来源：' + r.source + "</p>"''',
     '''<p class="muted" style="font-size:11px;margin-top:6px">数据来源 Sumber：' + r.source + "</p>"'''),
]


def main():
    with io.open(P, encoding="utf-8") as f:
        s = f.read()
    for old, new in PAIRS:
        n = s.count(old)
        if n != 1:
            print("!! count=%d for: %s" % (n, old[:70]))
            sys.exit(1)
        s = s.replace(old, new)
    with io.open(P, "w", encoding="utf-8") as f:
        f.write(s)
    print("risk-library.html OK, %d replacements" % len(PAIRS))


if __name__ == "__main__":
    main()
