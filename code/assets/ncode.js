/* ncode landing — the copy button, the page's own progress bar, the run card's clock, the mode showcase and its lightbox.
   The page reads the same without this file. Nothing here loads a library. */
(function () {
  "use strict";
  var reduce = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };

  /* copy the install line */
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    var target = document.getElementById(btn.getAttribute("data-copy"));
    if (!target) return;
    btn.hidden = false;
    btn.setAttribute("aria-live", "polite");
    btn.addEventListener("click", function () {
      var text = target.textContent.trim();
      var done = function (label) {
        btn.textContent = label;
        clearTimeout(btn._reset);
        btn._reset = setTimeout(function () { btn.textContent = "Copy"; }, 1600);
      };
      var select = function () {
        var range = document.createRange();
        range.selectNodeContents(target);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        done("Press ⌘C");
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function () { done("Copied"); }, select);
      } else {
        select();
      }
    });
  });

  /* the page has a progress bar too */
  var bar = document.querySelector(".nc-progress span");
  if (bar) {
    var queued = false;
    var paint = function () {
      queued = false;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.setProperty("--read", max > 0 ? Math.min(1, window.scrollY / max).toFixed(4) : "0");
    };
    var ask = function () {
      if (!queued) { queued = true; window.requestAnimationFrame(paint); }
    };
    window.addEventListener("scroll", ask, { passive: true });
    window.addEventListener("resize", ask, { passive: true });
    paint();
  }

  /* the run card keeps time while it is on screen; never with reduced motion */
  var card = document.querySelector("[data-live]");
  if (card && "IntersectionObserver" in window) {
    var clock = card.querySelector("[data-clock]");
    var spins = card.querySelectorAll("[data-spin]");
    var secs = parseInt(clock.getAttribute("data-clock"), 10) || 0;
    var frames = ["◐", "◓", "◑", "◒"];
    var frame = 0;
    var timer = null;
    var visible = false;
    var tick = function () {
      secs += 1;
      frame = (frame + 1) % frames.length;
      var s = secs % 60;
      clock.textContent = Math.floor(secs / 60) + ":" + (s < 10 ? "0" : "") + s;
      spins.forEach(function (el) { el.textContent = frames[frame]; });
    };
    var sync = function () {
      var run = visible && !document.hidden && !reduce.matches;
      if (run && !timer) timer = window.setInterval(tick, 1000);
      if (!run && timer) { window.clearInterval(timer); timer = null; }
    };
    new IntersectionObserver(function (entries) {
      visible = entries[entries.length - 1].isIntersecting;
      sync();
    }).observe(card);
    document.addEventListener("visibilitychange", sync);
    if (reduce.addEventListener) reduce.addEventListener("change", sync);
  }
  /* the mode showcase: a tab rail over the panels, which all show, stacked, without this file */
  var show = document.querySelector("[data-showcase]");
  var list = show && show.querySelector("[role=tablist]");
  if (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll("[role=tab]"));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute("aria-controls")); });
    var wide = window.matchMedia("(width > 1100px)");
    var orient = function () { list.setAttribute("aria-orientation", wide.matches ? "vertical" : "horizontal"); };
    var warm = function (i) {
      var img = panels[i].querySelector("img[loading=lazy]");
      if (img) img.loading = "eager";
    };
    var select = function (i, focus) {
      tabs.forEach(function (t, j) {
        var on = j === i;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
      });
      warm(i);
      warm((i + 1) % tabs.length);
      warm((i - 1 + tabs.length) % tabs.length);
      if (focus) tabs[i].focus({ preventScroll: !wide.matches });
      if (!wide.matches) {
        var t = tabs[i];
        list.scrollTo({ left: t.offsetLeft - (list.clientWidth - t.offsetWidth) / 2, behavior: reduce.matches ? "auto" : "smooth" });
      }
    };
    panels.forEach(function (p, j) {
      p.setAttribute("role", "tabpanel");
      p.setAttribute("aria-labelledby", tabs[j].id);
    });
    list.addEventListener("click", function (e) {
      var t = e.target.closest("[role=tab]");
      if (t) select(tabs.indexOf(t), false);
    });
    list.addEventListener("keydown", function (e) {
      var i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      var n = tabs.length;
      var k = e.key;
      var to = null;
      if (k === "ArrowRight" || (wide.matches && k === "ArrowDown")) to = (i + 1) % n;
      else if (k === "ArrowLeft" || (wide.matches && k === "ArrowUp")) to = (i - 1 + n) % n;
      else if (k === "Home") to = 0;
      else if (k === "End") to = n - 1;
      if (to === null) return;
      e.preventDefault();
      select(to, true);
    });
    tabs.forEach(function (t, j) {
      t.addEventListener("pointerenter", function () { warm(j); });
    });
    orient();
    if (wide.addEventListener) wide.addEventListener("change", orient);
    show.classList.add("is-tabbed");
    list.hidden = false;
    select(0, false);
  }

  /* a larger look at a shot: a modal <dialog>. Without it (or without this file) the link opens the image. */
  var box = document.getElementById("nc-zoom");
  if (box && typeof box.showModal === "function") {
    var zImg = box.appendChild(Object.assign(document.createElement("img"), { className: "zm-img", id: "nc-zoom-img", alt: "" }));
    var zCap = document.getElementById("nc-zoom-cap");
    var zFull = document.getElementById("nc-zoom-full");
    var zBar = box.querySelector(".zm-bar");
    var opener = null;
    var ratio = 1.6;
    var most = 1600;
    var fit = function () {
      /* the dialog is as wide as the image; the caption bar wraps inside it, so measure it twice */
      for (var pass = 0; pass < 2; pass++) {
        var w = Math.min(most, window.innerWidth * 0.94 - 2, (window.innerHeight * 0.92 - zBar.offsetHeight - 2) * ratio);
        box.style.width = Math.max(240, Math.floor(w)) + 2 + "px";
      }
    };
    document.addEventListener("click", function (e) {
      var a = e.target.closest ? e.target.closest("a[data-zoom]") : null;
      if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || window.innerWidth < 600) return;
      var img = a.querySelector("img");
      if (!img) return;
      e.preventDefault();
      opener = a;
      ratio = (+img.getAttribute("width") / +img.getAttribute("height")) || 1.6;
      most = +a.getAttribute("data-zoom") || 1600;
      var fig = a.closest("figure");
      var said = fig && (fig.querySelector(".sc-now") || fig.querySelector("figcaption"));
      zCap.textContent = said ? said.textContent : img.alt;
      zImg.alt = img.alt;
      zImg.width = +img.getAttribute("width");
      zImg.height = +img.getAttribute("height");
      zImg.src = a.getAttribute("href");
      zFull.href = a.getAttribute("href");
      box.showModal();
      fit();
    });
    document.getElementById("nc-zoom-x").addEventListener("click", function () { box.close(); });
    box.addEventListener("click", function (e) { if (e.target === box) box.close(); });
    box.addEventListener("close", function () {
      zImg.removeAttribute("src");
      if (opener) opener.focus();
      opener = null;
    });
    window.addEventListener("resize", function () { if (box.open) fit(); }, { passive: true });
  }
})();
