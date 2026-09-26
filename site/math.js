document.addEventListener('DOMContentLoaded', () => {
  const paper = document.querySelector('.paper');
  if (!paper || !window.renderMathInElement) return;
  renderMathInElement(paper, {delimiters:[{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}],throwOnError:false,strict:'ignore',trust:false});
  paper.querySelectorAll('.math.display').forEach(el => { el.tabIndex=0; el.setAttribute('role','region'); el.setAttribute('aria-label','Scrollable equation'); });
  function focusScrollingMath(){paper.querySelectorAll('.math.inline').forEach(el => {if(el.scrollWidth>el.clientWidth||el.scrollHeight>el.clientHeight){el.tabIndex=0;el.setAttribute('role','region');el.setAttribute('aria-label','Scrollable inline equation');}else{el.removeAttribute('tabindex');el.removeAttribute('role');el.removeAttribute('aria-label');}});}
  new ResizeObserver(focusScrollingMath).observe(paper);
  document.fonts.ready.then(focusScrollingMath);
  document.documentElement.dataset.mathReady='true';
});
