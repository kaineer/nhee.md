document.addEventListener('DOMContentLoaded', () => {
  const isMobile = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
  if (!isMobile) return;

  const container = document.querySelector('.doushi-container');
  if (!container) return;

  let mode = 'jidoushi'; // or 'tadoushi'
  let startX = 0;
  let startY = 0;
  let tracking = false;

  const setMode = (next) => {
    if (next === mode) return;
    mode = next;
    container.classList.toggle('mode-tadoushi', mode === 'tadoushi');
  };

  container.addEventListener('touchstart', (event) => {
    if (event.touches.length !== 1) return;
    tracking = true;
    startX = event.touches[0].clientX;
    startY = event.touches[0].clientY;
  }, { passive: true });

  container.addEventListener('touchmove', (event) => {
    if (!tracking || event.touches.length !== 1) return;
    const dx = event.touches[0].clientX - startX;
    const dy = event.touches[0].clientY - startY;
    // горизонтальный жест — не даём странице скроллиться по диагонали
    if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 10) {
      event.preventDefault();
    }
  }, { passive: false });

  container.addEventListener('touchend', (event) => {
    if (!tracking) return;
    tracking = false;
    const touch = event.changedTouches[0];
    const dx = touch.clientX - startX;
    const dy = touch.clientY - startY;
    const threshold = 50;

    if (Math.abs(dx) < threshold || Math.abs(dx) < Math.abs(dy)) return;

    if (dx < 0) {
      // свайп влево → 他動詞
      setMode('tadoushi');
    } else {
      // свайп вправо → 自動詞
      setMode('jidoushi');
    }
  }, { passive: true });
});
