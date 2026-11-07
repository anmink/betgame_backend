drop table if exists bets;
drop table if exists users;

create table users (
  id uuid primary key references auth.users(id) on delete cascade,
  username text not null,
  balance numeric not null default 100,
  created_at timestamptz not null default now()
);

create table bets (
  id bigint generated always as identity primary key,
  user_id uuid not null references users(id) on delete cascade,
  match_id bigint not null references matches(fixture_id),
  amount numeric not null check (amount > 0),
  odds numeric not null,
  prediction text not null check (prediction in ('home', 'draw', 'away')),
  status text not null default 'open' check (status in ('open', 'won', 'lost')),
  created_at timestamptz not null default now()
);

alter table users enable row level security;
alter table bets enable row level security;