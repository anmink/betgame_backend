create or replace function collect_cups(
  p_user_id uuid,
  p_cups integer,
  p_now timestamptz,
  p_cooldown interval
) returns integer
language plpgsql as $$
declare
  v_becher integer;
begin
  update users
  set becher = becher + p_cups,
      last_collect_at = p_now
  where id = p_user_id
    and (last_collect_at is null or last_collect_at <= p_now - p_cooldown)
  returning becher into v_becher;

  if not found then
    raise exception 'cooldown_active';
  end if;

  return v_becher;
end;
$$;

revoke execute on function collect_cups(uuid, integer, timestamptz, interval) from public, anon, authenticated;
grant execute on function collect_cups(uuid, integer, timestamptz, interval) to service_role;