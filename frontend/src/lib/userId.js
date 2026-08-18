import { getSession } from './auth';

const STORAGE_KEY = 'fatiguesense_user_id';

export function getUserId() {
  const session = getSession();
  if (session?.id) return session.id;

  let id = localStorage.getItem(STORAGE_KEY);
  if (!id) {
    id = generateId();
    localStorage.setItem(STORAGE_KEY, id);
  }
  return id;
}

function generateId() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return 'anon-' + Math.random().toString(36).slice(2) + Date.now().toString(36);
}
