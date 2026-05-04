import express from 'express';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { fetchTranscript } from 'youtube-transcript';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const app = express();
const port = process.env.PORT || 3000;
const maxLinks = 30;
const concurrency = 3;

app.use(express.json({ limit: '120kb' }));
app.use(express.static(path.join(__dirname, 'public')));

function uniqueLinks(rawLinks) {
  const seen = new Set();
  return rawLinks
    .map((link) => String(link || '').trim())
    .filter(Boolean)
    .filter((link) => {
      if (seen.has(link)) return false;
      seen.add(link);
      return true;
    });
}

function normalizeYouTubeInput(input) {
  const value = String(input || '').trim();
  const idOnly = value.match(/^[A-Za-z0-9_-]{11}$/);
  if (idOnly) return value;

  try {
    const url = new URL(value);
    const videoId = url.searchParams.get('v');
    if (videoId && /^[A-Za-z0-9_-]{11}$/.test(videoId)) return videoId;

    const pathId = url.pathname
      .split('/')
      .filter(Boolean)
      .find((part, index, parts) => {
        const previous = parts[index - 1];
        return ['shorts', 'embed', 'live'].includes(previous) && /^[A-Za-z0-9_-]{11}$/.test(part);
      });
    if (pathId) return pathId;

    if (url.hostname === 'youtu.be') {
      const shortId = url.pathname.split('/').filter(Boolean)[0];
      if (/^[A-Za-z0-9_-]{11}$/.test(shortId)) return shortId;
    }
  } catch {
    return value;
  }

  return value;
}

function timestamp(msOrSeconds) {
  const totalSeconds = Math.max(0, Math.floor(Number(msOrSeconds) || 0));
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return [hours, minutes, seconds].map((part) => String(part).padStart(2, '0')).join(':');
}

function normalizeOffset(offset, usesMilliseconds) {
  const value = Number(offset) || 0;
  return usesMilliseconds ? value / 1000 : value;
}

function toPlainText(transcript, includeTimestamps) {
  const usesMilliseconds = transcript.some((line) => Number(line.duration) > 100);

  return transcript
    .map((line) => {
      const text = String(line.text || '').replace(/\s+/g, ' ').trim();
      if (!text) return '';
      return includeTimestamps ? `[${timestamp(normalizeOffset(line.offset, usesMilliseconds))}] ${text}` : text;
    })
    .filter(Boolean)
    .join('\n');
}

function errorMessage(error) {
  const message = error instanceof Error ? error.message : String(error);
  return message.replace(/^\[YoutubeTranscript\]\s*\S*\s*/, '').trim() || '자막을 가져오지 못했습니다.';
}

async function mapLimit(items, limit, mapper) {
  const results = new Array(items.length);
  let nextIndex = 0;

  async function worker() {
    while (nextIndex < items.length) {
      const currentIndex = nextIndex;
      nextIndex += 1;
      results[currentIndex] = await mapper(items[currentIndex], currentIndex);
    }
  }

  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return results;
}

app.post('/api/transcripts', async (req, res) => {
  const links = uniqueLinks(Array.isArray(req.body?.links) ? req.body.links : []);
  const lang = String(req.body?.lang || '').trim();
  const includeTimestamps = Boolean(req.body?.includeTimestamps);

  if (links.length === 0) {
    return res.status(400).json({ error: '유튜브 링크를 1개 이상 입력해주세요.' });
  }

  if (links.length > maxLinks) {
    return res.status(400).json({ error: `한 번에 최대 ${maxLinks}개까지 처리할 수 있습니다.` });
  }

  const results = await mapLimit(links, concurrency, async (link) => {
    try {
      const transcript = await fetchTranscript(normalizeYouTubeInput(link), lang ? { lang } : undefined);
      const text = toPlainText(transcript, includeTimestamps);
      return {
        ok: true,
        link,
        count: transcript.length,
        lang: transcript[0]?.lang || lang || '',
        text,
      };
    } catch (error) {
      return {
        ok: false,
        link,
        error: errorMessage(error),
      };
    }
  });

  res.json({
    total: results.length,
    success: results.filter((result) => result.ok).length,
    failed: results.filter((result) => !result.ok).length,
    results,
  });
});

app.listen(port, () => {
  console.log(`YouTube transcript batch app: http://localhost:${port}`);
});
