const KEY = 'session';
export const state = {
  session: JSON.parse(localStorage.getItem(KEY) || '{}'),
  setSession(s) {
    this.session = s;
    localStorage.setItem(KEY, JSON.stringify(s));
  },
  clear() {
    this.session = {};
    localStorage.removeItem(KEY);
  },
  isLogged() {
    return !!this.session.email;
  }
};
