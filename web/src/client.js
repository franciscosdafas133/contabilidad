export async function api(path, options) {
  const response = await fetch(`/api${path}`, options);
  const text = await response.text();
  let body = null;
  try { body = text ? JSON.parse(text) : null; } catch {
    if (!response.ok) throw new Error('El servidor no respondió correctamente. Revisa que la API esté en marcha.');
    throw new Error('Respuesta inválida del servidor.');
  }
  if (!response.ok) {
    const detail = body?.detail;
    throw new Error(typeof detail === 'string' ? detail : Array.isArray(detail) ? detail.map(d => d.msg || d).join(' ') : 'Revisa los datos enviados.');
  }
  return body;
}
export const post = (path, body) => api(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
export const format = (value) => {
  const n = Number(value);
  if (!Number.isFinite(n)) return '—';
  return new Intl.NumberFormat('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(n);
};
