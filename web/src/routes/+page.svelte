<script>
</script>

<svelte:head>
  <title>weblog home</title>
  <meta name="description" content="Simple CMS" />
</svelte:head>

<section>
  <h1>weblog</h1>
  <p>right?</p>
  <form>
    <input type="text" class="px-4 py-3 rounded-full" />
    <label class="label">
      <span>Input</span>
      <input class="input" type="text" placeholder="Input" />
    </label>
    <div class="card p-4 w-full text-token space-y-4">
      <label class="label">
        <span>Input</span>
        <input class="input px-4 py-3" type="text" placeholder="Input" />
      </label>
      <label class="label">
        <span>Select</span>
        <select class="select">
          <option value="1">Option 1</option>
          <option value="2">Option 2</option>
          <option value="3">Option 3</option>
          <option value="4">Option 4</option>
          <option value="5">Option 5</option>
        </select>
      </label>
      <label class="label">
        <span>Textarea</span>
        <!-- cspell:disable-next-line -->
        <textarea
          class="textarea"
          rows="4"
          placeholder="Lorem ipsum dolor sit amet consectetur adipisicing elit."
        />
      </label>
    </div>
  </form>
</section>

<style>
</style>
