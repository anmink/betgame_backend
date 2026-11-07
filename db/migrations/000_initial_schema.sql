create table public.matches (
  fixture_id bigint not null,
  fixture_date text not null,
  fixture_status text null,
  league_id bigint null,
  league_name text null,
  league_round text null,
  teamhome_name text null,
  teamhome_logo text null,
  teamhome_winner boolean null,
  teamaway_name text null,
  teamaway_logo text null,
  teamaway_winner boolean null,
  goal_home bigint null,
  goal_away bigint null,
  odd_home real null,
  odd_draw real null,
  odd_away real null,
  constraint matches_pkey primary key (fixture_id)
) TABLESPACE pg_default;

create table public.system_values (
  key text not null,
  value text not null,
  constraint system_values_pkey primary key (key)
) TABLESPACE pg_default;

alter table matches enable row level security;
alter table system_values enable row level security;