import { expect, test } from 'vitest';
import { API_HOST } from '$env/static/private';

interface LooseObject {
  [key: string]: any;
}
const data: LooseObject = {};

test('login', async () => {
  const response = await fetch(`https://${API_HOST}/auth/login`, {
    method: 'POST',
    body: new URLSearchParams({
      username: 'a@a.a',
      password: 'a'
    })
  });
  expect(response.ok).eq(true);
  data.user_token = (await response.json()).access_token;
});

test('get user', async () => {
  const response = await fetch(`https://${API_HOST}/users/me`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${data.user_token}`
    }
  });
  expect(response.ok).eq(true);
  expect((await response.json()).email).eq('a@a.a');
});

test('create post unauthorized', async () => {
  const post = {
    id: null,
    title: 'hello',
    body: 'world',
    created: null
  };
  const response_create = await fetch(`https://${API_HOST}/posts/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(post)
  });
  expect(response_create.status).eq(401);
});

test('create post', async () => {
  const post = {
    id: null,
    title: 'hello',
    body: 'world',
    created: null
  };
  const response_create = await fetch(`https://${API_HOST}/posts/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${data.user_token}`
    },
    body: JSON.stringify(post)
  });
  expect(response_create.ok).eq(true);
  data.post_id = (await response_create.json()).id;
});

test('get post', async () => {
  const response = await fetch(`https://${API_HOST}/posts/get/${data.post_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  const post = await response.json();
  expect(response.ok).toBe(true);
  expect(post.title).toBe('hello');
});

test('get post list', async () => {
  const response = await fetch(`https://${API_HOST}/posts/list`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  const post = await response.json();
  expect(response.ok).toBe(true);
  expect(post[0].title).toBe('hello');
});

test('delete post unauthorized', async () => {
  const response = await fetch(`https://${API_HOST}/posts/delete/${data.post_id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  expect(response.status).eq(401);
});

test('delete post', async () => {
  const response = await fetch(`https://${API_HOST}/posts/delete/${data.post_id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${data.user_token}`
    }
  });
  expect((await response.json()).rowcount).toBe(1);
});
