import { expect, test } from 'vitest';

interface LooseObject {
  [key: string]: any;
}
const data: LooseObject = {};

test('login', async () => {
  const response = await fetch('http://weblog.local:8000/login', {
    method: 'POST',
    body: new URLSearchParams({
      username: 'alxhbk@proton.me',
      password: 'secret'
    })
  });
  console.log((await response.text()));
  expect(response.ok).eq(true);
  data.access_token = response.headers.get('Set-Cookie');
});

test('get user', async () => {
  const response = await fetch('http://weblog.local:8000/user/me', {
    headers: {
      'Cookie': data.access_token,
    }
  });
  expect(response.ok).toBe(true);
});

test('create post unauthorized', async () => {
  const post = {
    id: null,
    title: 'hello',
    body: 'world',
    created: null
  };
  const response_create = await fetch('http://weblog.local:8000/posts/create', {
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
  const response_create = await fetch('http://weblog.local:8000/posts/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Cookie': data.access_token,
    },
    body: JSON.stringify(post)
  });
  expect(response_create.ok).eq(true);
  data.post_id = (await response_create.json()).id;
});

test('get post', async () => {
  const response = await fetch(`http://weblog.local:8000/posts/get/${data.post_id}`, {
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
  const response = await fetch(`http://weblog.local:8000/posts/list`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  const posts = await response.json();
  expect(response.ok).toBe(true);
  expect(posts[0].title).toBe('hello');
});

test('delete post unauthorized', async () => {
  const response = await fetch(`http://weblog.local:8000/posts/delete/${data.post_id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  expect(response.status).eq(401);
});

test('delete post', async () => {
  const response = await fetch(`http://weblog.local:8000/posts/delete/${data.post_id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Cookie': data.access_token,
    }
  });
  expect((await response.json()).rowcount).toBe(1);
});
