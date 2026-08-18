// Same story as api.js: no auth backend wired up yet, so accounts and
// sessions just live in localStorage. Good enough for demoing the flow,
// not something to trust with real passwords - swap this out for real
// auth (Supabase auth, since it's already a dependency, is the obvious
// choice) before this goes anywhere near production.

const USERS_KEY = 'fatiguesense_users';
const SESSION_KEY = 'fatiguesense_session';

function readUsers() {
  try {
    return JSON.parse(localStorage.getItem(USERS_KEY)) || [];
  } catch {
    return [];
  }
}

function writeUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

function makeId() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return 'user-' + Math.random().toString(36).slice(2) + Date.now().toString(36);
}

export function getSession() {
  try {
    return JSON.parse(localStorage.getItem(SESSION_KEY));
  } catch {
    return null;
  }
}

function setSession(user) {
  const session = { id: user.id, name: user.name, email: user.email };
  localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  return session;
}

export function signUp(name, email, password) {
  if (!name.trim()) throw new Error('Please enter your name.');
  if (!/^\S+@\S+\.\S+$/.test(email)) throw new Error('Please enter a valid email.');
  if (password.length < 6) throw new Error('Password must be at least 6 characters.');

  const users = readUsers();
  if (users.some((u) => u.email.toLowerCase() === email.toLowerCase())) {
    throw new Error('An account with this email already exists.');
  }

  const user = { id: makeId(), name: name.trim(), email: email.trim(), password };
  writeUsers([...users, user]);
  return setSession(user);
}

export function logIn(email, password) {
  const user = readUsers().find(
    (u) => u.email.toLowerCase() === email.trim().toLowerCase() && u.password === password
  );
  if (!user) {
    throw new Error('Incorrect email or password.');
  }
  return setSession(user);
}

export function logOut() {
  localStorage.removeItem(SESSION_KEY);
}
