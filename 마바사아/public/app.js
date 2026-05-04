const form = document.querySelector('#transcriptForm');
const linksInput = document.querySelector('#links');
const langInput = document.querySelector('#lang');
const timestampsInput = document.querySelector('#timestamps');
const clearButton = document.querySelector('#clearButton');
const counter = document.querySelector('#linkCounter');
const statusBox = document.querySelector('#status');
const resultsBox = document.querySelector('#results');
const downloadAllButton = document.querySelector('#downloadAll');

let latestResults = [];

function parseLinks(value) {
  return value
    .split(/\r?\n|,\s*/)
    .map((link) => link.trim())
    .filter(Boolean);
}

function updateCounter() {
  counter.textContent = `${parseLinks(linksInput.value).length}개`;
}

function setStatus(message, tone = 'idle') {
  statusBox.textContent = message;
  statusBox.className = `status ${tone}`;
}

function safeName(text, index) {
  const match = text.match(/(?:v=|youtu\.be\/|shorts\/|embed\/)([A-Za-z0-9_-]{11})/);
  return `transcript-${String(index + 1).padStart(2, '0')}${match ? `-${match[1]}` : ''}.txt`;
}

function downloadText(filename, text) {
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

async function copyText(text, button) {
  await navigator.clipboard.writeText(text);
  const previous = button.textContent;
  button.textContent = '복사됨';
  setTimeout(() => {
    button.textContent = previous;
  }, 1000);
}

function renderResults(payload) {
  latestResults = payload.results || [];
  resultsBox.innerHTML = '';
  downloadAllButton.disabled = latestResults.every((result) => !result.ok);

  latestResults.forEach((result, index) => {
    const article = document.createElement('article');
    article.className = `result ${result.ok ? '' : 'failed'}`;

    const header = document.createElement('div');
    header.className = 'result-header';

    const info = document.createElement('div');
    const link = document.createElement('div');
    link.className = 'result-link';
    link.textContent = result.link;
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = result.ok
      ? `${result.count}개 구간${result.lang ? ` · ${result.lang}` : ''}`
      : '실패';
    info.append(link, meta);

    const actions = document.createElement('div');
    actions.className = 'result-actions';
    if (result.ok) {
      const copyButton = document.createElement('button');
      copyButton.className = 'ghost compact';
      copyButton.type = 'button';
      copyButton.textContent = '복사';
      copyButton.addEventListener('click', () => copyText(result.text, copyButton));

      const downloadButton = document.createElement('button');
      downloadButton.className = 'ghost compact';
      downloadButton.type = 'button';
      downloadButton.textContent = '다운로드';
      downloadButton.addEventListener('click', () => downloadText(safeName(result.link, index), result.text));
      actions.append(copyButton, downloadButton);
    }

    const body = document.createElement('pre');
    body.textContent = result.ok ? result.text : result.error;

    header.append(info, actions);
    article.append(header, body);
    resultsBox.append(article);
  });
}

linksInput.addEventListener('input', updateCounter);

clearButton.addEventListener('click', () => {
  linksInput.value = '';
  langInput.value = '';
  resultsBox.innerHTML = '';
  latestResults = [];
  downloadAllButton.disabled = true;
  updateCounter();
  setStatus('링크를 입력하고 추출을 시작하세요.');
});

downloadAllButton.addEventListener('click', () => {
  const text = latestResults
    .filter((result) => result.ok)
    .map((result, index) => `# ${index + 1}. ${result.link}\n\n${result.text}`)
    .join('\n\n---\n\n');
  downloadText('youtube-transcripts-all.txt', text);
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const links = parseLinks(linksInput.value);
  if (links.length === 0) {
    setStatus('유튜브 링크를 1개 이상 입력해주세요.', 'error');
    return;
  }

  const submitButton = form.querySelector('button[type="submit"]');
  submitButton.disabled = true;
  downloadAllButton.disabled = true;
  resultsBox.innerHTML = '';
  setStatus(`${links.length}개 링크를 처리 중입니다.`, 'busy');

  try {
    const response = await fetch('/api/transcripts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        links,
        lang: langInput.value.trim(),
        includeTimestamps: timestampsInput.checked,
      }),
    });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error || '요청을 처리하지 못했습니다.');
    }

    renderResults(payload);
    setStatus(`완료: 성공 ${payload.success}개, 실패 ${payload.failed}개`, payload.failed ? 'error' : 'idle');
  } catch (error) {
    setStatus(error.message || '요청을 처리하지 못했습니다.', 'error');
  } finally {
    submitButton.disabled = false;
  }
});

updateCounter();
