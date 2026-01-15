document.addEventListener('DOMContentLoaded', () => {
  const textInput = document.getElementById('textInput');
  const convertBtn = document.getElementById('convertBtn');
  const clearBtn = document.getElementById('clearBtn');

  convertBtn.addEventListener('click', () => {
    let text = textInput.value;
    // Разбиваем текст по переносам строк
    const lines = text.split(/\r?\n/);
    // Оборачиваем непустые строки в <p>, игнорируем пустые
    const paragraphs = lines
      .map(line => line.trim() !== '' ? `<p>${line}</p>` : '')
      .join('\n');
    textInput.value = paragraphs;
  });

  clearBtn.addEventListener('click', () => {
    textInput.value = '';
  });
});
