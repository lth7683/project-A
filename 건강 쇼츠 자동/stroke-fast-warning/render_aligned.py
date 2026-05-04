import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FFMPEG = shutil.which("ffmpeg")
FPS = 30
WIDTH = 1080
HEIGHT = 1920
TRANSITION = 0.25
AUDIO = ROOT / "assets/audio/narration-elevenlabs-timestamped.mp3"
ALIGNMENT = ROOT / "assets/audio/narration-elevenlabs-timestamped.json"


CAPTIONS = [
    ("이 증상 보이면\n절대 기다리지 마세요.", "이 증상 보이면\\N절대 기다리지 마세요", "assets/images/scene-01.png"),
    ("갑자기 한쪽 얼굴이 처지거나", "갑자기 한쪽 얼굴이\\N처지거나", "assets/images/scene-02.png"),
    ("팔 하나에 힘이 빠지면\n위험 신호일 수 있습니다.", "팔 하나에 힘이 빠지면\\N위험 신호일 수 있습니다", "assets/images/scene-03.png"),
    ("말이 어눌해지고\n문장이 이상하게 나오면", "말이 어눌해지고\\N문장이 이상하게 나오면", "assets/images/scene-04.png"),
    ("그 순간이 중요합니다.", "그 순간이\\N중요합니다", "assets/images/scene-05.png"),
    ("전문기관은\n이걸 FAST로 확인하라고 말합니다.", "전문기관은\\NFAST 확인을 말합니다", "assets/images/scene-06.png"),
    ("얼굴.\n팔.\n말.\n그리고 시간.", "얼굴\\N팔\\N말\\N그리고 시간", "assets/images/scene-07.png"),
    ("증상이 사라져도\n그냥 넘기면 안 됩니다.", "증상이 사라져도\\N그냥 넘기면 안 됩니다", "assets/images/scene-08.png"),
    ("여기서 꼭 알아야 할 건강상식.", "꼭 알아야 할\\N건강상식", "assets/images/scene-06.png"),
    ("뇌졸중이 의심되면\n물도 음식도 주면 안 됩니다.", "의심되면\\N물도 음식도 금지", "assets/images/scene-08.png"),
    ("삼키는 힘이 떨어져\n기도로 넘어갈 수 있습니다.", "삼키는 힘이 떨어져\\N위험할 수 있습니다", "assets/images/scene-08.png"),
    ("증상 시작 시간을 기억하고\n바로 119입니다.", "시작 시간 기억\\N바로 119", "assets/images/scene-05.png"),
]


def run(cmd, capture=False):
    return subprocess.run(cmd, check=True, text=True, capture_output=capture)


def audio_duration(path):
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        capture=True,
    )
    return float(result.stdout.strip())


def ass_time(seconds):
    cs = int(round(seconds * 100))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, cs = divmod(rem, 100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def ffmpeg_escape(path):
    return path.as_posix().replace(":", "\\:")


def compact(text):
    return "".join(text.split())


def build_index(chars):
    compact_chars = []
    compact_to_original = []
    for idx, char in enumerate(chars):
        if not char.isspace():
            compact_to_original.append(idx)
            compact_chars.append(char)
    return "".join(compact_chars), compact_to_original


def find_segments():
    data = json.loads(ALIGNMENT.read_text(encoding="utf-8"))
    alignment = data["alignment"]
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    compact_text, compact_to_original = build_index(chars)

    cursor = 0
    segments = []
    for source, caption, image in CAPTIONS:
        needle = compact(source)
        pos = compact_text.find(needle, cursor)
        if pos < 0:
            raise SystemExit(f"Could not align caption: {source!r}")
        first = compact_to_original[pos]
        last = compact_to_original[pos + len(needle) - 1]
        start = starts[first]
        end = ends[last]
        segments.append({"start": start, "end": end, "caption": caption, "image": image})
        cursor = pos + len(needle)
    return segments


def write_ass(path, segments):
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Center,Malgun Gothic,90,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,8,0,5,70,70,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for seg in segments:
        start = max(0, seg["start"] - 0.03)
        end = seg["end"] + 0.08
        lines.append(
            f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Center,,0,0,0,,{seg['caption']}"
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    if not FFMPEG:
        raise SystemExit("ffmpeg not found")

    duration = audio_duration(AUDIO)
    segments = find_segments()
    out_dir = ROOT / "renders"
    out_dir.mkdir(exist_ok=True)
    ass_path = out_dir / "captions-aligned.ass"
    out_path = out_dir / "final-elevenlabs-aligned.mp4"
    write_ass(ass_path, segments)

    visual = []
    for idx, seg in enumerate(segments):
        start = seg["start"] if idx == 0 else min(seg["start"], segments[idx - 1]["end"] + 0.18)
        end = segments[idx + 1]["start"] if idx < len(segments) - 1 else duration
        visual.append({**seg, "visual_start": start, "visual_end": max(end, seg["end"])})

    cmd = [FFMPEG, "-y"]
    clip_lengths = []
    for idx, seg in enumerate(visual):
        base = seg["visual_end"] - seg["visual_start"]
        input_duration = base + (TRANSITION if idx < len(visual) - 1 else 0)
        input_duration = max(input_duration, 0.6)
        clip_lengths.append(input_duration)
        cmd += ["-loop", "1", "-t", f"{input_duration:.3f}", "-i", str(ROOT / seg["image"])]
    cmd += ["-i", str(AUDIO)]

    parts = []
    for idx, clip_duration in enumerate(clip_lengths):
        frames = max(1, int(round(clip_duration * FPS)))
        zoom_step = "0.00035" if idx % 2 else "0.00045"
        parts.append(
            f"[{idx}:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},setsar=1,"
            f"zoompan=z='min(1.035,zoom+{zoom_step})':d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS},"
            "format=yuv420p"
            f"[v{idx}]"
        )

    current = "[v0]"
    elapsed = clip_lengths[0]
    for idx in range(1, len(visual)):
        offset = elapsed - TRANSITION
        label = f"[x{idx}]"
        parts.append(
            f"{current}[v{idx}]xfade=transition=fade:duration={TRANSITION}:offset={offset:.3f}{label}"
        )
        current = label
        elapsed += clip_lengths[idx] - TRANSITION

    parts.append(
        f"{current}subtitles='{ffmpeg_escape(ass_path)}',"
        f"trim=duration={duration:.3f},setpts=PTS-STARTPTS,format=yuv420p[vout]"
    )

    cmd += [
        "-filter_complex",
        ";".join(parts),
        "-map",
        "[vout]",
        "-map",
        f"{len(visual)}:a:0",
        "-shortest",
        "-r",
        str(FPS),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(out_path),
    ]
    run(cmd)

    project_path = ROOT / "project.json"
    project = json.loads(project_path.read_text(encoding="utf-8"))
    project["final_render"] = "renders/final-elevenlabs-aligned.mp4"
    project["captions"] = "renders/captions-aligned.ass"
    project["tts"]["audio"] = "assets/audio/narration-elevenlabs-timestamped.mp3"
    project["render_notes"] = {
        "sync": "captions and cuts generated from ElevenLabs character timestamps",
        "captions": "center-screen ASS subtitles",
        "cuts": "timestamp-based scene changes with 0.25s crossfades",
    }
    project_path.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)
    for seg in segments:
        print(f"{seg['start']:.2f}-{seg['end']:.2f} {seg['caption'].replace(chr(92)+'N', ' / ')}")


if __name__ == "__main__":
    main()
