document.addEventListener('DOMContentLoaded', () => {
  // Проверяем, что это мобильное устройство (сенсорный экран без мыши)
  const isMobile = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
  
  if (isMobile) {
    const items = document.querySelectorAll('.kanji-item');
    
    items.forEach(item => {
      item.addEventListener('click', () => {
        // Переключаем класс active для показа/скрытия обратной стороны
        item.classList.toggle('active');
      });
    });
  }
});
