// 페르소나 배지와 CV 다운로드 버튼을 trestles 사이드바로 이동
// 순서: 프로필 이미지 → 이름 → 직함 → [배지] → 소셜 링크 → [CV 버튼]
(function() {
  function relocate() {
    const entity = document.querySelector('.quarto-about-trestles .about-entity');
    if (!entity) return;

    const aboutLinks = entity.querySelector('.about-links');
    const badges = document.querySelector('.persona-badges');
    const cvDownload = document.querySelector('.cv-download');

    if (badges && aboutLinks) {
      badges.classList.add('sidebar-relocated');
      entity.insertBefore(badges, aboutLinks);
    } else if (badges) {
      badges.classList.add('sidebar-relocated');
      entity.appendChild(badges);
    }

    if (cvDownload) {
      cvDownload.classList.add('sidebar-relocated');
      entity.appendChild(cvDownload);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', relocate);
  } else {
    relocate();
  }
})();
