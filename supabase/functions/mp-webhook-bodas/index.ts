// Bodas — webhook do Mercado Pago. Pagamento aprovado (>= R$24,90) registra o pedido como pago
// (external_reference = slug). Nenhum dado do casal passa por aqui. Mesma receita da Carta do Noel.
Deno.serve(async (req) => {
  try {
    const token = Deno.env.get("MP_ACCESS_TOKEN");
    const SB_URL = Deno.env.get("SUPABASE_URL")!;
    const SVC = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const url = new URL(req.url);
    let pid: string | null = url.searchParams.get("data.id") || url.searchParams.get("id");
    let type: string | null = url.searchParams.get("type") || url.searchParams.get("topic");
    if (!pid || (type && type !== "payment")) {
      const b = await req.json().catch(() => null as any);
      if (b) { type = b.type || b.topic || type; pid = (b.data && b.data.id) || b.id || pid; }
    }
    if (!pid || (type && type !== "payment")) return new Response("ignored", { status: 200 });
    if (!token) return new Response("sem_token", { status: 200 });
    const pay = await fetch("https://api.mercadopago.com/v1/payments/" + encodeURIComponent(pid), {
      headers: { Authorization: "Bearer " + token },
    }).then((r) => r.json());
    if (pay && pay.status === "approved" && pay.external_reference && Number(pay.transaction_amount) >= 24.9) {
      await fetch(`${SB_URL}/rest/v1/bodas_pedidos?on_conflict=slug`, {
        method: "POST",
        headers: {
          apikey: SVC, Authorization: "Bearer " + SVC, "Content-Type": "application/json",
          Prefer: "resolution=merge-duplicates,return=minimal",
        },
        body: JSON.stringify({ slug: String(pay.external_reference), unlocked: true, valor: pay.transaction_amount, payment_id: String(pid) }),
      });
      return new Response("ok:unlocked", { status: 200 });
    }
    return new Response("ok", { status: 200 });
  } catch (e) {
    return new Response("err:" + String(e), { status: 200 });
  }
});
