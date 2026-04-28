/**
 * Utility functions for text highlighting and selection
 */

export const getSelectedText = () => {
  if (window.getSelection) {
    return window.getSelection().toString();
  }
  return '';
};

export const getSelectionRange = (container) => {
  const selection = window.getSelection();
  if (selection.rangeCount === 0) {
    return null;
  }

  const range = selection.getRangeAt(0);
  const precaretRange = range.cloneRange();
  precaretRange.selectNodeContents(container);
  precaretRange.setEnd(range.endContainer, range.endOffset);
  const start = precaretRange.toString().length - range.toString().length;
  const end = start + range.toString().length;

  return { start, end, text: range.toString() };
};

export const highlightTextInElement = (element, highlights) => {
  if (!element) return;

  let innerHTML = element.innerHTML;
  const sortedHighlights = [...highlights].sort((a, b) => a.start_position - b.start_position);

  sortedHighlights.forEach(highlight => {
    const { text } = highlight;
    const regex = new RegExp(`(${text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'g');
    innerHTML = innerHTML.replace(regex, '<mark class="highlight">$1</mark>');
  });

  element.innerHTML = innerHTML;
};

export const removeHighlightMarkup = (element) => {
  if (!element) return;
  
  const marks = element.querySelectorAll('mark.highlight');
  marks.forEach(mark => {
    const parent = mark.parentNode;
    while (mark.firstChild) {
      parent.insertBefore(mark.firstChild, mark);
    }
    parent.removeChild(mark);
  });
};
