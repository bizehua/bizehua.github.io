/* ============================================================
   在线模拟考试引擎（纯前端，数据来自 assets/data/questions.json）
   功能：试卷选择 / 随机抽题 / 倒计时 / 题卡导航 / 自动评分 /
        错题解析 / 成绩本地留存 / 合格线 80 分
   ============================================================ */
(function () {
  "use strict";

  var PASS = 80;               // 合格线
  var EXAM_MINUTES = 30;       // 考试时长（分钟）
  var LS_KEY = "lime-kiln-quiz-records";

  var state = {
    set: null,        // 当前试卷对象
    list: [],         // 乱序后的题目
    idx: 0,           // 当前题号
    answers: {},      // {qid: [optionIndex...]}
    startTime: 0,
    timerId: null,
    remain: 0,
    submitted: false,
    ms: {}            // 马来文对照数据 {qid: {q, o, e}}
  };

  var $ = function (id) { return document.getElementById(id); };

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function fmtTime(s) {
    var m = Math.floor(s / 60), r = s % 60;
    return (m < 10 ? "0" + m : m) + ":" + (r < 10 ? "0" + r : r);
  }

  function getRecords() {
    try { return JSON.parse(localStorage.getItem(LS_KEY) || "{}"); } catch (e) { return {}; }
  }
  function saveRecord(setId, score, passed) {
    try {
      var rec = getRecords();
      var old = rec[setId] || { best: 0, count: 0 };
      rec[setId] = {
        best: Math.max(old.best || 0, score),
        last: score,
        count: (old.count || 0) + 1,
        passed: passed,
        date: new Date().toISOString().slice(0, 10)
      };
      localStorage.setItem(LS_KEY, JSON.stringify(rec));
    } catch (e) { }
  }

  var TYPE_LABEL = { single: "单选题", multi: "多选题", judge: "判断题" };
  var TYPE_LABEL_MS = { single: "Soalan Tunggal", multi: "Soalan Berganda", judge: "Soalan Betul/Salah" };

  /* ---------- 试卷选择 ---------- */
  function renderSetSelect(data) {
    var rec = getRecords();
    var html = "";
    data.sets.forEach(function (s) {
      var r = rec[s.id];
      var recHtml = r
        ? '<div class="set-tags"><span class="badge ok">历史最高 Tertinggi ' + r.best + " 分</span><span class=\"badge info\">已考 " + r.count + " 次</span>" + (r.passed ? '<span class="badge ok">已通过 Lulus</span>' : '<span class="badge warn">未通过 Gagal</span>') + "</div>"
        : '<div class="set-tags"><span class="badge info">共 ' + s.questions.length + ' 题 Soalan</span><span class="badge info">限时 Masa ' + EXAM_MINUTES + ' 分钟 Minit</span><span class="badge warn">合格线 Lulus ' + PASS + ' 分 Markah</span></div>';
      html +=
        '<button class="set-card" data-set="' + s.id + '">' +
        "<h4>" + s.name + "</h4><p>" + s.desc + "</p>" + recHtml + "</button>";
    });
    $("setList").innerHTML = html;
    Array.prototype.forEach.call($("setList").querySelectorAll(".set-card"), function (btn) {
      btn.addEventListener("click", function () {
        var s = data.sets.filter(function (x) { return x.id === btn.getAttribute("data-set"); })[0];
        startExam(s);
      });
    });
  }

  /* ---------- 开始考试 ---------- */
  function startExam(set) {
    state.set = set;
    state.list = shuffle(set.questions);
    state.idx = 0;
    state.answers = {};
    state.submitted = false;
    state.startTime = Date.now();
    state.remain = EXAM_MINUTES * 60;

    $("quizSelect").style.display = "none";
    $("quizExam").style.display = "";
    $("quizResult").style.display = "none";
    $("examTitle").textContent = set.name;

    clearInterval(state.timerId);
    state.timerId = setInterval(tick, 1000);
    updateTimer();
    renderQuestion();
    renderNavGrid();
  }

  function tick() {
    state.remain--;
    if (state.remain <= 0) {
      state.remain = 0;
      updateTimer();
      clearInterval(state.timerId);
      submitExam(true);
      return;
    }
    updateTimer();
  }

  function updateTimer() {
    var el = $("timer");
    el.textContent = fmtTime(state.remain);
    if (state.remain <= 300) el.classList.add("warn");
    else el.classList.remove("warn");
    var done = Object.keys(state.answers).length;
    $("progressText").innerHTML = "已答 Dijawab " + done + " / " + state.list.length;
    $("progressBar").style.width = (done / state.list.length * 100) + "%";
  }

  /* ---------- 渲染题目 ---------- */
  function renderQuestion() {
    var q = state.list[state.idx];
    var ms = state.ms[q.id] || {};
    var msOpts = ms.o || [];
    var chosen = state.answers[q.id] || [];
    var html =
      '<div class="q-card"><div class="q-head">' +
      '<span class="q-type ' + q.type + '">' + TYPE_LABEL[q.type] + " " + (TYPE_LABEL_MS[q.type] || "") + "</span>" +
      '<span class="q-title">' + (state.idx + 1) + ". " + q.q +
      (ms.q ? '<span class="ms">' + ms.q + "</span>" : "") + "</span></div>" +
      '<div class="q-options">';
    q.options.forEach(function (opt, i) {
      var cls = "q-opt" + (chosen.indexOf(i) !== -1 ? " selected" : "");
      html += '<button class="' + cls + '" data-opt="' + i + '"><span class="opt-key">' +
        "ABCDEFGH".charAt(i) + '</span><span>' + opt +
        (msOpts[i] ? '<span class="ms">' + msOpts[i] + "</span>" : "") + "</span></button>";
    });
    html += "</div>";
    if (q.type === "multi") html += '<p class="muted mt-8">多选题：可选择多个选项，确认无误后继续。／Soalan berganda: boleh pilih beberapa pilihan.</p>';
    html += '<div class="q-nav">' +
      '<button class="btn ghost" id="btnPrev"' + (state.idx === 0 ? " disabled" : "") + ">← 上一题 Sebelum</button>" +
      '<div class="spacer"></div>' +
      (state.idx === state.list.length - 1
        ? '<button class="btn danger" id="btnSubmit">交卷 Hantar</button>'
        : '<button class="btn" id="btnNext">下一题 Seterusnya →</button>') +
      "</div></div>";
    $("questionBox").innerHTML = html;

    Array.prototype.forEach.call($("questionBox").querySelectorAll(".q-opt"), function (btn) {
      btn.addEventListener("click", function () { choose(parseInt(btn.getAttribute("data-opt"), 10)); });
    });
    var prev = $("btnPrev"); if (prev) prev.addEventListener("click", function () { goto(state.idx - 1); });
    var next = $("btnNext"); if (next) next.addEventListener("click", function () { goto(state.idx + 1); });
    var sub = $("btnSubmit"); if (sub) sub.addEventListener("click", function () { submitExam(false); });

    renderNavGrid();
  }

  function choose(i) {
    var q = state.list[state.idx];
    var chosen = state.answers[q.id] || [];
    if (q.type === "multi") {
      var pos = chosen.indexOf(i);
      if (pos === -1) chosen.push(i); else chosen.splice(pos, 1);
      chosen.sort();
    } else {
      chosen = [i];
    }
    state.answers[q.id] = chosen;
    renderQuestion();
    updateTimer();
  }

  function goto(i) {
    if (i < 0 || i >= state.list.length) return;
    state.idx = i;
    renderQuestion();
  }

  /* ---------- 题卡导航 ---------- */
  function renderNavGrid() {
    var html = "";
    state.list.forEach(function (q, i) {
      var done = state.answers[q.id] ? " done" : "";
      var cur = i === state.idx ? " current" : "";
      html += '<button class="' + done + cur + '" data-i="' + i + '">' + (i + 1) + "</button>";
    });
    $("navGrid").innerHTML = html;
    Array.prototype.forEach.call($("navGrid").querySelectorAll("button"), function (btn) {
      btn.addEventListener("click", function () { goto(parseInt(btn.getAttribute("data-i"), 10)); });
    });
  }

  /* ---------- 交卷评分 ---------- */
  function submitExam(auto) {
    var unanswered = state.list.length - Object.keys(state.answers).length;
    if (!auto && unanswered > 0) {
      if (!confirm("还有 " + unanswered + " 题未作答，确定交卷吗？／Masih " + unanswered + " soalan belum dijawab, hantar sekarang?")) return;
    }
    if (state.submitted) return;
    state.submitted = true;
    clearInterval(state.timerId);

    var correct = 0;
    state.list.forEach(function (q) {
      var ans = (state.answers[q.id] || []).slice().sort();
      var key = q.answer.slice().sort();
      if (ans.length === key.length && ans.every(function (v, i) { return v === key[i]; })) correct++;
    });
    var score = Math.round(correct / state.list.length * 100);
    var passed = score >= PASS;
    saveRecord(state.set.id, score, passed);

    var used = EXAM_MINUTES * 60 - state.remain;
    $("scoreVal").textContent = score;
    $("scoreVal").className = "score " + (passed ? "pass" : "fail");
    $("verdict").textContent = passed ? "✓ 合格 LULUS" : "✕ 未合格（合格线 " + PASS + " 分）GAGAL";
    $("verdict").style.color = passed ? "var(--c-ok)" : "var(--c-danger)";
    $("resultMeta").innerHTML =
      "答对 <b>" + correct + "</b> / " + state.list.length + " 题 Betul ｜ 用时 <b>" + fmtTime(used) + "</b>" +
      (auto ? " ｜ <span style='color:var(--c-danger)'>考试时间到，已自动交卷 Masa tamat, hantar automatik</span>" : "");

    var rev = "";
    state.list.forEach(function (q, i) {
      var ms = state.ms[q.id] || {};
      var msOpts = ms.o || [];
      var ans = (state.answers[q.id] || []).slice().sort();
      var key = q.answer.slice().sort();
      var ok = ans.length === key.length && ans.every(function (v, j) { return v === key[j]; });
      var opts = q.options.map(function (o, oi) {
        var cls = "q-opt";
        if (key.indexOf(oi) !== -1) cls += " correct";
        else if (ans.indexOf(oi) !== -1) cls += " wrong";
        return '<div class="' + cls + '" style="cursor:default"><span class="opt-key">' + "ABCDEFGH".charAt(oi) + "</span><span>" + o +
          (msOpts[oi] ? '<span class="ms">' + msOpts[oi] + "</span>" : "") + "</span></div>";
      }).join("");
      var userAns = ans.length ? ans.map(function (a) { return "ABCDEFGH".charAt(a); }).join("") : "未作答 Tiada";
      rev +=
        '<div class="panel mt-14"><div class="panel-pad">' +
        '<div class="q-head"><span class="q-type ' + q.type + '">' + TYPE_LABEL[q.type] + " " + (TYPE_LABEL_MS[q.type] || "") + "</span>" +
        '<span class="q-title">' + (i + 1) + ". " + q.q + (ms.q ? '<span class="ms">' + ms.q + "</span>" : "") + "</span>" +
        (ok ? '<span class="badge ok" style="margin-left:auto">✓ 正确</span>' : '<span class="badge danger" style="margin-left:auto">✕ 错误</span>') + "</div>" +
        '<p class="muted" style="font-size:12.5px">你的答案 Jawapan anda：' + userAns + " ｜ 正确答案：" + key.map(function (a) { return "ABCDEFGH".charAt(a); }).join("") + "</p>" +
        '<div class="q-options mt-8">' + opts + "</div>" +
        '<div class="q-explain"><b>解析 Penjelasan：</b>' + q.explain + (ms.e ? '<span class="ms">' + ms.e + "</span>" : "") + "</div></div></div>";
    });
    $("reviewBox").innerHTML = rev;

    $("quizExam").style.display = "none";
    $("quizResult").style.display = "";
    $("quizResult").scrollIntoView({ behavior: "smooth" });
  }

  /* ---------- 初始化 ---------- */
  document.addEventListener("DOMContentLoaded", function () {
    Promise.all([
      fetch("../assets/data/questions.json").then(function (r) { return r.json(); }),
      fetch("../assets/data/questions-ms.json").then(function (r) { return r.json(); }).catch(function () { return {}; })
    ])
      .then(function (res) {
        var data = res[0];
        state.ms = res[1] || {};
        $("quizNote").textContent = data.meta.note;
        renderSetSelect(data);
        var sideBtn = $("btnSubmitSide");
        if (sideBtn) sideBtn.addEventListener("click", function () { submitExam(false); });
        if (window.refreshMotion) window.refreshMotion();
        $("btnAgain").addEventListener("click", function () {
          $("quizResult").style.display = "none";
          $("quizSelect").style.display = "";
          renderSetSelect(data);
        });
        $("btnPrintReview").addEventListener("click", function () { window.print(); });
      })
      .catch(function () {
        $("setList").innerHTML = '<div class="alert danger"><span class="a-icon">✕</span><div>题库数据加载失败，请确认 assets/data/questions.json 文件存在。</div></div>';
      });
  });
})();
