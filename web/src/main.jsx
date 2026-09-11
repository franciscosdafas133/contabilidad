import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';
import { api, post, format } from './client';
import { Statement, Simulation, Progress } from './Advanced';
const skillNames = { classification: 'Reconocimiento', equation: 'Ecuación contable', esf: 'ESF', er: 'ER', ecpn: 'ECPN', efe: 'EFE' };
const modes = [['learn', 'Aprender un estado', '01'], ['guided', 'Ejercicio guiado', '02'], ['practice', 'Práctica sin ayuda', '03'], ['simulation', 'Integración y simulador', '04'], ['progress', 'Mi progreso', '05']];
const learnDefaults = { ESF: 'pd2_esf', ER: 'pd3_er', ECPN: 'pd3_ecpn', EFE: 'pd3_efe' };

function DataSheet({ exercise, catalog }) {
  const names = Object.fromEntries(catalog.accounts.map(a => [a.id, a.name]));
  const data = exercise.data || {};
  let rows = [];
  if (data.balances) rows = Object.entries(data.balances).map(([k, v]) => [names[k] || k, format(v)]);
  if (data.flows) rows = [['Efectivo inicial', format(data.initial)], ...data.flows.map(f => [f.label, format(f.amount)])];
  if (exercise.kind === 'ecpn' && data.opening) {
    const labels = { profit: 'Utilidad del ejercicio', contribution: 'Aporte de capital', capitalization: 'Capitalización de utilidades', voluntary: 'Reserva facultativa', dividends: 'Dividendos declarados' };
    rows = [
      ...Object.entries(data.opening).map(([k, v]) => [`${names[k] || k} inicial`, format(v)]),
      ...Object.entries(data).filter(([k, v]) => k !== 'opening' && v != null && v !== '').map(([k, v]) => [labels[k] || k, format(v)]),
    ];
  }
  if (data.rows) return <details className="source-data" open><summary>Hechos y matriz de operaciones · {data.rows.length} filas</summary><p className="muted">Cada fila representa un hecho del material. Completa en la plantilla los saldos o efectos pedidos; las cifras negativas representan disminuciones.</p><div className="table-scroll"><table><thead><tr><th>Hecho del material</th><th>Detalle</th></tr></thead><tbody>{data.rows.map((r, i) => <tr key={i}><td>{r.label}</td><td>{r.deltas ? Object.entries(r.deltas).map(([k, v]) => <span className="fact" key={k}>{names[k] || k}: <b>{format(v)}</b></span>) : (r.prompt || 'Completa los efectos en tu solución.')}</td></tr>)}</tbody></table></div></details>;
  if (!rows.length) {
    if (exercise.skill === 'classification') return <details className="source-data" open><summary>Cómo clasificar</summary><p className="muted">Elige el elemento contable de cada cuenta: Activo, Pasivo, Patrimonio Neto, Ingreso o Gasto. Las contra-cuentas (p. ej. depreciación acumulada) mantienen el elemento del activo y restan en su sección.</p></details>;
    return null;
  }
  return <details className="source-data" open><summary>Datos del enunciado</summary><div className="table-scroll"><table><thead><tr><th>Concepto</th><th className="numeric">Importe (S/)</th></tr></thead><tbody>{rows.map(([name, value], i) => <tr key={i}><td>{name}</td><td className="numeric">{value}</td></tr>)}</tbody></table></div></details>;
}

function ruleText(catalog, ruleId) {
  const rule = catalog?.rules?.[ruleId];
  if (!rule) return { text: 'Regla no disponible en el catálogo.', source: '' };
  return rule;
}

function filledCount(answers) {
  return Object.values(answers).filter(v => String(v ?? '').trim() !== '').length;
}

function Exercise({ id, mode, catalog, onSaved }) {
  const [exercise, setExercise] = useState(null), [solution, setSolution] = useState(null);
  const [answers, setAnswers] = useState({}), [result, setResult] = useState(null), [error, setError] = useState('');
  const [busy, setBusy] = useState(false), [hint, setHint] = useState(''), [started] = useState(Date.now());
  useEffect(() => {
    const controller = new AbortController();
    setExercise(null); setSolution(null); setAnswers({}); setResult(null); setError(''); setHint('');
    api(`/exercises/${id}${mode === 'learn' ? '/learn' : ''}`, { signal: controller.signal }).then(data => {
      setExercise(data.exercise || data); setSolution(data.solution || null);
    }).catch(e => { if (e.name !== 'AbortError') setError(e.message); });
    return () => controller.abort();
  }, [id, mode]);
  async function check(event) {
    event.preventDefault(); setBusy(true); setError('');
    try {
      const response = await post(`/exercises/${id}/check`, { attempt_id: crypto.randomUUID(), mode, answers, elapsed_seconds: Math.min(86400, Math.round((Date.now() - started) / 1000)) });
      setResult(response); onSaved();
    } catch (e) { setError(e.message); }
    finally { setBusy(false); }
  }
  if (!exercise) return error ? <p role="alert" className="error">{error}</p> : <p role="status">Cargando ejercicio…</p>;
  const graded = Object.fromEntries((result?.feedback || []).map(f => [f.id, f]));
  const completed = filledCount(answers);
  return <article>
    <div className="exercise-heading"><span className="eyebrow">{skillNames[exercise.skill]} / Unidades 1–4</span><h1>{exercise.title}</h1><p>{exercise.prompt}</p><p className="period">{exercise.period} · Expresado en soles</p></div>
    {mode === 'guided' && <ol className="steps" aria-label="Pasos orientativos"><li className="done">Lee los hechos</li><li className={completed ? 'done' : ''}>Identifica cuentas y efectos</li><li className={result ? 'done' : ''}>Calcula y comprueba</li></ol>}
    {mode === 'practice' && <p className="practice-note">Sin pistas durante el intento. Las respuestas aparecen después de comprobar. Usa dos decimales y punto decimal, sin separador de miles.</p>}
    <DataSheet exercise={exercise} catalog={catalog} />
    {mode === 'learn' && ['matrix', 'er', 'efe', 'ecpn'].includes(exercise.kind) && <Statement type={{ matrix: 'ESF', er: 'ER', efe: 'EFE', ecpn: 'ECPN' }[exercise.kind]} data={exercise.kind === 'matrix' ? solution?.statement : solution} catalog={catalog} />}
    <form onSubmit={check}>
      <div className="sheet-heading"><h2>{mode === 'learn' ? 'Plantilla resuelta' : 'Tu solución'}</h2><span>{exercise.tasks.length} respuestas {mode !== 'learn' && `· ${completed} completadas`}</span></div>
      <div className="table-scroll answer-sheet"><table><thead><tr><th scope="col">Cuenta o resultado</th><th scope="col">{exercise.skill === 'classification' ? 'Elemento' : 'Respuesta'}</th>{mode !== 'practice' && <th scope="col">Regla</th>}</tr></thead><tbody>{exercise.tasks.map(task => {
        const feedback = graded[task.id];
        const rule = ruleText(catalog, task.rule_id);
        return <React.Fragment key={task.id}><tr className={feedback ? feedback.correct ? 'correct-row' : 'incorrect-row' : ''}>
          <th scope="row"><label htmlFor={`answer-${task.id}`}>{task.label}</label></th>
          <td>{mode === 'learn' ? <strong>{task.type === 'choice' ? solution?.[task.id] : format(solution?.[task.id] ?? 0)}</strong> : task.type === 'choice' ?
            <select id={`answer-${task.id}`} value={answers[task.id] || ''} onChange={e => { const value = e.target.value; setAnswers(prev => ({ ...prev, [task.id]: value })); setResult(null); }}><option value="">Seleccionar</option>{task.options.map(o => <option key={o} value={o}>{o}</option>)}</select> :
            <input id={`answer-${task.id}`} aria-describedby={feedback ? `feedback-${task.id}` : undefined} type="text" inputMode="decimal" placeholder="0.00" autoComplete="off" value={answers[task.id] || ''} maxLength={40} onChange={e => { const value = e.target.value; setAnswers(prev => ({ ...prev, [task.id]: value })); setResult(null); }} />}</td>
          {mode !== 'practice' && <td><button type="button" className="text-button" aria-expanded={hint === task.id} onClick={() => setHint(h => h === task.id ? '' : task.id)}>{hint === task.id ? 'Ocultar' : 'Ver regla'}</button></td>}
        </tr>{hint === task.id && mode !== 'practice' && <tr><td colSpan="3" className="hint"><b>{task.rule_id}</b> · {rule.text}{rule.source && <small>{rule.source}</small>}</td></tr>}
        {feedback && <tr><td id={`feedback-${task.id}`} colSpan={mode === 'practice' ? 2 : 3} className={`feedback ${feedback.correct ? 'good' : 'bad'}`}><strong>{feedback.message}</strong>{!feedback.correct && <> Respuesta: {feedback.expected}. {feedback.explanation}<small>Regla {feedback.rule_id} · {feedback.source}</small></>}</td></tr>}</React.Fragment>;
      })}</tbody></table></div>
      {mode !== 'learn' && <div className="submit-bar"><span>Revisa signos, secciones y decimales.</span><button className="primary" disabled={busy} type="submit">{busy ? 'Comprobando…' : 'Comprobar respuestas'}</button></div>}
    </form>
    {error && <p role="alert" className="error">{error}</p>}
    {result && <section className={`result ${result.completed ? 'success' : ''}`} role="status"><h2>{result.completed ? 'Ejercicio completado' : 'Revisa las diferencias'}</h2><p>{result.correct} de {result.total} respuestas correctas. Tu intento quedó guardado en Mi progreso.</p></section>}
    <footer className="source"><strong>Material del curso</strong><br />{exercise.source}</footer>
  </article>;
}

function App() {
  const [mode, setMode] = useState('guided'), [catalog, setCatalog] = useState(null), [exercises, setExercises] = useState([]);
  const [selected, setSelected] = useState('pd1_clasificacion'), [error, setError] = useState(''), [revision, setRevision] = useState(0);
  useEffect(() => { Promise.all([api('/catalog'), api('/exercises')]).then(([c, e]) => { setCatalog(c); setExercises(e); }).catch(e => setError(e.message)); }, []);
  function changeMode(key) {
    setMode(key);
    if (key === 'learn' && !Object.values(learnDefaults).includes(selected)) setSelected(learnDefaults.ESF);
  }
  const currentMode = modes.find(m => m[0] === mode);
  return <div className="app-shell"><a className="skip-link" href="#workspace">Ir al ejercicio</a><aside className="sidebar"><div className="brand"><span className="brand-mark">=</span><div>Fundamentos<small>TALLER DE CONTABILIDAD</small></div></div><div className="course-label">160092 · UP · 2026-2</div><nav aria-label="Modos de estudio">{modes.map(([key, label, n]) => <button key={key} aria-current={mode === key ? 'page' : undefined} className={mode === key ? 'active' : ''} onClick={() => changeMode(key)}><span>{n}</span>{label}</button>)}</nav><div className="sidebar-bottom"><b>De la ecuación a los estados</b><p>Trabaja primero un estado. Después, conecta los cuatro.</p><span>Progreso en este equipo</span></div></aside>
    <div className="main-shell"><header className="topbar"><span>{currentMode[1]}</span><span className="muted">Fundamentos de Contabilidad</span></header><main id="workspace">
      {error ? <p role="alert" className="error">No se pudo cargar la aplicación. {error} <button type="button" onClick={() => location.reload()}>Reintentar</button></p> : !catalog ? <p role="status">Preparando el taller…</p> : <>
      {['learn', 'guided', 'practice'].includes(mode) ? <>{mode === 'learn' && <div className="state-picker" aria-label="Elegir estado">{Object.entries(learnDefaults).map(([label, id]) => <button type="button" key={id} className={selected === id ? 'selected' : ''} onClick={() => setSelected(id)}>{label}</button>)}</div>}<div className="exercise-selector"><label htmlFor="exercise-choice">Ejercicio</label><select id="exercise-choice" value={selected} onChange={e => setSelected(e.target.value)}>{exercises.map(e => <option key={e.id} value={e.id}>{e.title} · {skillNames[e.skill]}</option>)}</select></div><Exercise key={`${selected}-${mode}`} id={selected} mode={mode} catalog={catalog} onSaved={() => setRevision(r => r + 1)} /></> : mode === 'simulation' ? <Simulation catalog={catalog} /> : <Progress key={revision} />}
      </>}
    </main></div></div>;
}
createRoot(document.getElementById('root')).render(<App />);
