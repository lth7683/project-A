window.SCIENCE_SHORTS_PROJECT = {
  "project": {
    "title": "블랙홀은 왜 빛도 못 빠져나올까",
    "slug": "black-hole-light-escape",
    "language": "ko",
    "target_duration_sec": 45,
    "voice_id": "",
    "status": "complete",
    "topic": "블랙홀의 사건의 지평선과 탈출 속도",
    "audience": "중고등학생도 이해할 수 있는 과학 쇼츠 시청자",
    "audio": {
      "provider": "elevenlabs",
      "voice_id": "pb3lVZVjdFWbkhPKlelB",
      "model": "eleven_multilingual_v2",
      "path": "assets/audio/narration.mp3",
      "duration_sec": 56.84,
      "provisional": false,
      "note": "ElevenLabs TTS regenerated with requested voice_id."
    },
    "output": {
      "path": "renders/final.mp4",
      "alternate_path": "renders/final-elevenlabs.mp4",
      "duration_sec": 56.84,
      "video": "h264 1080x1920",
      "audio": "aac"
    },
    "source_urls": [
      "https://science.nasa.gov/universe/black-holes/",
      "https://www.nasa.gov/image-article/black-hole-friday/",
      "https://imagine.gsfc.nasa.gov/science/objects/black_holes1.html"
    ],
    "render": {
      "width": 1080,
      "height": 1920,
      "fps": 30
    }
  },
  "script": "# 블랙홀은 왜 빛도 못 빠져나올까\n\n빛보다 빠른 건 없죠.\n그런데 블랙홀 근처에는, 빛조차 밖으로 나올 수 없는 경계가 있습니다.\n\n핵심은 \"끌어당기는 힘\"보다 \"탈출 속도\"예요.\n지구를 벗어나려면 로켓이 아주 빠르게 날아야 하듯,\n무거운 물체에서 멀어지려면 필요한 속도가 있습니다.\n\n블랙홀은 엄청난 질량이 아주 작은 공간에 눌려 있는 천체입니다.\n그래서 어느 경계 안쪽에서는,\n빠져나가기 위해 필요한 속도가 빛의 속도보다 커집니다.\n\n하지만 우주에서 빛의 속도는 넘을 수 없는 한계입니다.\n이 경계를 사건의 지평선이라고 부르고,\n한번 안으로 들어가면 빛도, 물질도, 정보도 밖으로 돌아올 수 없습니다.\n\n그래서 블랙홀 자체는 까맣게 보입니다.\n우리가 보는 건 블랙홀이 아니라,\n그 주변에서 뜨겁게 빛나는 가스와 휘어진 빛의 흔적입니다.\n\n결론: 블랙홀은 빛을 \"잡아먹는 구멍\"이라기보다,\n밖으로 나가는 모든 길이 안쪽으로 휘어지는 공간입니다.\n\n",
  "sources": "# Sources\n\n- NASA Science, \"Black Holes\": black holes are extremely dense concentrations of matter; near the event horizon gravity is strong enough that nothing, not even light, can escape. It also notes that black holes are detected by their effects on nearby matter and light.\n  - https://science.nasa.gov/universe/black-holes/\n- NASA, \"It's Black Hole Friday!\": the event horizon is the boundary where the velocity needed to escape exceeds the speed of light, described as the speed limit of the cosmos.\n  - https://www.nasa.gov/image-article/black-hole-friday/\n- NASA Imagine the Universe, \"Black Holes\": explains escape velocity, Schwarzschild radius, and the event horizon as the point of no return where escape velocity equals light speed.\n  - https://imagine.gsfc.nasa.gov/science/objects/black_holes1.html\n\n## Fact Notes\n\n- Do not explain black holes as literal vacuum cleaners. From far away, gravity behaves like any object of the same mass.\n- The core explanation for \"why light cannot escape\" is not that light is slow, but that inside the event horizon all future paths through spacetime lead inward.\n- The escape-velocity analogy is useful for a short video, but avoid implying the event horizon is a solid surface.\n",
  "scenes": [
    {
      "id": "scene-01",
      "narration": "빛보다 빠른 건 없죠. 그런데 블랙홀 근처에는, 빛조차 밖으로 나올 수 없는 경계가 있습니다.",
      "caption": "빛조차 빠져나오지 못하는 경계",
      "duration_sec": 9.08,
      "image": "assets/images/scene-01.png",
      "image_prompt": "Use case: scientific-educational\nAsset type: 9:16 science Shorts scene\nPrimary request: a dramatic but accurate educational view of a black hole event horizon, with a dark central disk and glowing accretion material bending around it\nStyle/medium: polished cinematic science illustration, realistic space lighting\nComposition/framing: vertical 9:16, black hole centered slightly low, glowing ring arcs around it, strong empty upper space for captions\nLighting/mood: high contrast, awe-inspiring, deep space\nText: no text in image\nConstraints: depict light bending near a black hole, do not show a literal tunnel or monster-like hole, no watermark"
    },
    {
      "id": "scene-02",
      "narration": "핵심은 끌어당기는 힘보다 탈출 속도예요. 지구를 벗어나려면 로켓이 아주 빠르게 날아야 하듯, 무거운 물체에서 멀어지려면 필요한 속도가 있습니다.",
      "caption": "핵심은 탈출 속도",
      "duration_sec": 10.28,
      "image": "assets/images/scene-02.png",
      "image_prompt": "Use case: scientific-educational\nAsset type: 9:16 science Shorts scene\nPrimary request: an educational visual metaphor comparing a rocket escaping Earth gravity with a curved speed gauge rising upward\nStyle/medium: clean 3D educational illustration, realistic but simple\nComposition/framing: vertical split-depth scene, small Earth at bottom, rocket climbing upward, abstract speed arc behind it\nLighting/mood: clear, energetic, classroom explainer\nText: no text in image\nConstraints: communicate escape velocity visually without equations, no labels, no watermark"
    },
    {
      "id": "scene-03",
      "narration": "블랙홀은 엄청난 질량이 아주 작은 공간에 눌려 있는 천체입니다. 그래서 어느 경계 안쪽에서는, 빠져나가기 위해 필요한 속도가 빛의 속도보다 커집니다.",
      "caption": "질량이 작게 압축되면 중력이 극단적으로 커집니다",
      "duration_sec": 10.89,
      "image": "assets/images/scene-03.png",
      "image_prompt": "Use case: scientific-educational\nAsset type: 9:16 science Shorts scene\nPrimary request: a visual explanation of huge mass compressed into a tiny region, warping a spacetime grid into a deep funnel-like curvature around a black center\nStyle/medium: high-quality science museum illustration\nComposition/framing: vertical 9:16, spacetime grid curves downward toward a dark compact center, surrounding stars subtly distorted\nLighting/mood: precise, mysterious, educational\nText: no text in image\nConstraints: use spacetime curvature as a metaphor, avoid showing a physical solid surface, no watermark"
    },
    {
      "id": "scene-04",
      "narration": "하지만 우주에서 빛의 속도는 넘을 수 없는 한계입니다. 이 경계를 사건의 지평선이라고 부르고, 한번 안으로 들어가면 빛도, 물질도, 정보도 밖으로 돌아올 수 없습니다.",
      "caption": "사건의 지평선: 돌아올 수 없는 경계",
      "duration_sec": 12.09,
      "image": "assets/images/scene-04.png",
      "image_prompt": "Use case: scientific-educational\nAsset type: 9:16 science Shorts scene\nPrimary request: photons represented as thin beams approaching a glowing boundary around a black hole; outside beams curve around, inside beams bend inward\nStyle/medium: precise cinematic educational illustration\nComposition/framing: vertical, black hole lower center, subtle glowing circular boundary, light rays visibly curving inward\nLighting/mood: tense, clear, explanatory\nText: no text in image\nConstraints: make the event horizon look like an illustrative boundary not a hard surface, no arrows with labels, no watermark"
    },
    {
      "id": "scene-05",
      "narration": "그래서 블랙홀 자체는 까맣게 보입니다. 우리가 보는 건 블랙홀이 아니라, 그 주변에서 뜨겁게 빛나는 가스와 휘어진 빛의 흔적입니다. 결론: 블랙홀은 빛을 잡아먹는 구멍이라기보다, 밖으로 나가는 모든 길이 안쪽으로 휘어지는 공간입니다.",
      "caption": "우리가 보는 건 주변의 빛나는 흔적",
      "duration_sec": 14.5,
      "image": "assets/images/scene-05.png",
      "image_prompt": "Use case: scientific-educational\nAsset type: 9:16 science Shorts closing scene\nPrimary request: a black hole silhouette surrounded by a bright orange accretion disk and gravitationally lensed light, with distant stars distorted around it\nStyle/medium: cinematic NASA-inspired science illustration, realistic textures\nComposition/framing: vertical 9:16, black center in lower third, luminous ring and bent light dominate the frame, room for captions at bottom\nLighting/mood: awe, final reveal, polished educational short\nText: no text in image\nConstraints: do not include readable text, no fictional spaceship, no watermark"
    }
  ],
  "renders": [
    "renders\\final-elevenlabs.mp4",
    "renders\\final.mp4"
  ],
  "audio": [
    "assets\\audio\\elevenlabs-narration.json",
    "assets\\audio\\elevenlabs-narration.mp3",
    "assets\\audio\\narration.json",
    "assets\\audio\\narration.mp3",
    "assets\\audio\\narration.wav"
  ],
  "captions": [
    "assets\\captions\\captions.srt"
  ]
};
