/* ============================================================
   麦尔兹双膛窑石灰窑工艺高风险示意图交互
   高风险区域热点点击 → 右侧显示风险详情；图例按类别筛选高亮
   ============================================================ */
(function () {
  "use strict";

  var ZONES = {
    co1: {
      cat: "co", title: "煤气管网 · 加压机 · 眼睛阀",
      feature: [
        "厂区转炉煤气（富CO）经管网进入作业区，经加压机升压后送往窑体烧嘴",
        "管道法兰、阀门、眼睛阀为典型泄漏点，CO无色无味，吸入可迅速致昏迷",
        "现场曾多次在石灰入户转炉煤气眼睛阀处进行抽堵盲板作业（动火调整）"
      ],
      controls: [
        "固定式CO报警仪+便携式报警仪双重监测，报警立即撤离",
        "煤气作业办理危险作业许可，佩戴正压式空气呼吸器",
        "警戒区禁火种、非防爆电器，使用铜质防爆工具",
        "眼睛阀、水封、放散阀按点检标准每班检查并记录"
      ]
    },
    co2: {
      cat: "co", title: "烧嘴 · 燃烧通道",
      feature: [
        "转炉煤气经烧嘴喷入燃烧通道与窑膛，燃烧期火焰温度超1100℃",
        "烧嘴堵塞、回火、煤气泄漏可导致着火、爆炸与中毒",
        "轮换换向期间煤气侧均存在残余煤气"
      ],
      controls: [
        "烧嘴区域为CO高风险区，作业必须双人监护",
        "换向（燃烧期↔蓄热期）操作严格执行操作规程，确认阀门状态",
        "煤气水封每班检查，保持正常水封高度"
      ]
    },
    co3: {
      cat: "co", title: "窑膛内部（燃烧期）",
      feature: [
        "燃烧期窑膛内充满火焰与高温废气，CO含量高",
        "停窑后窑膛内残留煤气与废气，人员进入有中毒、窒息风险",
        "属典型有限空间：缺氧、CO残留、高温、粉尘多重叠加"
      ],
      controls: [
        "进入窑膛必须按有限空间作业管理：审批、通风、检测、监护",
        "检测氧含量19.5%~23.5%、CO不超标后方可进入",
        "佩戴正压式空气呼吸器，外部设专人监护并保持联络"
      ]
    },
    h1: {
      cat: "heat", title: "窑体表面",
      feature: [
        "煅烧区物料温度1100~1200℃，窑体表面可达200℃以上",
        "外壳隔热局部缺损部位温度更高，误触可致严重灼烫",
        "窑体测温点检每班执行并记录数字"
      ],
      controls: [
        "窑体附近作业穿隔热防护服、戴隔热手套",
        "高温部位设置警示标识与隔离，严禁随意倚靠、触碰",
        "窑体检查、清疤作业停机降温后进行"
      ]
    },
    h2: {
      cat: "heat", title: "高温烟气管道 · 换热器",
      feature: [
        "窑膛排出的高温烟气（数百度）经管道进入换热器加热助燃空气",
        "管道膨胀节、法兰、蝶阀为泄漏与变形高发点",
        "表面灼烫风险叠加高空作业风险"
      ],
      controls: [
        "管道保温完好，缺损及时修复并挂牌警示",
        "高温管道附近作业办理高处作业许可，安全带高挂低用",
        "停机降温并检测合格后方可进入管道内部"
      ]
    },
    h3: {
      cat: "heat", title: "出灰机 · 热灰区域",
      feature: [
        "煅烧完成的石灰经出灰机排出，温度数百度",
        "热灰喷溅、粉尘飞扬可致灼烫与粉尘危害",
        "清理堵料、检查阀板时最易发生灼烫"
      ],
      controls: [
        "出灰区域作业穿隔热服、戴防护面罩与手套",
        "停机、断电、挂牌后方可清理与检查",
        "保持通道畅通，热灰积水区域设置警戒防蒸汽烫伤"
      ]
    },
    c1: {
      cat: "confined", title: "窑膛内部（检修进入）",
      feature: [
        "窑膛为作业区核心有限空间之一，已建立有限空间台账",
        "进入人员面临缺氧、CO残留、高温余热、粉尘与坠落风险",
        "作业内容：耐材检查修补、内衬清理、设备检修"
      ],
      controls: [
        "严格执行有限空间作业审批与“先通风、再检测、后作业”",
        "作业负责人、监护人、作业人员、应急救援人员全部告知交底并培训考试",
        "作业前、作业过程、作业后均进行气体检测，记录存档"
      ]
    },
    c2: {
      cat: "confined", title: "布袋/电除尘器内部",
      feature: [
        "除尘器收集窑尾粉尘，内部积灰、缺氧、CO残留风险叠加",
        "布袋更换、净气室检修、灰斗清灰均属有限空间作业",
        "人员进入曾发生晕倒险肇事故，须高度警惕"
      ],
      controls: [
        "建立有限空间作业台账，办理审批后方可进入",
        "强制通风置换，检测合格，佩戴正压式空气呼吸器",
        "外部全程监护，应急救援器材（三脚架、安全绳、呼吸器）到位"
      ]
    },
    c3: {
      cat: "confined", title: "烟道 · 引风机管道",
      feature: [
        "烟道截面大、距离长，通风死角多，残存CO与高温",
        "膨胀节检修、清灰、内衬检查时人员需进入",
        "风机蜗壳内部同样按有限空间管理"
      ],
      controls: [
        "进入前切断风机电源，挂牌警示",
        "多点位检测（上、中、下）合格后方可进入",
        "作业中断后再次进入必须重新通风检测"
      ]
    },
    g1: {
      cat: "general", title: "上料系统",
      feature: [
        "石灰石经料仓称量、斗提机与皮带上料至布料装置",
        "运转部位夹碾、高处落料为主要风险"
      ],
      controls: [
        "运转部位防护罩齐全，作业前停机断电挂牌",
        "严禁跨越运行中的皮带，严禁在皮带运转时清理",
        "上料区域粉尘作业佩戴防尘口罩"
      ]
    },
    g2: {
      cat: "general", title: "控制室 · 监测系统",
      feature: [
        "DCS监控双膛换向、温度、压力、CO浓度等关键参数",
        "重要参数测量、远传、连续记录是危险源管控的核心措施"
      ],
      controls: [
        "CO报警信号、温度压力异常立即核实并按规定上报",
        "操作记录真实完整，严禁弄虚作假",
        "控制室保持应急通道畅通，张贴应急联络卡"
      ]
    },
    g3: {
      cat: "general", title: "石灰输送 · 成品库",
      feature: [
        "成品石灰经皮带、斗提机送入成品库，装车外运",
        "车辆伤害、机械伤害、粉尘为主要风险"
      ],
      controls: [
        "库区人车分流，限速行驶，设置警示标识",
        "装车作业人员站在侧风向，佩戴防尘用品",
        "保持库区通道与消防通道畅通"
      ]
    }
  };

  var CATS = {
    co: { name: "CO 高风险区", color: "#b71c1c", desc: "煤气泄漏 · 中毒 · 爆炸" },
    heat: { name: "高温灼烫区", color: "#e65100", desc: "窑体 · 烟气 · 热灰" },
    confined: { name: "有限空间", color: "#f9a825", desc: "窑膛 · 除尘 · 烟道" },
    general: { name: "一般巡检区域", color: "#2c5282", desc: "上料 · 控制 · 成品" }
  };

  function showZone(id) {
    var z = ZONES[id];
    if (!z) return;
    var cat = CATS[z.cat];
    document.querySelectorAll(".hotspot").forEach(function (h) { h.classList.remove("active"); });
    var el = document.querySelector('[data-zone="' + id + '"]');
    if (el) el.classList.add("active");
    document.getElementById("ziDot").style.background = cat.color;
    var zms = (window.ZONES_MS || {})[id] || {};
    var cMs = (window.CATS_MS || {})[z.cat] || {};
    document.getElementById("ziTitle").innerHTML = z.title +
      (zms.title ? '<span class="ms">' + zms.title + "</span>" : "");
    document.getElementById("ziCat").innerHTML = cat.name +
      (cMs.name ? '<span class="ms">' + cMs.name + "</span>" : "");
    document.getElementById("ziCat").style.color = cat.color;
    document.getElementById("ziCat").style.borderColor = cat.color;
    var fMs = zms.feature || [], cMs2 = zms.controls || [];
    document.getElementById("ziFeature").innerHTML = z.feature.map(function (f, i) {
      return "<li>" + f + (fMs[i] ? '<span class="ms">' + fMs[i] + "</span>" : "") + "</li>";
    }).join("");
    document.getElementById("ziControls").innerHTML = z.controls.map(function (c, i) {
      return "<li>" + c + (cMs2[i] ? '<span class="ms">' + cMs2[i] + "</span>" : "") + "</li>";
    }).join("");
  }

  function filterCat(cat) {
    document.querySelectorAll(".hotspot").forEach(function (h) {
      if (!cat) { h.classList.remove("dim"); return; }
      var id = h.getAttribute("data-zone");
      h.classList.toggle("dim", ZONES[id] && ZONES[id].cat !== cat);
    });
    var first = null;
    document.querySelectorAll(".hotspot").forEach(function (h) {
      var id = h.getAttribute("data-zone");
      if (!first && (!cat || (ZONES[id] && ZONES[id].cat === cat))) first = id;
    });
    if (first) showZone(first);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".hotspot").forEach(function (h) {
      h.addEventListener("click", function () {
        document.querySelectorAll(".hotspot").forEach(function (x) { x.classList.remove("dim"); });
        showZone(h.getAttribute("data-zone"));
      });
    });
    document.querySelectorAll("[data-cat]").forEach(function (row) {
      row.addEventListener("click", function () {
        var cat = row.getAttribute("data-cat");
        var already = row.classList.contains("on");
        document.querySelectorAll("[data-cat]").forEach(function (r) { r.classList.remove("on"); });
        if (already) { filterCat(null); } else { row.classList.add("on"); filterCat(cat); }
      });
    });
    showZone("co1");
  });
})();
