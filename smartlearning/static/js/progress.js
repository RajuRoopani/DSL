async function getCsrfToken() {
  const cookie = document.cookie.split(';').map(c => c.trim()).find(c => c.startsWith('csrftoken='));
  return cookie ? cookie.split('=')[1] : '';
}

async function addXP(amount) {
  const token = await getCsrfToken();
  const res = await fetch('/progress/api/progress/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': token
    },
    body: JSON.stringify({ xp: amount })
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || 'Failed to add XP');
  }
  return res.json();
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('add-xp-btn');
  if (!btn) return;
  btn.addEventListener('click', async () => {
    const amount = parseInt(document.getElementById('add-xp').value, 10) || 0;
    try {
      const data = await addXP(amount);
      // update XP element with authoritative total from server
      const xpEl = document.getElementById('xp-value');
      if (xpEl && data.total_xp !== undefined) {
        xpEl.textContent = data.total_xp;
      }
    } catch (err) {
      console.error('Add XP failed', err);
      alert('Failed to add XP. Are you logged in?');
    }
  });
});
