import { writable } from 'svelte/store';

type User = {
  email?: string;
  id?: string;
  accessToken?: string;
  verificationToken?: string;
  displayName?: string;
  isSuper?: boolean;
  isActive?: boolean;
  isVerified?: boolean;
};

export const user = writable<User>({});
