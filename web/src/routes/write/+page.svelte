<script lang="ts">
  import remarkRehype from 'remark-rehype';
  import { unified } from 'unified';
  const md = '# Hello, *world';
  console.log(md);

  /*
  const h = await unified()
    .use(remarkParse)
    .use(remarkHype)
    .process(md);
  */
</script>

<h1>Write</h1>

<div>
  <label>
    Title
    <input type="text" name="title" />
  </label>
  <label>
    Text
    <input type="textfield" name="title" id="simplemde" />
  </label>
</div>
