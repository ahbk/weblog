import { fail } from '@sveltejs/kit';
import type { Actions } from './$types';

//export const load = (async ({ cookies }) => {
//  const user = await db.getUserFromSession(cookies.get('sessionid'));
//  return { user };
//}) satisfies PageServerLoad;

export const actions = {
  login: async ({ cookies, request, fetch }) => {
    const data = await request.formData();
    const body = new URLSearchParams({
      username: (data.get('email') as any),
      password: (data.get('password') as any),
    });
    const response = await fetch('http://weblog.dev:8000/auth/login', {
      method: "POST",
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body,
    });
    console.log(response.headers);

    if(response.ok) {
      //const access_token = (await response.json())['access_token'];
      //cookies.set('access_token', access_token);
      return { success: true };
    } else {
      return fail(400);
    }
  },
  register: async (event) => {
    console.log(event);
  },
} satisfies Actions;
