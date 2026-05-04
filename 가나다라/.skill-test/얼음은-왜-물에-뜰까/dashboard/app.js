const data = window.SCIENCE_SHORTS_PROJECT || {};
const project = data.project || {};

document.querySelector("#title").textContent = project.title || "Untitled";
document.querySelector("#language").textContent = project.language || "-";
document.querySelector("#duration").textContent = `${project.target_duration_sec || "-"} sec`;
document.querySelector("#status").textContent = project.status || "draft";
document.querySelector("#script").textContent = data.script || "";
document.querySelector("#sources").textContent = data.sources || "";

const outputs = document.querySelector("#outputs");
[...(data.renders || []), ...(data.audio || []), ...(data.captions || [])].forEach((path) => {
  const a = document.createElement("a");
  a.href = `../${path}`;
  a.textContent = path.split(/[\\/]/).pop();
  outputs.appendChild(a);
});

const scenes = document.querySelector("#scenes");
(data.scenes || []).forEach((scene, index) => {
  const article = document.createElement("article");
  article.className = "scene";

  if (scene.image) {
    const img = document.createElement("img");
    img.src = `../${scene.image}`;
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
