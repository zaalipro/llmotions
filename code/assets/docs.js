/* ncode docs — search, copy buttons and the "On this page" highlight.
   Every page reads fine without this file; it only adds what needs a script. */
(function () {
  "use strict";

  /* ---- copy buttons on code blocks ---------------------------------------------------- */
  document.querySelectorAll(".code .copy").forEach(function (btn) {
    btn.hidden = false;
    btn.setAttribute("aria-live", "polite");
    btn.addEventListener("click", function () {
      var pre = btn.closest(".code").querySelector("pre");
      var text = pre.innerText.replace(/\n$/, "");
      var done = function (label) {
        btn.textContent = label;
        clearTimeout(btn._reset);
        btn._reset = setTimeout(function () { btn.textContent = "Copy"; }, 1600);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function () { done("Copied"); }, function () { select(pre); done("Press ⌘C"); });
      } else {
        select(pre);
        done("Press ⌘C");
      }
    });
  });

  function select(node) {
    var range = document.createRange();
    range.selectNodeContents(node);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }

  /* ---- search ------------------------------------------------------------------------- */
  var box = document.querySelector(".d-search");
  if (box) {
    box.hidden = false;
    var input = box.querySelector("input");
    var panel = box.querySelector(".d-hits");
    var list = panel.querySelector("ul");
    var count = document.getElementById("d-count");
    var index = null;
    var loading = null;

    var load = function () {
      if (!loading) {
        loading = fetch(box.getAttribute("data-search"), { credentials: "same-origin" })
          .then(function (r) { return r.ok ? r.json() : { pages: [] }; })
          .then(function (data) { index = data.pages || []; return index; })
          .catch(function () { index = []; return index; });
      }
      return loading;
    };

    var open = function (on) {
      panel.hidden = !on;
      input.setAttribute("aria-expanded", on ? "true" : "false");
    };

    var score = function (terms, text, weight) {
      var hay = (text || "").toLowerCase();
      var s = 0;
      for (var i = 0; i < terms.length; i++) {
        if (hay.indexOf(terms[i]) >= 0) s += weight;
      }
      return s;
    };

    var matchesAll = function (terms, text) {
      var hay = text.toLowerCase();
      for (var i = 0; i < terms.length; i++) {
        if (hay.indexOf(terms[i]) < 0) return false;
      }
      return true;
    };

    var search = function (q) {
      var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
      var hits = [];
      if (!terms.length || !index) return hits;
      index.forEach(function (page) {
        var all = [page.t, page.d, page.g].concat(page.s.map(function (s) { return s[0] + " " + s[2]; })).join(" ");
        if (!matchesAll(terms, all)) return;
        var best = { title: page.t, url: page.u, text: page.d, score: score(terms, page.t, 8) + score(terms, page.d, 3) };
        page.s.forEach(function (s) {
          if (!s[1]) return;
          var sc = score(terms, s[0], 5) + score(terms, s[2], 1);
          if (sc > 0) hits.push({ title: page.t + " › " + s[0], url: page.u + "#" + s[1], text: s[2], score: sc });
        });
        hits.push(best);
      });
      hits.sort(function (a, b) { return b.score - a.score; });
      return hits.slice(0, 8);
    };

    var render = function () {
      var q = input.value.trim();
      list.textContent = "";
      if (!q) { open(false); count.textContent = ""; return; }
      var hits = search(q);
      if (!hits.length) {
        var li = document.createElement("li");
        li.className = "none";
        li.textContent = "Nothing matches “" + q + "”.";
        list.appendChild(li);
      }
      hits.forEach(function (hit) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = hit.url;
        var b = document.createElement("b");
        b.textContent = hit.title;
        var span = document.createElement("span");
        span.textContent = hit.text || "";
        a.appendChild(b);
        a.appendChild(span);
        li.appendChild(a);
        list.appendChild(li);
      });
      count.textContent = hits.length ? hits.length + " results" : "No results";
      open(true);
    };

    input.addEventListener("focus", load);
    input.addEventListener("input", function () { load().then(render); });
    box.addEventListener("keydown", function (e) {
      var links = Array.prototype.slice.call(list.querySelectorAll("a"));
      var at = links.indexOf(document.activeElement);
      if (e.key === "Escape") {
        if (!panel.hidden) { open(false); input.focus(); e.preventDefault(); }
        else if (input.value) { input.value = ""; render(); e.preventDefault(); }
      } else if (e.key === "ArrowDown" && links.length) {
        links[Math.min(at + 1, links.length - 1)].focus();
        e.preventDefault();
      } else if (e.key === "ArrowUp" && at >= 0) {
        (at === 0 ? input : links[at - 1]).focus();
        e.preventDefault();
      } else if (e.key === "Enter" && document.activeElement === input && links.length) {
        window.location.href = links[0].href;
      }
    });
    box.addEventListener("focusout", function (e) {
      if (!box.contains(e.relatedTarget)) open(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key !== "/" || e.metaKey || e.ctrlKey || e.altKey) return;
      var t = e.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      e.preventDefault();
      input.focus();
    });
  }

  /* ---- "On this page": mark the section being read -------------------------------------- */
  var toc = document.querySelector(".d-toc");
  if (toc && "IntersectionObserver" in window) {
    var links = {};
    toc.querySelectorAll("a[href^='#']").forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
    var current = null;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var link = links[entry.target.id];
        if (!link) return;
        if (current) current.classList.remove("on");
        link.classList.add("on");
        current = link;
      });
    }, { rootMargin: "-70px 0px -70% 0px" });
    document.querySelectorAll(".d-article h2[id], .d-article h3[id]").forEach(function (h) { observer.observe(h); });
  }
})();
