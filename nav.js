/* ------------------------------------------------------------------
   Site configuration — the single place to customize the site.
   Reorder NAV items, edit links, or swap the avatar here.
------------------------------------------------------------------- */
const SITE = {
  name: "Youssef Alaa",
  fullName: "Youssef Alaa Abdelrady",
  role: "Applied AI Engineer · Cairo, Egypt",
  email: "youssefalaa.1356@gmail.com",
  linkedin: "https://www.linkedin.com/in/youssef-alaa-334581406/",
  github: "https://github.com/Youssef-Al-eng",
  avatar: "https://avatars.githubusercontent.com/Youssef-Al-eng?size=320"
};

const NAV = [
  { title: "Home",       url: "index.html" },
  { title: "About",      url: "about.html" },
  { title: "Projects",   url: "projects.html" },
  { title: "Research",   url: "research.html" },
  { title: "Experience", url: "experience.html" },
  { title: "Education",  url: "education.html" },
  { title: "Contact",    url: "contact.html" }
];

(function build() {
  const page = location.pathname.split("/").pop() || "index.html";

  const nav = document.getElementById("site-nav");
  if (nav) {
    nav.innerHTML = "<ul>" + NAV.map(function (n) {
      var active = n.url === page ? ' class="active"' : "";
      return '<li><a href="' + n.url + '"' + active + ">" + n.title + "</a></li>";
    }).join("") + "</ul>";
  }

  var sb = document.getElementById("sidebar");
  if (sb) {
    sb.innerHTML =
      '<img class="avatar" src="' + SITE.avatar + '" alt="Photo of ' + SITE.fullName + '">' +
      '<div class="name">' + SITE.fullName + "</div>" +
      '<div class="role">' + SITE.role + "</div>" +
      '<div class="follow-label">Follow</div><ul>' +
      '<li><a href="mailto:' + SITE.email + '">Email</a></li>' +
      '<li><a href="' + SITE.linkedin + '" target="_blank" rel="noopener">LinkedIn</a></li>' +
      '<li><a href="' + SITE.github + '" target="_blank" rel="noopener">GitHub</a></li>' +
      "</ul>";
  }

  var f = document.getElementById("footer");
  if (f) {
    f.innerHTML =
      '<div class="footer-inner">' +
      "<div>© " + new Date().getFullYear() + " " + SITE.fullName + "</div>" +
      '<div>Follow: <a href="' + SITE.github + '">GitHub</a> · ' +
      '<a href="' + SITE.linkedin + '" target="_blank" rel="noopener">LinkedIn</a></div></div>';
  }
})();
