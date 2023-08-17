import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { user } from '../../stores/user';
import { get } from 'svelte/store';
import { API_HOST } from '$env/static/private';

export const load = (async ({ cookies, fetch, url }) => {
  user.update((u) => {
    u.accessToken = cookies.get('accessToken');
    return u;
  });

  if (!get(user).accessToken) {
    user.update((_) => ({}));
    console.log('asdf');
    return;
  }

  const response = await fetch(`https://${API_HOST}/users/me`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${get(user).accessToken}`
    }
  });

  if (!response.ok) {
    cookies.delete('accessToken');
    return;
  }

  const me = await response.json();

  user.update((u) => {
    return {
      id: me.id,
      email: me.email,
      accessToken: u.accessToken,
      displayName: me.display_name,
      isSuper: me.is_superuser,
      isActive: me.is_active,
      isVerified: me.is_verified
    };
  });

  if (!url.searchParams.has('verificationToken')) {
    return { user: get(user) };
  }

  user.update((u) => {
    u.verificationToken = url.searchParams.get('verificationToken');
    return u;
  });

  return { user: get(user) };
}) satisfies PageServerLoad;

export const actions = {
  login: async ({ cookies, request, url, fetch }) => {
    const data = await request.formData();
    const email = data.get('email');
    const password = data.get('password');

    if (!(email && password)) {
      return fail(400, { email, incorrect: true });
    }

    const response = await fetch(`https://${API_HOST}/auth/login`, {
      method: 'POST',
      body: new URLSearchParams({
        username: email as string,
        password: password as string
      })
    });

    if (!response.ok) {
      return fail(400, { email, incorrect: true });
    }

    const accessToken = (await response.json())['access_token'];
    cookies.set('accessToken', accessToken);

    if (url.searchParams.has('redirectTo')) {
      throw redirect(303, url.searchParams.get('redirectTo'));
    }

    return { success: true };
  },

  logout: async ({ cookies }) => {
    cookies.delete('accessToken');
    return { success: true };
  },

  register: async ({ request, fetch }) => {
    const data = await request.formData();
    const email = data.get('email');
    const password = data.get('password');

    if (!(email && password)) {
      return fail(400, { email, incorrect: true });
    }

    const response = await fetch(`https://${API_HOST}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email as string,
        password: password as string
      })
    });
  },

  patchMe: async ({ request, fetch }) => {
    const data = await request.formData();
    const displayName = data.get('displayName');
    const response = await fetch(`https://${API_HOST}/users/me`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${get(user).accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        display_name: displayName as string
      })
    });
  },

  deleteMe: async ({ fetch }) => {
    const response = await fetch(`https://${API_HOST}/users/me`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${get(user).accessToken}`
      }
    });
    return { success: response.ok };
  },

  verification_request: async ({ fetch }) => {
    const response = await fetch(`https://${API_HOST}/auth/request-verify-token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email: get(user).email })
    });
    return { verify: response.ok };
  },
  verify: async ({ fetch }) => {
    const response = await fetch(`https://${API_HOST}/auth/request-verify-token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email: get(user).email })
    });
    return { verify: response.ok };
  }
} satisfies Actions;
