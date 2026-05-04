import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FFMPEG = shutil.which("ffmpeg")
FPS = 30
WIDTH = 1080
HEIGHT = 1920
TRANSITION = 0.35


timeline = [
    (0.00, 2.65, "이 증상 보이면\\N절대 기다리지 마세요", "assets/images/scene-01.png"),
    (2.65, 5.35, "갑자기 한쪽 얼굴이\\N처지거나", "assets/images/scene-02.png"),
    (5.35, 8.10, "팔 하나에 힘이 빠지면\\N위험 신호일 수 있습니다", "assets/images/scene-03.png"),
    (8.10, 11.25, "말이 어눌해지고\\N문장이 이상하게 나오면", "assets/images/scene-04.png"),
    (11.25, 13.85, "그 순간이\\N중요합니다", "assets/images/scene-05.png"),
    (13.85, 17.45, "전문기관은\\NFAST 확인을 말합니다", "assets/images/scene-06.png"),
    (17.45, 20.15, "얼굴\\N팔\\N말\\N그리고 시간", "assets/images/scene-07.png"),
    (20.15, 24.72, "증상이 사라져도\\N119 먼저\\N고정 댓글 확인", "assets/images/scene-08.png"),
]


def run(cmd):
    subprocess.run(cmd, check=True)


def ass_time(seconds):
    cs = int(round(seconds * 100))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, cs = divmod(rem, 100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def ffmpeg_escape(path):
    return path.as_posix().replace(":", "\\:")


def write_ass(path):
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Center,Malgun Gothic,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,8,0,5,70,70,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for start, end, caption, _ in timeline:
        lines.append(
            f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Center,,0,0,0,,{caption}"
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    if not FFMPEG:
        raise SystemExit("ffmpeg not found")

    out_dir = ROOT / "renders"
    out_dir.mkdir(exist_ok=True)
    ass_path = out_dir / "captions-center.ass"
    out_path = out_dir / "final-elevenlabs-smooth.mp4"
    audio = ROOT / "assets/audio/narration-elevenlabs-fast.mp3"
    write_ass(ass_path)

    cmd = [FFMPEG, "-y"]
    clip_lengths = []
    for idx, (start, end, _, image) in enumerate(timeline):
        duration = end - start
        input_duration = duration + (TRANSITION if idx < len(timeline) - 1 else 0)
        clip_lengths.append(input_duration)
        cmd += ["-loop", "1", "-t", f"{input_duration:.3f}", "-i", str(ROOT / image)]
    cmd += ["-i", str(audio)]

    parts = []
    for idx, duration in enumerate(clip_lengths):
        frames = max(1, int(round(duration * FPS)))
        zoom = "zoom+0.00045" if idx % 2 == 0 else "zoom+0.00030"
        parts.append(
            f"[{idx}:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},setsar=1,"
            f"zoompan=z='min(1.045,{zoom})':d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS},"
            f"format=yuv420p[v{idx}]"
        )

    current = "[v0]"
    elapsed = clip_lengths[0]
    for idx in range(1, len(timeline)):
        out_label = f"[x{idx}]"
        offset = elapsed - TRANSITION
        parts.append(
            f"{current}[v{idx}]xfade=transition=fade:duration={TRANSITION}:offset={offset:.3f}{out_label}"
        )
        current = out_label
        elapsed += clip_lengths[idx] - TRANSITION

    parts.append(
        f"{current}subtitles='{ffmpeg_escape(ass_path)}',"
        "trim=duration=24.722,setpts=PTS-STARTPTS,format=yuv420p[vout]"
    )
    filter_complex = ";".join(parts)

    cmd += [
        "-filter_complex",
        filter_complex,
        "-map",
        "[vout]",
        "-map",
        f"{len(timeline)}:a:0",
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
    project["final_render"] = "renders/final-elevenlabs-smooth.mp4"
    project["captions"] = "renders/captions-center.ass"
    project["render_notes"] = {
        "sync": "timeline rebuilt against ElevenLabs fast audio",
        "captions": "center-screen ASS subtitles",
        "cuts": "Ken Burns motion with 0.35s crossfade transitions",
    }
    project_path.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
