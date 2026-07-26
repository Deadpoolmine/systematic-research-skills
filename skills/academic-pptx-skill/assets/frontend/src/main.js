import './styles/main.css';
import.meta.glob('./slides/slide-*.js', { eager: true });
import { PPTController } from './js/ppt-controller.js';

window.addEventListener('DOMContentLoaded', () => {
  new PPTController();
});
