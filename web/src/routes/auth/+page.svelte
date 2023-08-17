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

<div>
  <h1 class="text-4xl">Authentication</h1>
  {#if form?.incorrect}
    <p>Invalid credentials!</p>
  {/if}

  {#if !data?.user}
    {#if form?.success}
      <p>Successfully logged out!</p>
    {/if}
    <form class="space-y-3" method="POST" action="?/login" use:enhance>
      <label class="label">
        Email
        <input class="input" name="email" type="email" value={form?.email ?? ''} />
      </label>
      <label class="label">
        Password
        <input class="input" name="password" type="password" />
      </label>
      <button class="btn btn-blue">Log in</button>
      <button class="btn btn-blue" formaction="?/register">Register</button>
    </form>
  {:else}
    {#if form?.success}
      <p>Successfully logged in! Welcome back, {data.user.displayName || data.user.email}!</p>
    {/if}
    <dl class="divide-y">
      <div class="row">
        <dd>id</dd>
        <dt>{data.user.id}</dt>
      </div>
      <div class="row">
        <dd>access token</dd>
        <dt>{data.user.accessToken}</dt>
      </div>
      <div class="row">
        <dd>verification token</dd>
        <dt>{data.user.verificationToken}</dt>
      </div>
      <div class="row">
        <dd>email</dd>
        <dt>{data.user.email}</dt>
      </div>
      <div class="row">
        <dd>display name</dd>
        <dt>
          <form method="POST" use:enhance>
            <input type="text" name="displayName" value={data.user.displayName} />
            <button class="btn btn-blue" formaction="?/patchMe">Save</button>
            <button class="btn btn-red">Cancel</button>
          </form>
        </dt>
      </div>
      <div class="row">
        <dd>active</dd>
        <dt>{data.user.isActive}</dt>
      </div>
      <div class="row">
        <dd>superuser</dd>
        <dt>{data.user.isSuper}</dt>
      </div>
      <div class="row">
        <dd>verified</dd>
        <dt>{data.user.isVerified}</dt>
      </div>
    </dl>
    <form class="space-y-3" method="POST" use:enhance>
      <button class="btn btn-blue" formaction="?/logout">Log out</button>
    </form>
    <form class="space-y-3" method="POST" use:enhance>
      <button class="btn btn-blue" formaction="?/verification_request">Request verification</button>
      <button class="btn btn-blue" formaction="?/verify" value={data.user.verificationToken}
        >Verify</button
      >
      <button class="btn btn-red" formaction="?/deleteMe">Delete</button>
    </form>
  {/if}
</div>

<style lang="postcss">
  .row {
    @apply px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0;
  }
</style>
