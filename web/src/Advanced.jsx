import React, { useEffect, useState } from 'react';
import { api, post, format } from './client';

const sections = { AC: 'Activo corriente', ANC: 'Activo no corriente', PC: 'Pasivo corriente', PNC: 'Pasivo no corriente', PN: 'Patrimonio neto', AO: 'Actividades de operación', AI: 'Actividades de inversión', AF: 'Actividades de financiamiento' };
const equityNames = { capital: 'Capital social', reserve: 'Reserva legal', voluntary_reserve: 'Reserva facultativa', retained: 'Resultados acumulados' };
const modeNames = { guided: 'Guiado', practice: 'Sin ayuda', learn: 'Aprender' };

export function Statement({ type, data, before, catalog, compact = false }) {
  if (!data) return null;
  const template = catalog.statement_templates?.[type] || { title: type };
  const row = (id, label, amount, old, total = false) => <tr key={id} className={`${total ? 'total-line' : ''} ${old !== undefined && String(amount) !== String(old) ? 'changed-line' : ''}`}><th scope="row">{label}</th><td className="numeric">{format(amount)}</td></tr>;
  let rows = [];
  if (type === 'ESF') {
    for (const section of Object.keys(sections).slice(0, 5)) {
      rows.push(<tr key={section} className="section-line"><th colSpan="2">{sections[section]}</th></tr>);
      for (const line of data.sections?.[section] || []) rows.push(row(line.id, line.name, line.amount, before ? before.sections?.[section]?.find(l => l.id === line.id)?.amount ?? '0.00' : undefined));
      rows.push(row(`total_${section}`, `Total ${sections[section].toLowerCase()}`, data.totals?.[section], before?.totals?.[section], true));
    }
    rows.push(row('assets', 'Total activo', data.assets, before?.assets, true), row('other', 'Total pasivo y patrimonio', data.liabilities_equity, before?.liabilities_equity, true));
  }
  if (type === 'ER') {
    const group = (section) => (data.lines || []).filter(l => l.section === section).forEach(l => rows.push(row(l.id, l.name, l.amount, before ? before.lines?.find(old => old.id === l.id)?.amount ?? '0.00' : undefined)));
    group('sales'); group('deductions'); rows.push(row('net_sales', 'Ventas netas', data.net_sales, before?.net_sales, true));
    group('cost'); rows.push(row('gross_profit', 'Utilidad bruta', data.gross_profit, before?.gross_profit, true));
    group('operating'); rows.push(row('operating_profit', 'Utilidad operativa', data.operating_profit, before?.operating_profit, true));
    group('financial'); rows.push(row('profit_before_tax', 'Utilidad antes del impuesto', data.profit_before_tax, before?.profit_before_tax, true));
    rows.push(row('tax', 'Impuesto a la renta', data.tax_expense, before?.tax_expense));
    rows.push(row('net_profit', 'Utilidad neta', data.net_profit, before?.net_profit, true));
  }
  if (type === 'EFE') {
    for (const section of ['AO', 'AI', 'AF']) {
      rows.push(<tr key={section} className="section-line"><th colSpan="2">{sections[section]}</th></tr>);
      (data.lines || []).filter(l => l.activity === section).forEach((l, i) => rows.push(row(`${section}_${i}`, l.label, l.amount)));
      rows.push(row(`total_${section}`, `Flujo neto ${section}`, data[section], before?.[section], true));
    }
    rows.push(row('change', 'Variación neta', data.change, before?.change, true), row('initial', 'Efectivo inicial', data.initial, before?.initial), row('final', 'Efectivo final', data.final, before?.final, true));
  }
  return <section className={`statement ${compact ? 'compact' : ''}`}><h2><span>{type}</span> {template.title}</h2><div className="table-scroll">{type === 'ECPN' ? <table className="equity-table"><thead><tr><th>Movimiento</th>{Object.values(equityNames).map(n => <th key={n}>{n}</th>)}</tr></thead><tbody>{(data.rows || []).map((r, i) => <tr key={i}><th scope="row">{r.label}</th>{Object.keys(equityNames).map(k => <td className="numeric" key={k}>{format(r[k] || 0)}</td>)}</tr>)}<tr className="total-line"><th>Saldo final</th>{Object.keys(equityNames).map(k => <td className={`numeric ${before && before[k] !== data[k] ? 'changed-line' : ''}`} key={k}>{format(data[k])}</td>)}</tr></tbody></table> : <table><thead><tr><th>Concepto</th><th className="numeric">S/</th></tr></thead><tbody>{rows}</tbody></table>}</div></section>;
}

const defaultFields = { amount: '1000', cash_part: '1000', cost: '400', activity: 'AF' };

export function Simulation({ catalog }) {
  const [scenario, setScenario] = useState('park_city'), [operations, setOperations] = useState([]), [result, setResult] = useState(null);
  const [type, setType] = useState('sale'), [fields, setFields] = useState({ ...defaultFields });
  const [predictions, setPredictions] = useState([{ account: 'cash', direction: 'increase' }, { account: 'sales', direction: 'increase' }]);
  const [feedback, setFeedback] = useState(null), [busy, setBusy] = useState(true), [error, setError] = useState(''), [view, setView] = useState('after');
  const [showAll, setShowAll] = useState(false);
  const definition = catalog.transaction_types.find(t => t.id === type) || catalog.transaction_types[0];
  const names = Object.fromEntries(catalog.accounts.map(a => [a.id, a.name]));
  useEffect(() => {
    const controller = new AbortController();
    setBusy(true); setResult(null); setError(''); setOperations([]); setFeedback(null);
    api('/simulate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ scenario, operations: [] }), signal: controller.signal }).then(setResult).catch(e => { if (e.name !== 'AbortError') setError(e.message); }).finally(() => { if (!controller.signal.aborted) setBusy(false); });
    return () => controller.abort();
  }, [scenario]);
  function changeType(next) {
    setType(next);
    setFeedback(null);
    const spec = catalog.transaction_types.find(t => t.id === next);
    const nextFields = {};
    for (const field of spec?.fields || []) nextFields[field] = defaultFields[field] || (field === 'activity' ? 'AF' : '0');
    setFields(nextFields);
  }
  async function execute(event) {
    event.preventDefault(); setBusy(true); setError('');
    const operation = { type, ...Object.fromEntries(definition.fields.map(k => [k, fields[k] || (k === 'activity' ? 'AF' : '0')])) };
    const next = [...operations, operation];
    try {
      const response = await post('/simulate', { scenario, operations: next, prediction: Object.fromEntries(predictions.filter(p => p.account).map(p => [p.account, p.direction])) });
      setResult(response); setOperations(next); setFeedback(response.prediction_feedback); setView('after');
    } catch (e) { setError(e.message); }
    finally { setBusy(false); }
  }
  async function undo() {
    setBusy(true); setError('');
    const next = operations.slice(0, -1);
    try { setResult(await post('/simulate', { scenario, operations: next })); setOperations(next); setFeedback(null); }
    catch (e) { setError(e.message); }
    finally { setBusy(false); }
  }
  const report = result?.[view];
  return <article><span className="eyebrow">Nivel de integración · Después de practicar cada estado</span><h1>Una operación, cuatro estados</h1><p>Predice las cuentas que cambian, aplica un hecho y sigue su efecto en los estados.</p>
    <div className="exercise-selector"><label htmlFor="scenario">Caso inicial</label><select id="scenario" value={scenario} disabled={busy} onChange={e => setScenario(e.target.value)}><option value="park_city">Park City · Caso completo de 2020</option><option value="empty">Empresa nueva · Sin saldos</option></select></div>
    {scenario === 'park_city' && <details className="case-note"><summary>Criterios usados en Park City</summary><p>Conservamos los decimales del ER y ECPN. Los dividendos declarados son S/ 28 221,15 y el EFE paga S/ 28 221,00; se interpretan S/ 0,15 pendientes. El activo recalculado es S/ 841 395,67. El Excel redondea algunas líneas del ESF y contiene un bloque auxiliar con referencias rotas.</p><p>Intereses pagados: AF, según el solucionario. Las inversiones CP de este caso se muestran separadas del efectivo. IR 29,5%; reserva legal 10% con tope 20% del capital.</p></details>}
    <form className="operation-form" onSubmit={execute}><h2>1. Elige el hecho económico</h2><div className="operation-fields"><label htmlFor="operation-type">Operación<select id="operation-type" value={type} onChange={e => changeType(e.target.value)}>{catalog.transaction_types.map(t => <option key={t.id} value={t.id}>{t.label}</option>)}</select></label>{definition.fields.map(field => <label key={field} htmlFor={`field-${field}`}>{({ amount: 'Importe total (S/)', cash_part: 'Parte al contado (S/)', cost: 'Costo indicado (S/)', activity: 'Intereses pagados: actividad' })[field]}{field === 'activity' ? <select id={`field-${field}`} value={fields[field] || 'AF'} onChange={e => setFields(prev => ({ ...prev, [field]: e.target.value }))}><option value="AF">AF · Según Park City / Las Vegas</option><option value="AO">AO · Si el enunciado lo pide</option></select> : <input id={`field-${field}`} type="text" inputMode="decimal" required value={fields[field] || ''} onChange={e => setFields(prev => ({ ...prev, [field]: e.target.value }))} />}</label>)}</div>
      <h2>2. Predice los efectos directos</h2><p className="muted">Incluye las cuentas que cambian antes de recalcular impuesto y reserva. Una venta con costo requiere ambos efectos.</p>
      {predictions.map((p, i) => <div className="prediction-row" key={i}><select aria-label={`Cuenta prevista ${i + 1}`} value={p.account} onChange={e => setPredictions(prev => prev.map((v, j) => j === i ? { ...v, account: e.target.value } : v))}><option value="">Seleccionar cuenta</option>{catalog.accounts.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}</select><select aria-label={`Efecto previsto ${i + 1}`} value={p.direction} onChange={e => setPredictions(prev => prev.map((v, j) => j === i ? { ...v, direction: e.target.value } : v))}><option value="increase">Aumenta</option><option value="decrease">Disminuye</option></select>{predictions.length > 2 && <button type="button" aria-label={`Quitar predicción ${i + 1}`} onClick={() => setPredictions(prev => prev.filter((_, j) => j !== i))}>Quitar</button>}</div>)}
      <button type="button" className="text-button" disabled={predictions.length >= 8} onClick={() => setPredictions(prev => [...prev, { account: '', direction: 'increase' }])}>+ Añadir cuenta prevista</button>
      <div className="submit-bar"><span>{operations.length} operaciones aplicadas a este caso.</span><div className="button-row"><button type="button" disabled={busy || !operations.length} onClick={undo}>Deshacer última</button><button type="submit" className="primary" disabled={busy || predictions.filter(p => p.account).length < 2}>{busy ? 'Calculando…' : 'Aplicar operación'}</button></div></div>
    </form>
    {error && <p className="error" role="alert">{error}</p>}
    {feedback && <section className="prediction-feedback" role="status"><h2>3. Contrasta tu predicción</h2><ul>{feedback.map(f => <li key={f.account}>{names[f.account] || f.account}: <strong className={f.correct ? 'good' : 'bad'}>{f.correct ? 'correcto' : f.message}</strong>{!f.correct && f.expected && ` · ${f.expected === 'increase' ? 'aumenta' : 'disminuye'}`}</li>)}</ul></section>}
    {result && report && <><div className="checks" role="status"><span>{report.checks?.equation ? '✓' : '✕'} A = P + PN</span><span>{report.checks?.cash ? '✓' : '✕'} EFE concilia con efectivo</span><span>{report.checks?.equity ? '✓' : '✕'} ECPN concilia con ESF</span></div>
    {!!result.changes?.length && <div className="table-scroll change-table"><table><caption>Cambios de la última operación</caption><thead><tr><th>Cuenta</th><th>Antes</th><th>Después</th><th>Origen</th></tr></thead><tbody>{result.changes.map(c => <tr key={c.account}><th>{names[c.account] || c.account}</th><td className="numeric">{format(c.before)}</td><td className="numeric">{format(c.after)}</td><td>{c.origin === 'direct' ? 'Directo' : 'Recalculado'}</td></tr>)}</tbody></table></div>}
    <div className="view-toolbar"><div className="button-row"><button type="button" className={view === 'before' ? 'selected' : ''} aria-pressed={view === 'before'} onClick={() => setView('before')}>Antes de la última operación</button><button type="button" className={view === 'after' ? 'selected' : ''} aria-pressed={view === 'after'} onClick={() => setView('after')}>Después</button></div><label><input type="checkbox" checked={showAll} onChange={e => setShowAll(e.target.checked)} /> Expandir estados</label></div>
    <p className="period">{scenario === 'park_city' ? 'Park City SAC · Del 1 de enero al 31 de diciembre de 2020 · ESF al 31 de diciembre de 2020' : 'Empresa nueva · Período de simulación'} · S/</p>
    <div className={`statement-grid ${showAll ? 'expanded' : ''}`}>{['ER', 'ECPN', 'ESF', 'EFE'].map(t => <Statement key={t} type={t} data={report[t]} before={view === 'after' ? result.before?.[t] : undefined} catalog={catalog} compact />)}</div>
    <details className="source-data"><summary>Traza de reglas y fuentes</summary><div className="trace-list">{(result.after?.trace || []).map((t, i) => <div key={i}><b>{t.label || t.rule_id}</b><p>{t.message}</p><small>Regla {t.rule_id} · {t.source}</small></div>)}</div></details></>}
  </article>;
}

export function Progress() {
  const [data, setData] = useState(null), [error, setError] = useState('');
  useEffect(() => { const c = new AbortController(); api('/progress', { signal: c.signal }).then(setData).catch(e => { if (e.name !== 'AbortError') setError(e.message); }); return () => c.abort(); }, []);
  if (error) return <p className="error" role="alert">{error}</p>;
  if (!data) return <p role="status">Cargando progreso…</p>;
  const names = { classification: 'Reconocimiento', equation: 'Ecuación contable', esf: 'ESF', er: 'ER', ecpn: 'ECPN', efe: 'EFE' };
  const errorNames = { missing: 'Respuesta vacía', invalid: 'Formato numérico', sign: 'Signo', structure: 'Sección', efe: 'Actividad EFE', classification: 'Elemento', calculation: 'Cálculo', relationship: 'Relación entre estados', equity: 'Patrimonio' };
  const pct = (correct, total) => total ? Math.round(correct / total * 100) : 0;
  return <article><span className="eyebrow">Aprendizaje en este equipo</span><h1>Mi progreso</h1><p>Se cuentan todos los intentos comprobados, incluidos los que todavía tienen diferencias.</p>
    {!data.attempts.length ? <div className="empty-state"><h2>Aún no hay intentos</h2><p>Completa un ejercicio guiado o una práctica y pulsa Comprobar respuestas.</p></div> : <><div className="progress-summary"><span><strong>{data.attempts.length}</strong> intentos</span><span><strong>{data.attempts.filter(a => a.completed).length}</strong> completados</span><span><strong>{Math.round(data.attempts.reduce((n, a) => n + a.elapsed_seconds, 0) / 60)}</strong> minutos registrados</span></div>
    <h2>Precisión por habilidad</h2><div className="skill-list">{Object.entries(data.skills).map(([k, s]) => <div key={k}><div><b>{names[k] || k}</b><span>{s.correct} / {s.total} respuestas · {pct(s.correct, s.total)}%</span></div><progress value={s.correct} max={Math.max(s.total, 1)} aria-label={`Precisión ${names[k] || k}`} /></div>)}</div>
    {data.recommendations.length > 0 && <section className="recommendation"><h2>Qué practicar ahora</h2>{data.recommendations.map(r => <p key={r.skill}><b>{names[r.skill] || r.skill}:</b> {r.message}</p>)}</section>}
    <div className="sheet-heading"><h2>Errores observados</h2></div><ul className="error-counts">{Object.entries(data.errors).map(([k, n]) => <li key={k}>{errorNames[k] || k}<b>{n}</b></li>)}</ul>
    <div className="sheet-heading"><h2>Historial de intentos</h2><a href="/api/progress/export" download>Exportar datos</a></div><div className="table-scroll"><table><thead><tr><th>Ejercicio</th><th>Modo</th><th>Resultado</th><th>Fecha</th></tr></thead><tbody>{[...data.attempts].reverse().map((a, i) => <tr key={i}><td>{a.exercise}</td><td>{modeNames[a.mode] || a.mode}</td><td>{a.correct} / {a.total}{a.completed && ' · Completado'}</td><td>{new Date(a.created_at).toLocaleString('es-PE')}</td></tr>)}</tbody></table></div></>}
    <p className="source">Estos registros permiten preparar un piloto. Por sí solos no demuestran mejora pedagógica: se necesita comparar pretest, postest y transferencia con alumnos.</p>
  </article>;
}
