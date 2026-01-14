document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("img[data-fallback]").forEach(img => {
    img.addEventListener("error", () => {
      img.src = img.dataset.fallback;
    }, {once: true});
  });
});
