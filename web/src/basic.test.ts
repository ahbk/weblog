import { assert, expect, test } from 'vitest';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkHtml from 'remark-html';

test('remarkHype', async () => {
  const md = '# Hello, *world';
  const h = await unified().use(remarkParse).use(remarkHtml).process(md);
  expect('<h1>Hello, *world</h1>\n').toBe(String(h));
});

test('post', async () => {
  const response = await fetch('http://weblog.dev:8000/auth/login', {
    method: 'POST',
    body: new URLSearchParams({
      username: 'alxhbk@proton.me',
      password: 'secret',
    })
  });
  expect(response.ok).eq(true);
  const response_login = await response.json();
  const post = {
    id: null,
    title: "hello",
    body: "world",
    created: null,
  };
  const response_create = await fetch('http://weblog.dev:8000/posts/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${response_login.access_token}`,
    },
    body: JSON.stringify(post),
  });
  post.id = (await response_create.json()).id;
  expect(response_create.ok).eq(true)

  const response_delete = await fetch(`http://weblog.dev:8000/posts/delete/${post.id}`, {
    method: 'DELETE',
  });
  expect((await response_delete.json()).rowcount).toBe(1);
});

test('login', async () => {
    const response = await fetch('http://weblog.dev:8000/auth/login', {
      method: 'POST',
      body: new URLSearchParams({
        username: 'alxhbk@proton.me',
        password: 'secret',
      })
    });
    expect(response.ok).eq(true);
});

test('Math.sqrt()', () => {
  expect(Math.sqrt(4)).toBe(2);
  expect(Math.sqrt(144)).toBe(12);
  expect(Math.sqrt(2)).toBe(Math.SQRT2);
});

test('JSON', () => {
  const input = {
    foo: 'hello',
    bar: 'world'
  };

  const output = JSON.stringify(input);

  expect(output).eq('{"foo":"hello","bar":"world"}');
  assert.deepEqual(JSON.parse(output), input, 'matches original');
});
