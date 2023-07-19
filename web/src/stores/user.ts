import { writable, get } from 'svelte/store';

interface User {
  email?: string;
  display_name?: string;
  access_token: string;
  logged_in?: boolean;
}

export const user = writable<User>({ access_token: '' });

export async function update_user() {
  if(get(user).access_token) {
    const response_user = await fetch('http://weblog.dev:8000/user/me', {
      headers: {
        Authorization: `Bearer ${get(user).access_token}`
      }
    });
    if(response_user.ok) {
      let me = await response_user.json();
      user.update(user => {
        return {
          email: me.email,
          display_name: me.display_name,
          access_token: user.access_token,
          logged_in: true,
        };
      });
      return true;
    }
    user.update(_ => {
      return {
        access_token: '',
        logged_in: false,
      };
    });
  }
  return false;
}
