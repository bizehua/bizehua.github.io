# -*- coding: utf-8 -*-
"""
东钢焦电部石灰作业区 · 安全生产表单 PDF 生成脚本
字段结构转换自工作域现有表单文件：
  1. 有限空间作业审批表.pdf      ← 3、安全管理/6特殊作业管理/有限空间作业台账.xlsx
  2. 隐患排查治理台账.pdf         ← 3、安全管理/10安全检查表/隐患台账/石灰1月隐患台账.xlsx
  3. 安全培训签到表.pdf           ← 1、人事管理/5、培训管理/2026.1/1月培训照片及签到.xlsx
  4. 安全检查表（中英）.pdf       ← 3、安全管理/10安全检查表/安全检查表新版/筒仓安全生产检查表.xlsx
  5. 危险作业审批表.pdf           ← 3、安全管理/5危险源管理/1石灰危险作业台账、审批台账.xlsx
  6. 应急救援物资台账.pdf         ← 3、安全管理/8事故与应急预案1/5 应急救援物资台账/石灰作业区应急物资台账.xlsx
运行：python3 tools/generate_pdfs.py
"""
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# ---------- 中文字体 ----------
FONT = "STSong-Light"
FONT_B = "STSong-Light"
try:
    pdfmetrics.registerFont(TTFont("STHeiti", "/System/Library/Fonts/STHeiti Light.ttc", subfontIndex=0))
    FONT = FONT_B = "STHeiti"
except Exception:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

NAVY = colors.HexColor("#1E3A5F")
NAVY2 = colors.HexColor("#2C5282")
LIGHT = colors.HexColor("#EEF2F7")
GRID = colors.HexColor("#9AA8B8")
TEXT = colors.HexColor("#16202E")
RED = colors.HexColor("#B71C1C")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "downloads")
OUT = os.path.abspath(OUT)

MARGIN = 15 * mm


def P(text, size=10, bold=False, align=TA_LEFT, color=TEXT, leading=None):
    return Paragraph(text, ParagraphStyle(
        "s", fontName=FONT_B if bold else FONT, fontSize=size,
        leading=leading or size * 1.55, alignment=align, textColor=color, wordWrap="CJK"))


def title_block(title, sub, width):
    t = Table([[P(title, 15, True, TA_CENTER, colors.white)],
               [P(sub, 8.5, False, TA_CENTER, colors.HexColor("#D7E3F2"))]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, 0), 8), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
        ("TOPPADDING", (0, 1), (-1, 1), 0), ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def section_bar(text, width):
    t = Table([[P(text, 10.5, True, TA_LEFT, colors.white)]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY2),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def styled_table(data, widths, row_heights=None, header_rows=0, font_size=9.5):
    t = Table(data, colWidths=widths, rowHeights=row_heights, repeatRows=header_rows)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), FONT),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("GRID", (0, 0), (-1, -1), 0.6, GRID),
        ("BOX", (0, 0), (-1, -1), 1.1, NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]
    if header_rows:
        style += [("BACKGROUND", (0, 0), (-1, header_rows - 1), LIGHT),
                  ("FONTNAME", (0, 0), (-1, header_rows - 1), FONT_B)]
    t.setStyle(TableStyle(style))
    return t


def note(text):
    return P("说明：" + text, 8.5, False, TA_LEFT, colors.HexColor("#4A5A6E"))


def footer_factory(site_note):
    def _footer(canvas, doc):
        canvas.saveState()
        w, h = doc.pagesize
        canvas.setFont(FONT, 7.5)
        canvas.setFillColor(colors.HexColor("#7D8CA0"))
        canvas.drawString(MARGIN, 7 * mm, site_note)
        canvas.drawRightString(w - MARGIN, 7 * mm, "第 %d 页" % doc.page)
        canvas.setStrokeColor(colors.HexColor("#C7D2DE"))
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, 10 * mm, w - MARGIN, 10 * mm)
        canvas.restoreState()
    return _footer


SITE_NOTE = "东钢焦电部石灰作业区 · 安全生产表单（依据《2026年东钢集团“标准化作业区”验收标准》转换生成）"


def build(path, pagesize, title, story):
    doc = SimpleDocTemplate(path, pagesize=pagesize,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=13 * mm, bottomMargin=14 * mm,
                            title=title, author="东钢焦电部石灰作业区")
    doc.build(story, onFirstPage=footer_factory(SITE_NOTE), onLaterPages=footer_factory(SITE_NOTE))
    print("生成:", path)


# ============================================================
# 1. 有限空间作业审批表（纵向）
# ============================================================
def pdf_confined_space():
    W = A4[0] - 2 * MARGIN
    s = [title_block("有限空间作业审批表", "编号：____________________ ｜ 作业前办理 · 票据随身携带 · 作业区留存", W), Spacer(1, 5 * mm)]

    info = [
        [P("作业单位/班组", 9.5, True), "", P("作业地点", 9.5, True), ""],
        [P("有限空间名称", 9.5, True), "", P("主要危害物质", 9.5, True), ""],
        [P("作业负责人", 9.5, True), "", P("监护人员", 9.5, True), ""],
        [P("作业人员", 9.5, True), "", P("计划作业时间", 9.5, True), P("　　年　　月　　日　　时至　　时", 9.5)],
        [P("作业内容", 9.5, True), "", "", ""],
    ]
    t = styled_table(info, [30 * mm, 60 * mm, 30 * mm, 60 * mm], row_heights=[10 * mm] * 5)
    t.setStyle(TableStyle([("SPAN", (1, 4), (3, 4)), ("BACKGROUND", (0, 0), (0, -1), LIGHT),
                           ("BACKGROUND", (2, 0), (2, -2), LIGHT)]))
    s += [t, Spacer(1, 4 * mm), section_bar("一、气体检测记录", W), Spacer(1, 1.5 * mm)]

    det = [[P("检测时机", 9.5, True, TA_CENTER), P("氧含量 %（19.5~23.5）", 9, True, TA_CENTER),
            P("CO mg/m³", 9, True, TA_CENTER), P("可燃气体 %LEL", 9, True, TA_CENTER),
            P("检测时间", 9, True, TA_CENTER), P("检测人", 9, True, TA_CENTER)]]
    for k in ["作业前", "作业中", "作业后"]:
        det.append([P(k, 9.5, False, TA_CENTER), "", "", "", "", ""])
    s += [styled_table(det, [30 * mm, 34 * mm, 26 * mm, 30 * mm, 32 * mm, 28 * mm], row_heights=[9 * mm, 9 * mm, 9 * mm, 9 * mm], header_rows=1),
          Spacer(1, 4 * mm), section_bar("二、安全措施确认（逐项确认后打√）", W), Spacer(1, 1.5 * mm)]

    checks = ["已办理有限空间作业审批，作业票据随身携带",
              "已对作业负责人、监护人员、作业人员、应急救援人员进行安全告知、技术交底并培训考试",
              "已进行强制通风置换，气体检测合格（氧含量19.5%~23.5%、CO不超标）",
              "作业人员佩戴正压式空气呼吸器并系安全绳，通讯畅通",
              "外部设专人全程监护，应急救援器材（三脚架、安全绳、呼吸器）到位",
              "作业中断后再次进入前，已重新通风、检测合格",
              "已执行作业前、作业过程、作业后安全检查并记录",
              "出入登记已建立，人员、工具、物料出入已登记"]
    ck = [[P("□ " + c, 9.5)] for c in checks]
    t = styled_table(ck, [W], row_heights=[8.5 * mm] * len(checks))
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, GRID), ("BOX", (0, 0), (-1, -1), 1.1, NAVY),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    s += [t, Spacer(1, 4 * mm), section_bar("三、作业出入登记", W), Spacer(1, 1.5 * mm)]

    reg = [[P("序号", 9.5, True, TA_CENTER), P("时间", 9.5, True, TA_CENTER), P("地点", 9.5, True, TA_CENTER),
            P("出入登记人员", 9.5, True, TA_CENTER), P("监护人员", 9.5, True, TA_CENTER), P("检测结果", 9.5, True, TA_CENTER)]]
    for i in range(1, 6):
        reg.append([P(str(i), 9.5, False, TA_CENTER), "", "", "", "", ""])
    s += [styled_table(reg, [14 * mm, 30 * mm, 30 * mm, 36 * mm, 34 * mm, 36 * mm], row_heights=[9 * mm] * 6, header_rows=1),
          Spacer(1, 4 * mm), section_bar("四、审批签字", W), Spacer(1, 1.5 * mm)]

    sign = [[P("申请人/日期", 9.5, True, TA_CENTER), P("监护人/日期", 9.5, True, TA_CENTER),
             P("作业负责人/日期", 9.5, True, TA_CENTER), P("作业区审批人/日期", 9.5, True, TA_CENTER),
             P("厂级审批人/日期", 9.5, True, TA_CENTER)],
            ["", "", "", "", ""]]
    s += [styled_table(sign, [36 * mm] * 5, row_heights=[9 * mm, 16 * mm], header_rows=1), Spacer(1, 4 * mm),
          note("本表依据验收标准第25~29项（特殊作业管理：有限空间作业安全管理）及作业区《有限空间作业台账》字段编制；无有限空间台账、未执行作业审批按否决项处理。")]
    build(os.path.join(OUT, "有限空间作业审批表.pdf"), A4, "有限空间作业审批表", s)


# ============================================================
# 2. 隐患排查治理台账（横向）
# ============================================================
def pdf_hazard_ledger():
    W = landscape(A4)[0] - 2 * MARGIN
    s = [title_block("石灰作业区2026年　　月隐患治理台账", "检查人：____________ ｜ 检查日期：　　年　　月　　日 ｜ 发现一项、登记一项、整改一项、销号一项", W),
         Spacer(1, 4 * mm)]

    head = ["序号", "检查人", "隐患内容", "隐患区域", "隐患类别", "整改期限", "责任班组", "责任人", "整改措施", "完成时间", "验收人"]
    data = [[P(h, 9, True, TA_CENTER) for h in head]]
    for i in range(1, 16):
        data.append([P(str(i), 9, False, TA_CENTER)] + [""] * 10)
    widths = [10 * mm, 20 * mm, 61 * mm, 18 * mm, 22 * mm, 20 * mm, 18 * mm, 20 * mm, 42 * mm, 20 * mm, 16 * mm]
    s += [styled_table(data, widths, row_heights=[9 * mm] + [10.5 * mm] * 15, header_rows=1), Spacer(1, 4 * mm),
          note("隐患类别分为：一般事故隐患 / 重大事故隐患；整改期限分为：立即整改 / 限期整改 / 计划整改。能整改的制定措施、落实时间与责任人；不能整改的逐级上报并跟踪复查；检查结果与奖惩挂钩（验收标准第43~49项）。")]
    build(os.path.join(OUT, "隐患排查治理台账.pdf"), landscape(A4), "隐患排查治理台账", s)


# ============================================================
# 3. 安全培训签到表（纵向）
# ============================================================
def pdf_training_sign():
    W = A4[0] - 2 * MARGIN
    s = [title_block("安全培训签到表", "本表存入“一人一档”培训档案 ｜ 签到须本人签字 ｜ 验收标准第17项", W), Spacer(1, 5 * mm)]

    info = [
        [P("培训主题", 9.5, True), "", P("培训日期", 9.5, True), ""],
        [P("培训地点", 9.5, True), "", P("主讲人", 9.5, True), ""],
        [P("培训类别", 9.5, True), P("□入厂安全教育　□岗位操作规程　□专项培训　□应急演练　□其他：______", 9.5), P("学时", 9.5, True), ""],
    ]
    t = styled_table(info, [30 * mm, 60 * mm, 30 * mm, 60 * mm], row_heights=[10 * mm] * 3)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), LIGHT), ("BACKGROUND", (2, 0), (2, -1), LIGHT)]))
    s += [t, Spacer(1, 4 * mm), section_bar("培训签到明细", W), Spacer(1, 1.5 * mm)]

    head = ["序号", "姓名", "岗位 / 班组", "签到（本人签字）", "考试成绩", "备注"]
    data = [[P(h, 9.5, True, TA_CENTER) for h in head]]
    for i in range(1, 17):
        data.append([P(str(i), 9.5, False, TA_CENTER), "", "", "", "", ""])
    s += [styled_table(data, [14 * mm, 38 * mm, 44 * mm, 44 * mm, 20 * mm, 20 * mm], row_heights=[9 * mm] * 17, header_rows=1),
          Spacer(1, 4 * mm),
          note("培训档案一人一档，使用人资统一模板，纸质+电子双端存档；新入职人员须有入职培训及师带徒培训记录；专项培训（如有限空间）须附考试成绩。")]
    build(os.path.join(OUT, "安全培训签到表.pdf"), A4, "安全培训签到表", s)


# ============================================================
# 4. 安全检查表（中英）（纵向）
# ============================================================
def pdf_bilingual_checklist():
    W = A4[0] - 2 * MARGIN
    s = [title_block("石灰作业区（筒仓：面灰仓、块灰仓）安全生产检查表",
                     "Silo (Face Lime Silo / Lump Lime Silo) Safety Inspection Checklist ｜ 第 ____ 周 ｜ 日期：　　年　　月　　日 ｜ 班次：□白班　□夜班", W),
         Spacer(1, 4 * mm)]

    rows = [
        ("1", "料仓本体支架", "Silo body bracket", "支撑点地脚螺栓无松动，支撑立柱连接点无腐蚀", "Support bolts tight; no corrosion at column joints"),
        ("2", "安全通道", "Safety exit", "安全通道畅通，不存放杂物；斜梯、楼梯防护完好", "Exit clear, no debris; stairs and ladders well protected"),
        ("3", "平台护栏", "Platform guardrail", "平台边缘无容易下落的杂物；防护栏完好", "No loose items at platform edge; guardrail intact"),
        ("4", "灭火器", "Fire extinguisher", "灭火器压力充足、附件齐全、在检验周期内", "Sufficient pressure, complete accessories, within validity period"),
        ("5", "照明设施", "Lighting facilities", "照明良好、光线充足；电源接线无裸露", "Good lighting; no exposed wiring"),
        ("6", "警示标识", "Warning sign", "安全警示标识醒目、悬挂规范、干净整洁", "Signs conspicuous, properly hung and clean"),
        ("7", "放料装置", "Discharge device", "电液推杆运行正常，无漏油；装车装置运行正常", "Electric push rod runs normally without oil leakage"),
        ("8", "溜槽", "Chute", "溜槽、溜管无漏洞、畅通；溜槽吊点无开焊", "No leakage or blockage; hangers free of cracks"),
    ]
    head = ["序号", "检查部位\nCheck parts", "检查标准\nInspection standard", "检查情况\nInspection status", "检查人\nChecker"]
    data = [[P(h.replace("\n", "<br/>"), 9, True, TA_CENTER) for h in head]]
    for no, cn, en, cn_std, en_std in rows:
        data.append([P(no, 9, False, TA_CENTER),
                     P("<b>%s</b><br/>%s" % (cn, en), 8.5),
                     P("%s<br/><font color='#7D8CA0'>%s</font>" % (cn_std, en_std), 8.5),
                     "", ""])
    s += [styled_table(data, [11 * mm, 36 * mm, 85 * mm, 28 * mm, 20 * mm], row_heights=None, header_rows=1),
          Spacer(1, 3 * mm)]
    sign = [[P("作业长或组长签字<br/>Signature of supervisor or team leader", 9, True, TA_CENTER), ""]]
    t = styled_table(sign, [60 * mm, 120 * mm], row_heights=[14 * mm])
    s += [t, Spacer(1, 4 * mm),
          note("检查表五要素齐全：检查项目、检查标准、检查情况、检查时间、检查人；覆盖作业长、班组长、岗位、作业区联查、专项检查（验收标准第43项）；检查结果与奖惩挂钩。")]
    build(os.path.join(OUT, "安全检查表（中英）.pdf"), A4, "安全检查表（中英）", s)


# ============================================================
# 5. 危险作业审批表（纵向）
# ============================================================
def pdf_hazardous_permit():
    W = A4[0] - 2 * MARGIN
    s = [title_block("危险作业审批表", "编号：____________________ ｜ 先审批后作业 · 作业票据随身携带", W), Spacer(1, 5 * mm)]

    t1 = [[P("作业类型", 9.5, True), P("□动火作业　□高处作业　□起重作业　□受限空间作业　□动土作业<br/>□断路作业　□抽堵盲板作业　□临时用电作业", 9.5)]]
    t = styled_table(t1, [26 * mm, 154 * mm], row_heights=[16 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), LIGHT)]))
    s += [t, Spacer(1, 3 * mm)]

    info = [
        [P("作业位置", 9.5, True), "", P("作业主体/班组", 9.5, True), ""],
        [P("申请人", 9.5, True), "", P("计划作业时间", 9.5, True), P("　　年　　月　　日　　时至　　时", 9.5)],
        [P("监护人员", 9.5, True), "", P("作业人数", 9.5, True), ""],
    ]
    t = styled_table(info, [30 * mm, 60 * mm, 30 * mm, 60 * mm], row_heights=[10 * mm] * 3)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), LIGHT), ("BACKGROUND", (2, 0), (2, -1), LIGHT)]))
    s += [t, Spacer(1, 4 * mm), section_bar("风险评估与控制措施", W), Spacer(1, 1.5 * mm)]

    risk = [
        [P("主要危害物质", 9.5, True), ""],
        [P("作业内容", 9.5, True), ""],
        [P("可能造成的事故", 9.5, True), ""],
        [P("主要控制措施", 9.5, True), ""],
    ]
    t = styled_table(risk, [36 * mm, 144 * mm], row_heights=[11 * mm, 13 * mm, 11 * mm, 22 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), LIGHT)]))
    s += [t, Spacer(1, 4 * mm), section_bar("安全确认（逐项确认后打√）", W), Spacer(1, 1.5 * mm)]

    checks = ["作业人员劳保用品齐全，特种作业人员持证上岗",
              "作业前安全措施已确认并向全体作业人员交底",
              "已办理危险作业许可，票据随身携带",
              "现场警戒隔离到位，监护人到位并全程监护",
              "应急器材、应急预案与救援联络已落实",
              "作业后现场清理与安全设施恢复情况已检查"]
    ck = [[P("□ " + c, 9.5)] for c in checks]
    t = styled_table(ck, [W], row_heights=[8.5 * mm] * len(checks))
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, GRID), ("BOX", (0, 0), (-1, -1), 1.1, NAVY),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    s += [t, Spacer(1, 4 * mm), section_bar("审批签字", W), Spacer(1, 1.5 * mm)]

    sign = [[P("申请人/日期", 9.5, True, TA_CENTER), P("监护人/日期", 9.5, True, TA_CENTER),
             P("作业区审批人/日期", 9.5, True, TA_CENTER), P("厂级审批人/日期", 9.5, True, TA_CENTER)],
            ["", "", "", ""]]
    s += [styled_table(sign, [45 * mm] * 4, row_heights=[9 * mm, 16 * mm], header_rows=1), Spacer(1, 4 * mm),
          note("本表依据作业区《石灰危险作业台账、审批台账》（动火/高处/起重/受限空间/动土/断路/抽堵盲板/临时用电八类）字段编制；危险作业无审批、安全措施不落实按验收标准第23~24项考核。")]
    build(os.path.join(OUT, "危险作业审批表.pdf"), A4, "危险作业审批表", s)


# ============================================================
# 6. 应急救援物资台账（横向）
# ============================================================
def pdf_emergency_equipment():
    W = landscape(A4)[0] - 2 * MARGIN
    s = [title_block("石灰作业区应急救援物资装备台账",
                     "台账内容含器材位置、数量、负责人、联系电话 ｜ 定期检验、维护、保养并记录 ｜ 验收标准第31项", W),
         Spacer(1, 4 * mm)]

    head = ["序号", "器材名称", "规格型号", "数量", "存放位置", "责任人", "联系电话", "检查/维护日期", "状态"]
    data = [[P(h, 9, True, TA_CENTER) for h in head]]
    for i in range(1, 15):
        data.append([P(str(i), 9, False, TA_CENTER)] + [""] * 8)
    widths = [10 * mm, 46 * mm, 34 * mm, 14 * mm, 48 * mm, 24 * mm, 40 * mm, 30 * mm, 20 * mm]
    s += [styled_table(data, widths, row_heights=[9 * mm] + [10.5 * mm] * 14, header_rows=1), Spacer(1, 4 * mm),
          note("应覆盖：正压式空气呼吸器、CO（煤气）报警仪、灭火器、安全阀、压力表、急救箱、应急照明、三脚架与安全绳等；状态栏填写：完好 / 维修中 / 报废。")]
    build(os.path.join(OUT, "应急救援物资台账.pdf"), landscape(A4), "应急救援物资台账", s)


if __name__ == "__main__":
    pdf_confined_space()
    pdf_hazard_ledger()
    pdf_training_sign()
    pdf_bilingual_checklist()
    pdf_hazardous_permit()
    pdf_emergency_equipment()
    print("全部完成，输出目录：", OUT)
