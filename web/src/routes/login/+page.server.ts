import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load = (async ({ cookies, fetch }) => {
  const response = await fetch('http://weblog.dev:8000/users/me', {
    method: "GET",
    headers: {
      'Authorization': `Bearer ${cookies.get('access_token')}`,
    },
  });
  const user = await response.json();
  return { user };
}) satisfies PageServerLoad;

export const actions = {
  login: async ({ cookies, request, url, fetch }) => {
    const data = await request.formData();
    const email = data.get('email');
    const password = data.get('password');
    const response = await fetch('http://weblog.dev:8000/auth/login', {
      method: "POST",
      body: new URLSearchParams({
        username: email as any,
        password: password as any,
      }),
    });

    console.log(url);
    if(!response.ok) {
      return fail(400, { email, incorrect: true });
    }

    const access_token = (await response.json())['access_token'];
    cookies.set('access_token', access_token, { secure: false });

    if (url.searchParams.has('redirectTo')) {
      throw redirect(303, url.searchParams.get('redirectTo'));
    }

    return { success: true };
  },
  register: async (event) => {
    console.log(event);
  },
} satisfies Actions;
