import { error, type Page } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load = (() => {
  throw error(404, 'sup');
  return { t: "aasdf" };
}) satisfies PageLoad;
