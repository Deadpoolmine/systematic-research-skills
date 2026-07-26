export class PPTController {
  constructor() {
    this.viewport = document.getElementById('ppt-viewport');
    this.prevButton = document.getElementById('prevBtn');
    this.nextButton = document.getElementById('nextBtn');
    this.progress = document.getElementById('progressBarFill');
    this.indicator = document.getElementById('pageIndicator');
    this.slides = [];
    this.current = 0;
    this.loadSlides();
    this.bindEvents();
    this.show(this.readPageFromUrl() - 1, false);
    this.scaleViewport();
  }

  loadSlides() {
    const pageNumbers = [...window.slideDataMap.keys()].sort((a, b) => a - b);
    for (const pageNumber of pageNumbers) {
      const slide = document.createElement('section');
      slide.className = 'slide';
      slide.innerHTML = window.slideDataMap.get(pageNumber).trim();
      this.viewport.appendChild(slide);
      this.slides.push(slide);
    }
  }

  bindEvents() {
    this.prevButton.addEventListener('click', () => this.show(this.current - 1));
    this.nextButton.addEventListener('click', () => this.show(this.current + 1));
    document.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowLeft') this.show(this.current - 1);
      if (event.key === 'ArrowRight' || event.key === ' ') {
        event.preventDefault();
        this.show(this.current + 1);
      }
      if (event.key === 'Home') this.show(0);
      if (event.key === 'End') this.show(this.slides.length - 1);
    });
    window.addEventListener('resize', () => this.scaleViewport());
  }

  readPageFromUrl() {
    const value = Number(new URLSearchParams(window.location.search).get('page'));
    return Number.isInteger(value) && value > 0 ? value : 1;
  }

  show(index, updateUrl = true) {
    if (this.slides.length === 0) {
      this.prevButton.disabled = true;
      this.nextButton.disabled = true;
      this.indicator.textContent = '0 / 0';
      return;
    }
    const next = Math.max(0, Math.min(index, this.slides.length - 1));
    this.slides.forEach((slide, position) => slide.classList.toggle('active', position === next));
    this.current = next;
    this.prevButton.disabled = next === 0;
    this.nextButton.disabled = next === this.slides.length - 1;
    this.progress.style.width = `${((next + 1) / this.slides.length) * 100}%`;
    this.indicator.textContent = `${next + 1} / ${this.slides.length}`;
    if (updateUrl) {
      const params = new URLSearchParams(window.location.search);
      params.set('page', String(next + 1));
      window.history.replaceState({}, '', `${window.location.pathname}?${params}`);
    }
  }

  scaleViewport() {
    const scale = Math.min((window.innerWidth - 40) / 1440, (window.innerHeight - 40) / 810, 1);
    this.viewport.style.transform = `scale(${scale})`;
  }
}
