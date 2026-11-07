alter table users rename column balance to coins;
alter table users alter column coins type integer using coins::integer;
alter table users alter column coins set default 50;
alter table users add constraint coins_not_negative check (coins >= 0);
alter table users add column becher integer not null default 0 check (becher >= 0);
alter table users add column last_collect_at timestamptz;

alter table bets rename column amount to stake;
alter table bets alter column stake type integer using stake::integer;
alter table bets add column payout integer;

create table kurs (
    id bigint generated always as identity primary key,
    value numeric not null check (value between 0.5 and 2.0),
    created_at timestamptz not null default now()
);

alter table kurs enable row level security;