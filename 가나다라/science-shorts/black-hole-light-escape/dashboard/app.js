const data = window.SCIENCE_SHORTS_PROJECT || {};
const project = data.project || {};

function assetUrl(path) {
  return `../${String(path || "").replaceAll("\\", "/")}`;
}

function fileName(path) {
  return String(path || "").split(/[\\/]/).pop();
}

document.querySelector("#title").textContent = project.title || "Untitled";
document.querySelector("#language").textContent = project.language || "-";
document.querySelector("#duration").textContent = `${project.output?.duration_sec || project.target_duration_sec || "-"} sec`;
document.querySelector("#status").textContent = project.status || "draft";
document.querySelector("#script").textContent = data.script || "";
document.querySelector("#sources").textContent = data.sources || "";

const renderPath = project.output?.path || (data.renders || []).find((path) => fileName(path) === "final.mp4") || (data.renders || [])[0];
const videoWrap = document.querySelector("#video-wrap");
if (renderPath) {
  const video = document.createElement("video");
  video.controls = true;
  video.playsInline = true;
  video.preload = "metadata";
  video.src = assetUrl(renderPath);
  videoWrap.appendChild(video);
} else {
  const empty = document.createElement("p");
  empty.className = "muted";
  empty.textContent = "No rendered video found.";
  videoWrap.appendChild(empty);
}

const audioPath = project.audio?.path || (data.audio || []).find((path) => /\.(mp3|wav|m4a)$/i.test(path));
const audioWrap = document.querySelector("#audio-wrap");
if (audioPath) {
  const audio = document.createElement("audio");
  audio.controls = true;
  audio.preload = "metadata";
  audio.src = assetUrl(audioPath);
  audioWrap.appendChild(audio);
}

const outputs = document.querySelector("#outputs");
[...(data.renders || []), ...(data.audio || []), ...(data.captions || [])].forEach((path) => {
  const a = document.createElement("a");
  a.href = assetUrl(path);
  a.textContent = fileName(path);
  outputs.appendChild(a);
});

const scenes = document.querySelector("#scenes");
(data.scenes || []).forEach((scene, index) => {
  const article = document.createElement("article");
  article.className = "scene";

  if (scene.image) {
    const img = document.createElement("img");
    img.src = assetUrl(scene.image);
    img.alt = scene.id || `scene-${index + 1}`;
    article.appendChild(img);
  }

  const title = document.createElement("h3");
  title.textContent = scene.id || `Scene ${index + 1}`;
  article.appendChild(title);

  const caption = document.createElement("p");
  caption.textContent = scene.caption || "";
  article.appendChild(caption);

  const narration = document.createElement("p");
  narration.textContent = scene.narration || "";
  article.appendChild(narration);

  const prompt = document.createElement("p");
  prompt.className = "prompt";
  prompt.textContent = scene.image_prompt || "";
  article.appendChild(prompt);

  scenes.appendChild(article);
});
