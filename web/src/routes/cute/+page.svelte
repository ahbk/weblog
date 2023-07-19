<script lang="ts">
  import { enhance } from '$app/forms';

  let data = {posts: [{
    title: 'hello',
    body: 'world',
    }]};

  let login = false;

  function toggle_login() {
    login = !login;
  }
</script>

<svelte:head>
  <title>weblog home</title>
  <meta name="description" content="Simple CMS" />
</svelte:head>

<section class="weblog">
  <div class="top">
    <div class="search-bar">
      <form>
        <input type="text" placeholder="search" />
        <button>🔍</button>
      </form>
    </div>
    <div class="user-bar">
      <button on:click={toggle_login}>🔏</button>
      {#if login}
        <div class="login">
          <h2>Login</h2>
          <form method="POST" action="?/login" use:enhance>
            <input name="email" type="email" placeholder="email" value={form?.email ?? ''} />
            <br />
            <input name="password" type="password" placeholder="password" />
            <br />
            <button>Log in</button>
          </form>
          {#if form?.incorrect}<p class="error">Invalid credentials!</p>{/if}

          {#if form?.success}
            <!-- this message is ephemeral; it exists because the page was rendered in
                response to a form submission. it will vanish if the user reloads -->
            <p>Successfully logged in! Welcome back, </p>
          {/if}
        </div>
      {/if}
    </div>
  </div>
  <div class="feed-surface">
    <div class="feed">
      {#each data.posts as post}
        <div class="post">
          <h2 class="post-title">{post.title}</h2>
          <p>{post.body}</p>
          <button>😐</button>
        </div>
      {/each}
      <div class="end-of-posts">- - -</div>
    </div>
  </div>
  <div class="bottom">c</div>
</section>

<style>
</style>
