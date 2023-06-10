import { expect, test } from 'vitest';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkHtml from 'remark-html';

test('remarkHype', async () => {
  const md = '# Hello, *world*';
  const h = await unified().use(remarkParse).use(remarkHtml).process(md);
  expect('<h1>Hello, <em>world</em></h1>\n').toBe(String(h));
});

