document.addEventListener('DOMContentLoaded', () => {
  const isMobile = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
  
  if (isMobile) {
    const items = document.querySelectorAll('.kanji-item');
    
    items.forEach(item => {
      item.addEventListener('click', () => {
        item.classList.toggle('active');
      });
    });
  }
});
