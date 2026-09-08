document.addEventListener('DOMContentLoaded', () => {
  const isMobile = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
  if (!isMobile) return;

  const rows = Array.from(document.querySelectorAll('.doushi-row'));
  const progress = document.querySelector('.doushi-progress');
  const container = document.querySelector('.doushi-container');
  if (!rows.length || !container) return;

  let index = 0;
  let startX = 0;
  let startY = 0;
  let tracking = false;
  let animating = false;

  const updateProgress = () => {
    if (progress) {
      progress.textContent = `${index + 1} / ${rows.length}`;
    }
  };

  const show = (nextIndex, direction) => {
    if (animating || nextIndex === index) return;
    if (nextIndex < 0 || nextIndex >= rows.length) return;

    animating = true;
    const current = rows[index];
    const next = rows[nextIndex];
    const goingRight = direction === 'right';

    current.classList.remove('active');
    current.classList.add(goingRight ? 'slide-out-right' : 'slide-out-left');

    next.classList.add(goingRight ? 'slide-in-from-left' : 'slide-in-from-right');
    next.classList.add('active');

    // Force layout so the enter transform applies before clearing it
    void next.offsetWidth;
    next.classList.remove('slide-in-from-left', 'slide-in-from-right');

    window.setTimeout(() => {
      current.classList.remove('slide-out-left', 'slide-out-right');
      index = nextIndex;
      updateProgress();
      animating = false;
    }, 260);
  };

  const goNext = () => show(index + 1, 'left');
  const goPrev = () => show(index - 1, 'right');

  container.addEventListener('touchstart', (event) => {
    if (animating || event.touches.length !== 1) return;
    tracking = true;
    startX = event.touches[0].clientX;
    startY = event.touches[0].clientY;
  }, { passive: true });

  container.addEventListener('touchmove', (event) => {
    if (!tracking || event.touches.length !== 1) return;
    const dx = event.touches[0].clientX - startX;
    const dy = event.touches[0].clientY - startY;
    // Prefer horizontal swipe over vertical scroll
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
      goNext();
    } else {
      goPrev();
    }
  }, { passive: true });

  updateProgress();
});
