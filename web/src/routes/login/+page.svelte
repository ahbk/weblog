<script lang="ts">
  import { enhance } from '$app/forms';
  import type { PageData, ActionData } from './$types';
  export let data: PageData;
  export let form: ActionData;
</script>

<svelte:head>
  <title>Login</title>
  <meta name="description" content="Login" />
</svelte:head>

<div class="text-column">
  <h1>Login</h1>
  {data.user.email}
  <h1>Login</h1>
  <form method="POST" action="?/login" use:enhance>
    <label>
      Email
      <input name="email" type="email" value={form?.email ?? ''} />
    </label>
    <label>
      Password
      <input name="password" type="password" />
    </label>
    <button>Log in</button>
    <button formaction="?/register">Register</button>
  </form>
  {#if form?.incorrect}<p class="error">Invalid credentials!</p>{/if}

  {#if form?.success}
    <!-- this message is ephemeral; it exists because the page was rendered in
           response to a form submission. it will vanish if the user reloads -->
    <p>Successfully logged in! Welcome back, {data.user.email}</p>
  {/if}
</div>
