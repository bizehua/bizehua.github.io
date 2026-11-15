/* ============================================================
   全站框架脚本 v4（中马双语）
   页头/导航/页脚统一注入 · 主题切换 · 动画系统 · 移动端底部导航
   后续接后台：只改 SITE_CONFIG 与 NAV_ITEMS 两处配置
   ============================================================ */
(function () {
  "use strict";

  /* ---------- 全站配置（中马双语） ---------- */
  var SITE_CONFIG = {
    title: "东钢焦电部石灰作业区",
    footerTitle: "东钢焦电部安全生产培训.石灰标准化作业区建设平台",
    subtitle: "SAFETY TRAINING · STANDARDIZED WORK ZONE ｜ LATIHAN KESELAMATAN · KAWASAN KERJA STANDARD",
    footerNote: "本站为焦电部石灰作业区内部安全生产培训与标准化建设平台，课程内容依据作业区安全规程、操作规程、应急预案及管理制度等实际文件编制，中马双语对照，仅供内部学习使用。<span class='ms'>Laman dalaman untuk latihan keselamatan & pembinaan standard kawasan kapur Jabatan Kok & Kuasa; kandungan berdasarkan prosedur keselamatan, prosedur operasi, pelan kecemasan dan sistem pengurusan sebenar — dwibahasa Cina–Melayu, untuk kegunaan pembelajaran dalaman sahaja.</span>",
    footerBottom: "东钢焦电部 · 石灰作业区 ｜ 安全生产 预防为主 ｜ 学习进度与成绩存储于本地浏览器 ｜ Jabatan Kok &amp; Kuasa · Kawasan Kapur ｜ Keselamatan pengeluaran, pencegahan utama ｜ Kemajuan &amp; markah disimpan dalam pelayar"
  };

  var NAV_ITEMS = [
    { label: "首页", ms: "Laman Utama", href: "index.html" },
    { label: "课程库", ms: "Katalog Kursus", href: "pages/courses.html" },
    {
      label: "安全学习", ms: "Keselamatan", href: "pages/safety.html", flag: "重点", group: [
        { label: "安全基础知识", ms: "Asas Keselamatan", href: "pages/safety-basics.html" },
        { label: "安全培训课程", ms: "Kursus Latihan", href: "pages/training.html" },
        { label: "在线模拟考试", ms: "Peperiksaan", href: "pages/quiz.html" },
        { label: "工艺风险知识库", ms: "Pangkalan Risiko", href: "pages/risk-library.html" },
        { label: "事故案例警示", ms: "Kes Kemalangan", href: "pages/cases.html" },
        { label: "安全作业工具", ms: "Alat Kerja", href: "pages/tools.html" },
        { label: "有限空间作业专题", ms: "Ruang Terhad", href: "pages/confined-space.html" },
        { label: "应急处置卡", ms: "Kad Kecemasan", href: "pages/emergency-cards.html" }
      ]
    },
    { label: "石灰窑工艺高风险示意图", ms: "Rajah Risiko", href: "pages/kiln-diagram.html" },
    { label: "资料下载", ms: "Muat Turun", href: "pages/downloads.html" },
    { label: "验收标准", ms: "Standard", href: "pages/standards.html" }
  ];

  var TAB_ITEMS = [
    { label: "首页", ms: "Utama", icon: "🏠", href: "index.html" },
    { label: "课程", ms: "Kursus", icon: "📚", href: "pages/courses.html" },
    { label: "考试", ms: "Exam", icon: "📝", href: "pages/quiz.html" },
    { label: "示意图", ms: "Diagram", icon: "🗺️", href: "pages/kiln-diagram.html" },
    { label: "下载", ms: "Turun", icon: "⬇️", href: "pages/downloads.html" }
  ];

  var inPages = window.location.pathname.indexOf("/pages/") !== -1;
  var P = inPages ? "../" : "";

  function isActive(href) {
    var file = href.split("/").pop();
    var cur = window.location.pathname.split("/").pop() || "index.html";
    return file === cur;
  }

  /* ---------- 主题 ---------- */
  function getTheme() {
    try { return localStorage.getItem("lime-kiln-theme") || "light"; } catch (e) { return "light"; }
  }
  function applyTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    try { localStorage.setItem("lime-kiln-theme", t); } catch (e) { }
    var btn = document.getElementById("themeToggle");
    if (btn) btn.textContent = t === "dark" ? "☀️" : "🌙";
  }
  function toggleTheme() { applyTheme(getTheme() === "dark" ? "light" : "dark"); }

  /* ---------- 框架渲染 ---------- */
  function renderShell() {
    applyTheme(getTheme());

    var headerEl = document.getElementById("app-header");
    if (headerEl) {
      var navHtml = NAV_ITEMS.map(function (it) {
        if (it.group) {
          var sub = it.group.map(function (g) {
            return '<a href="' + P + g.href + '"><span class="g-dot"></span>' + g.label + (g.ms ? '<span class="ms">' + g.ms + '</span>' : '') + '</a>';
          }).join("");
          return '<div class="nav-group"><a class="nav-link' + (isActive(it.href) ? " active" : "") +
            '" href="' + P + it.href + '" title="' + it.ms + '">' + it.label +
            (it.ms ? '<span class="nav-ms">' + it.ms + '</span>' : '') +
            '<span class="nav-flag">' + it.flag + "</span> ▾</a>" +
            '<div class="nav-group-menu">' + sub + "</div></div>";
        }
        return '<a class="nav-link' + (isActive(it.href) ? " active" : "") + '" href="' + P + it.href + '" title="' + it.ms + '">' + it.label + (it.ms ? '<span class="nav-ms">' + it.ms + '</span>' : '') + "</a>";
      }).join("");

      headerEl.innerHTML =
        '<div class="hazard-stripe"></div>' +
        '<header class="site-header"><div class="header-inner">' +
        '<a class="logo-mark" href="' + P + 'index.html" title="返回首页 / Laman Utama">' +
        '<img src="' + P + 'assets/img/logo.png" alt="东钢集团 Eastern Steel" class="logo-img">' +
        "</a>" +
        "<div><div class=\"site-title\">" + SITE_CONFIG.title + "</div>" +
        "<div class=\"site-subtitle\">" + SITE_CONFIG.subtitle + "</div></div>" +
        '<div class="header-actions">' +
        '<button class="icon-btn" id="themeToggle" title="切换深浅色主题 / Tukar Tema" aria-label="切换主题">🌙</button>' +
        "</div></div></header>" +
        '<nav class="site-nav"><div class="nav-inner">' + navHtml + "</div></nav>";

      /* 顶部品牌条与页面大标题重复 → 全站移除该条；
         LOGO 下放到正文：首页放进 hero 顶部，内页放在面包屑上方；
         主题按钮移入导航右侧，保持可用 */
      var heroEl = document.querySelector(".hero");
      var headerNode = headerEl.querySelector(".site-header");
      if (headerNode) {
        var logoNode = headerNode.querySelector(".logo-mark");
        var toggleBtn = headerNode.querySelector("#themeToggle");
        var navInner = headerEl.querySelector(".nav-inner");

        if (logoNode) {
          var brand = document.createElement("div");
          if (heroEl) {
            brand.className = "hero-brand";
            brand.appendChild(logoNode);
            heroEl.insertBefore(brand, heroEl.firstChild);
            document.body.classList.add("has-hero");
          } else {
            var pageEl = document.querySelector("main.page");
            if (pageEl) {
              brand.className = "page-brand";
              brand.appendChild(logoNode);
              pageEl.insertBefore(brand, pageEl.firstChild);
            }
          }
        }

        if (toggleBtn && navInner) {
          var themeBox = document.createElement("div");
          themeBox.className = "nav-theme";
          themeBox.appendChild(toggleBtn);
          navInner.appendChild(themeBox);
        }

        headerNode.parentNode.removeChild(headerNode);
        document.body.classList.add("no-brand");
      }

      var tt = document.getElementById("themeToggle");
      if (tt) tt.addEventListener("click", toggleTheme);
      applyTheme(getTheme());
    }

    var tabEl = document.getElementById("app-tabbar");
    if (tabEl) {
      tabEl.innerHTML = TAB_ITEMS.map(function (t) {
        return '<a class="' + (isActive(t.href) ? "active" : "") + '" href="' + P + t.href + '" title="' + t.ms + '">' +
          '<span class="t-icon">' + t.icon + "</span>" + t.label + '<span class="tab-ms">' + t.ms + "</span></a>";
      }).join("");
    }

    var footEl = document.getElementById("app-footer");
    if (footEl) {
      footEl.innerHTML =
        '<footer class="site-footer"><div class="footer-inner">' +
        "<div><div class=\"footer-brand\">" + SITE_CONFIG.footerTitle + "</div>" +
        '<div class="footer-brand-sub">' + SITE_CONFIG.footerNote + "</div></div>" +
        "<div><h5>课程学习 Kursus</h5>" +
        '<a href="' + P + 'pages/courses.html">课程库总览<span class="ms">Katalog</span></a>' +
        '<a href="' + P + 'pages/hr.html">人员管理<span class="ms">Personel</span></a>' +
        '<a href="' + P + 'pages/equipment.html">设备管理<span class="ms">Peralatan</span></a>' +
        '<a href="' + P + 'pages/process.html">工艺管理<span class="ms">Proses</span></a></div>' +
        "<div><h5>安全学习 Keselamatan</h5>" +
        '<a href="' + P + 'pages/training.html">安全培训课程<span class="ms">Kursus</span></a>' +
        '<a href="' + P + 'pages/quiz.html">在线模拟考试<span class="ms">Peperiksaan</span></a>' +
        '<a href="' + P + 'pages/risk-library.html">工艺风险知识库<span class="ms">Risiko</span></a>' +
        '<a href="' + P + 'pages/cases.html">事故案例警示<span class="ms">Kes</span></a>' +
        '<a href="' + P + 'pages/emergency-cards.html">应急处置卡<span class="ms">Kecemasan</span></a></div>' +
        "<div><h5>标准与资料 Standard</h5>" +
        '<a href="' + P + 'pages/standards.html">验收标准（参考）<span class="ms">Standard</span></a>' +
        '<a href="' + P + 'pages/downloads.html">资料下载<span class="ms">Muat turun</span></a>' +
        '<a href="' + P + 'pages/tools.html">安全作业工具<span class="ms">Alat kerja</span></a></div>' +
        "</div><div class=\"footer-bottom\">" + SITE_CONFIG.footerBottom + "</div></footer>";
    }

    initMotion();
  }

  /* ---------- 动画系统 ---------- */
  var observer = null;
  function initMotion() {
    var bar = document.createElement("div");
    bar.className = "read-progress";
    document.body.appendChild(bar);
    var top = document.createElement("button");
    top.className = "back-top";
    top.innerHTML = "↑";
    top.setAttribute("aria-label", "返回顶部");
    top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
    document.body.appendChild(top);

    function onScroll() {
      var h = document.documentElement;
      var pct = h.scrollTop / (h.scrollHeight - h.clientHeight) * 100;
      bar.style.width = (pct || 0) + "%";
      top.classList.toggle("show", h.scrollTop > 420);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    if ("IntersectionObserver" in window) {
      observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add("revealed");
            countUp(en.target);
            observer.unobserve(en.target);
          }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
      scanReveal();
    } else {
      document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("revealed"); });
      document.querySelectorAll("[data-count]").forEach(function (el) {
        el.textContent = el.getAttribute("data-count");
      });
    }
  }

  function countUp(scope) {
    var els = [];
    if (scope.querySelectorAll) els = Array.prototype.slice.call(scope.querySelectorAll("[data-count]"));
    if (scope.hasAttribute && scope.hasAttribute("data-count")) els.push(scope);
    els.forEach(function (el) {
      if (el.getAttribute("data-counted")) return;
      el.setAttribute("data-counted", "1");
      var target = parseInt(el.getAttribute("data-count"), 10) || 0;
      var t0 = null, dur = 900;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased);
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }

  function scanReveal() {
    var sels = ".section, .board-card, .course-card, .risk-card, .tool-item, .step-node, .emergency-card, .case-card, .hstat, .lesson-block, .filter-bar, .set-card";
    document.querySelectorAll(sels).forEach(function (el, i) {
      if (el.classList.contains("reveal")) return;
      el.classList.add("reveal");
      var d = (i % 6) + 1;
      if (d > 1) el.classList.add("reveal-d" + Math.min(d, 6));
      if (observer) observer.observe(el);
    });
  }

  /* 暴露给动态渲染页面调用 */
  window.refreshMotion = function () { if (observer) scanReveal(); };

  /* 双语文本工具：字段可能是字符串或 {zh, ms} */
  window.bil = function (v) {
    if (v && typeof v === "object") return v.zh || "";
    return v || "";
  };
  window.bilMs = function (v) {
    if (v && typeof v === "object") return v.ms || "";
    return "";
  };

  document.addEventListener("DOMContentLoaded", renderShell);
})();
