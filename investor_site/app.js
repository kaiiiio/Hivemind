const tocLinks = [...document.querySelectorAll(".toc a")];
const sections = tocLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

function updateActiveLink() {
  const current =
    [...sections].reverse().find((section) => section.getBoundingClientRect().top <= 140) ||
    sections[0];

  if (!current) return;

  tocLinks.forEach((link) => {
    link.classList.toggle("active", link.getAttribute("href") === `#${current.id}`);
  });
}

window.addEventListener("scroll", updateActiveLink, { passive: true });
document.addEventListener("scroll", updateActiveLink, { passive: true });
updateActiveLink();
