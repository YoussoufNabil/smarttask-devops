const API = '/api/tasks';
const tasksEl = document.getElementById('tasks');
const form = document.getElementById('taskForm');
const title = document.getElementById('title');
const statusEl = document.getElementById('status');

async function loadTasks() {
  statusEl.textContent = 'Chargement...';
  try {
    const res = await fetch(API);
    if (!res.ok) throw new Error('API indisponible');
    const tasks = await res.json();
    tasksEl.innerHTML = '';
    if (!tasks.length) {
      tasksEl.innerHTML = '<li class="small">Aucune tâche pour le moment.</li>';
    }
    for (const task of tasks) {
      const li = document.createElement('li');
      li.innerHTML = `
        <span class="${task.completed ? 'done' : ''}">${escapeHtml(task.title)}</span>
        <span class="actions">
          <button class="toggle" data-id="${task.id}">${task.completed ? 'Réouvrir' : 'Terminer'}</button>
          <button class="delete" data-id="${task.id}">Supprimer</button>
        </span>`;
      tasksEl.appendChild(li);
    }
    statusEl.textContent = `${tasks.length} tâche(s)`;
  } catch (e) {
    statusEl.textContent = 'Erreur : ' + e.message;
  }
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const value = title.value.trim();
  if (!value) return;
  const res = await fetch(API, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({title: value})
  });
  if (!res.ok) { statusEl.textContent = 'Impossible d’ajouter la tâche.'; return; }
  title.value = '';
  loadTasks();
});

tasksEl.addEventListener('click', async (e) => {
  const id = e.target.dataset.id;
  if (!id) return;
  if (e.target.classList.contains('toggle')) {
    await fetch(`${API}/${id}/toggle`, {method: 'PATCH'});
  }
  if (e.target.classList.contains('delete')) {
    await fetch(`${API}/${id}`, {method: 'DELETE'});
  }
  loadTasks();
});

document.getElementById('refresh').addEventListener('click', loadTasks);

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}

loadTasks();
