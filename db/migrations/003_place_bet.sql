create or replace function place_bet(
  p_user_id uuid,
  p_match_id bigint,
  p_stake integer,
  p_prediction text,
  p_odds numeric
) returns bigint
language plpgsql as $$
declare
  v_bet_id bigint;
begin
  update users
  set coins = coins - p_stake
  where id = p_user_id and coins >= p_stake;

  if not found then
    raise exception 'insufficient_coins';
  end if;

  insert into bets (user_id, match_id, stake, odds, prediction)
  values (p_user_id, p_match_id, p_stake, p_odds, p_prediction)
  returning id into v_bet_id;

  return v_bet_id;
end;
$$;

revoke execute on function place_bet(uuid, bigint, integer, text, numeric) from public, anon, authenticated;
grant execute on function place_bet(uuid, bigint, integer, text, numeric) to service_role;