// 페르소나 배지와 CV 다운로드 버튼을 trestles 사이드바 하단으로 이동
// 페이지 로드 후 한 번만 실행
(function() {
  function relocate() {
    const entity = document.querySelector('.quarto-about-trestles .about-entity');
    if (!entity) return;

    const badges = document.querySelector('.persona-badges');
    const cvDownload = document.querySelector('.cv-download');

    if (badges) {
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
