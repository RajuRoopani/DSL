async function fetchSkills() {
  const res = await fetch('/roadmap/api/skills/');
  return await res.json();
}

async function generate(skillId) {
  const res = await fetch(`/roadmap/api/generate/${skillId}/`);
  return await res.json();
}

async function init() {
  const skills = await fetchSkills();
  const select = document.getElementById('skill-select');
  skills.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s.id;
    opt.text = s.name;
    select.appendChild(opt);
  });

  document.getElementById('generate').addEventListener('click', async () => {
    const id = select.value;
    const data = await generate(id);
    const container = document.getElementById('roadmap-result');
    container.innerHTML = '';
    if (data.topics && data.topics.length) {
      data.topics.forEach(t => {
        const h = document.createElement('h3');
        h.textContent = t.topic.title;
        container.appendChild(h);
        if (t.resources.length) {
          const ul = document.createElement('ul');
          t.resources.forEach(r => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = r.url || '#';
            a.textContent = r.title;
            a.target = '_blank';
            li.appendChild(a);
            ul.appendChild(li);
          });
          container.appendChild(ul);
        }
      });
    } else {
      container.textContent = 'No topics found for this skill.';
    }
  });
}

init();
