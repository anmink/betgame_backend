create or replace function settle_bet(p_bet_id bigint, p_won boolean, p_payout integer)
returns void
language plpgsql as $$
declare
  v_user_id uuid;
begin
  update bets
  set status = case when p_won then 'won' else 'lost' end,
      payout = case when p_won then p_payout else 0 end
  where id = p_bet_id and status = 'open'
  returning user_id into v_user_id;

  if not found then
    return;
  end if;

  if p_won then
    update users set coins = coins + p_payout where id = v_user_id;
  end if;
end;
$$;

revoke execute on function settle_bet(bigint, boolean, integer) from public, anon, authenticated;
grant execute on function settle_bet(bigint, boolean, integer) to service_role;