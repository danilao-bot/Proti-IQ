/**
 * Proti IQ Supabase Cloud Client.
 * Connects directly to the live PostgreSQL database for crops, jobs, meals, and rankings.
 */
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://dzbcefkvzufomdpfjmrw.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_cRzeE31P8Dlc9T5AZpgdIg_3GUu7E46';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

export async function fetchLiveCrops() {
  const { data, error } = await supabase
    .from('crops')
    .select('*')
    .order('common_name');
  if (error) {
    console.error('Supabase fetch crops error:', error);
    return null;
  }
  return data;
}

export async function fetchLiveJobs() {
  const { data, error } = await supabase
    .from('jobs')
    .select('*');
  if (error) {
    console.error('Supabase fetch jobs error:', error);
    return null;
  }
  return data;
}

export async function fetchLiveMeals() {
  const { data, error } = await supabase
    .from('meals')
    .select('*')
    .order('name');
  if (error) {
    console.error('Supabase fetch meals error:', error);
    return null;
  }
  return data;
}

export async function fetchLiveRankings(jobId) {
  const { data, error } = await supabase
    .from('rankings')
    .select('*, crops(*)')
    .eq('job', jobId)
    .order('score', { ascending: false });
  if (error) {
    console.error(`Supabase fetch rankings for ${jobId} error:`, error);
    return null;
  }
  return data;
}
