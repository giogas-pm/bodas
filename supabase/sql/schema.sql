-- Bodas: nomes, data e foto do casal NUNCA vão pro servidor (ficam no aparelho). Aqui só "pedido X pago" + trava (hash) + eventos.
create table if not exists public.bodas_pedidos (
  slug text primary key,
  unlocked boolean not null default true,
  valor numeric,
  payment_id text,
  trava text,
  created_at timestamptz not null default now()
);
create table if not exists public.bodas_eventos (
  id uuid primary key default gen_random_uuid(),
  evento text not null, slug text, meta jsonb,
  created_at timestamptz not null default now()
);
alter table public.bodas_pedidos enable row level security;
alter table public.bodas_eventos enable row level security;
drop policy if exists bodas_eventos_ins on public.bodas_eventos;
create policy bodas_eventos_ins on public.bodas_eventos for insert to anon with check (char_length(evento) <= 40 and (slug is null or char_length(slug) <= 24) and (meta is null or pg_column_size(meta) < 400));
revoke all on public.bodas_pedidos from anon, authenticated;
revoke select, update, delete on public.bodas_eventos from anon, authenticated;
create or replace function public.bodas_status(p_slug text) returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce((select unlocked from bodas_pedidos where slug = p_slug), false)
$$;
-- 1 pagamento = 1 casal: na 1ª impressão grava o hash do casal; depois devolve sempre o hash gravado.
create or replace function public.bodas_travar(p_slug text, p_trava text) returns text
language plpgsql security definer set search_path = public as $$
declare t text;
begin
  if p_trava is null or char_length(p_trava) > 80 then return null; end if;
  update bodas_pedidos set trava = p_trava where slug = p_slug and unlocked and trava is null;
  select trava into t from bodas_pedidos where slug = p_slug;
  return t;
end $$;
revoke all on function public.bodas_status(text) from public;
revoke all on function public.bodas_travar(text, text) from public;
grant execute on function public.bodas_status(text) to anon, authenticated;
grant execute on function public.bodas_travar(text, text) to anon, authenticated;
