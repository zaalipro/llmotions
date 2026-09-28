/* ncode landing — the copy button, the page's own progress bar and the run card's clock.
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
})();
