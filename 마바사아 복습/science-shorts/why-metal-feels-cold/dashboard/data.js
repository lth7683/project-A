window.SCIENCE_SHORTS_PROJECT = {
  "project": {
    "title": "금속은 왜 같은 온도인데 더 차갑게 느껴질까?",
    "slug": "why-metal-feels-cold",
    "language": "ko",
    "target_duration_sec": 45,
    "voice_id": "7Nah3cbXKVmGX7gQUuwz",
    "duplicate_check": {
      "checked_before_script": true,
      "method": "scripts/topic_audit.py --root .",
      "existing_topic_count": 0,
      "result": "No previous Shorts topics found in the workspace, so this topic is clear."
    },
    "status": "rendered_with_elevenlabs_voice",
    "render": {
      "width": 1080,
      "height": 1920,
      "fps": 30
    }
  },
  "script": "# 금속은 왜 같은 온도인데 더 차갑게 느껴질까?\n\n같은 방에 있던 나무 숟가락과 금속 숟가락.\n온도는 거의 같은데, 왜 금속만 차갑게 느껴질까요?\n\n정답은 온도가 아니라, 내 손의 열이 얼마나 빨리 빠져나가느냐입니다.\n금속은 열전도율이 높아서 손가락의 열을 순식간에 가져갑니다.\n\n반대로 나무나 플라스틱은 열을 천천히 가져가요.\n그래서 실제 온도가 같아도, 손은 금속을 더 차갑다고 착각합니다.\n\n차가움은 물체의 성격만이 아니라, 내 몸과 물체 사이의 열 이동 속도인 셈이죠.\n\n그래서 뜨거운 팬도 위험합니다.\n금속은 차가울 때도, 뜨거울 때도, 열을 빠르게 주고받으니까요.\n\n",
  "sources": "# Sources\n\n## Duplicate-topic check\n\n- Checked before writing the script with `topic_audit.py --root .`.\n- Existing Shorts topics found in this workspace: 0.\n- Selected topic: `금속은 왜 같은 온도인데 더 차갑게 느껴질까?`\n- Result: no overlap found.\n\n## Science sources\n\n- OpenStax, *College Physics 2e*, section 14.5 \"Conduction\": explains that tile can feel colder than carpet at the same temperature because heat leaves skin faster, and lists metals such as copper, aluminum, and steel as much higher thermal-conductivity materials than wood or air. https://openstax.org/books/college-physics-2e/pages/14-5-conduction\n\n",
  "scenes": [
    {
      "id": "scene-01",
      "narration": "같은 방에 있던 나무 숟가락과 금속 숟가락. 온도는 거의 같은데, 왜 금속만 차갑게 느껴질까요?",
      "caption": "같은 온도인데\n왜 금속만 차가울까?",
      "duration_sec": 8.0,
      "image": "assets/images/scene-01.png",
      "image_prompt": "Use case: scientific-educational. Asset type: 9:16 science Shorts scene. A hand hovering between a wooden spoon and a metal spoon on the same table, subtle thermometer icons showing same room temperature, clean modern educational illustration, high contrast, no text, no watermark, accurate everyday physics."
    },
    {
      "id": "scene-02",
      "narration": "정답은 온도가 아니라, 내 손의 열이 얼마나 빨리 빠져나가느냐입니다.",
      "caption": "차가움의 정체는\n열이 빠져나가는 속도",
      "duration_sec": 8.0,
      "image": "assets/images/scene-02.png",
      "image_prompt": "Use case: scientific-educational. Asset type: 9:16 science Shorts scene. Close-up of a fingertip touching a cool metal surface, glowing heat particles flowing from the finger into the metal, clean cinematic educational illustration, no text, no watermark."
    },
    {
      "id": "scene-03",
      "narration": "금속은 열전도율이 높아서 손가락의 열을 순식간에 가져갑니다.",
      "caption": "금속은 열을\n빠르게 가져간다",
      "duration_sec": 8.0,
      "image": "assets/images/scene-03.png",
      "image_prompt": "Use case: scientific-educational. Asset type: 9:16 science Shorts scene. Split view comparing metal and wood: fast bright heat stream into metal, slow faint heat stream into wood, simple visual metaphor, clean educational rendering, no words, no watermark."
    },
    {
      "id": "scene-04",
      "narration": "반대로 나무나 플라스틱은 열을 천천히 가져가요. 그래서 실제 온도가 같아도, 손은 금속을 더 차갑다고 착각합니다.",
      "caption": "온도가 아니라\n피부가 잃는 열",
      "duration_sec": 10.0,
      "image": "assets/images/scene-04.png",
      "image_prompt": "Use case: scientific-educational. Asset type: 9:16 science Shorts scene. Human hand touching wood, plastic, and metal samples at the same temperature, skin sensory nerves shown as subtle glowing lines, clean science illustration, no text, no watermark."
    },
    {
      "id": "scene-05",
      "narration": "그래서 뜨거운 팬도 위험합니다. 금속은 차가울 때도, 뜨거울 때도, 열을 빠르게 주고받으니까요.",
      "caption": "금속은 차가워도 뜨거워도\n열 교환이 빠르다",
      "duration_sec": 9.0,
      "image": "assets/images/scene-05.png",
      "image_prompt": "Use case: scientific-educational. Asset type: 9:16 science Shorts scene. Safe kitchen scene with a hot metal pan and a wooden handle nearby, visible heat shimmer and caution mood without gore or injury, clean educational illustration, no text, no watermark."
    }
  ],
  "renders": [
    "renders\\final.mp4"
  ],
  "audio": [
    "assets\\audio\\narration.json",
    "assets\\audio\\narration.mp3",
    "assets\\audio\\narration.wav"
  ],
  "captions": [
    "assets\\captions\\captions.srt"
  ]
};
