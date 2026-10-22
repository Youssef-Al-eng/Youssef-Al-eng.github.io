(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");
  document.documentElement.classList.add("js");

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  function closeMenu() {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open navigation");
    nav.classList.remove("is-open");
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      toggle.setAttribute("aria-label", expanded ? "Open navigation" : "Close navigation");
      nav.classList.toggle("is-open", !expanded);
    });
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        closeMenu(); toggle.focus();
      }
    });
  }

  var filters = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  var cards = Array.prototype.slice.call(document.querySelectorAll(".project-card[data-category]"));
  var status = document.querySelector(".filter-status");
  filters.forEach(function (button) {
    button.addEventListener("click", function () {
      var value = button.getAttribute("data-filter");
      var visible = 0;
      filters.forEach(function (item) { item.setAttribute("aria-pressed", String(item === button)); });
      cards.forEach(function (card) {
        var categories = (card.getAttribute("data-category") || "").split(/\s+/);
        var show = value === "all" || categories.indexOf(value) !== -1;
        card.hidden = !show;
        if (show) visible += 1;
      });
      if (status) status.textContent = value === "all" ? "Showing all " + visible + " research projects." : "Showing " + visible + " " + button.textContent.trim() + " projects.";
    });
  });

  var year = document.getElementById("current-year");
  if (year) year.textContent = String(new Date().getFullYear());

  if ("IntersectionObserver" in window) {
    var skillCards = Array.prototype.slice.call(document.querySelectorAll(".skills-card"));
    if (skillCards.length && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      skillCards.forEach(function (card) { card.classList.add("reveal"); });
      document.documentElement.classList.add("reveal-ready");
      var revealObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -35px 0px" });
      skillCards.forEach(function (card) { revealObserver.observe(card); });
    }

    var sections = Array.prototype.slice.call(document.querySelectorAll("main section[id]"));
    var links = Array.prototype.slice.call(document.querySelectorAll(".site-nav a[href^='#']"));
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (link) {
          if (link.getAttribute("href") === "#" + entry.target.id) link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        });
      });
    }, { rootMargin: "-25% 0px -65% 0px" });
    sections.forEach(function (section) { observer.observe(section); });
  }
})();
