import base64
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VOICE_ID = "LS3HmRGCXV8wxCAhUbTt"
MODEL_ID = "eleven_multilingual_v2"


def narration_text(markdown: str) -> str:
    lines = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append(stripped)
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def main():
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise SystemExit("Missing ELEVENLABS_API_KEY")

    text = narration_text((ROOT / "narration.md").read_text(encoding="utf-8"))
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.8,
            "style": 0.25,
            "use_speaker_boost": True,
        },
    }
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"ElevenLabs HTTP {exc.code}: {detail}") from exc

    audio_b64 = data.get("audio_base64")
    if not audio_b64:
        raise SystemExit(f"Unexpected response keys: {sorted(data.keys())}")

    audio_path = ROOT / "assets/audio/narration-elevenlabs-timestamped.mp3"
    json_path = ROOT / "assets/audio/narration-elevenlabs-timestamped.json"
    audio_path.write_bytes(base64.b64decode(audio_b64))
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(audio_path)
    print(json_path)


if __name__ == "__main__":
    main()
