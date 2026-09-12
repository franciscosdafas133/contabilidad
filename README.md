# Fundamentos de Contabilidad (UP 2026-2)

Taller educativo localhost / web: ecuación contable y los cuatro EEFF (ESF, ER, ECPN, EFE) con motor **determinístico** (sin LLM en runtime).

## Stack

- Motor + API: Python · FastAPI
- Frontend: React · Vite
- Conocimiento: `knowledge/` + tests golden en `tests/`

## Desarrollo local

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
pip install -e ".[test]"
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000

# otra terminal
cd web
npm install
npm run dev
```

- App: http://127.0.0.1:5173 (proxy `/api` → `:8000`)
- API directa: http://127.0.0.1:8000/api/health

## Deploy en Vercel

1. Importa el repo en [Vercel](https://vercel.com/new).
2. Framework preset: **FastAPI**.
3. **Root Directory: déjalo vacío / `./`** (NO pongas `web`).
4. No hace falta tocar Build Command (viene de `vercel.json`).
5. Deploy.

Comprueba después: `https://TU-URL.vercel.app/api/health` debe devolver JSON.

Si ves HTML en vez de JSON, desactiva **Deployment Protection** (Settings → Deployment Protection).

El progreso en Vercel usa SQLite en `/tmp` (efímero entre instancias serverless).

## Notas

- Los materiales originales del curso (`OneDrive_…`) **no** se suben al repositorio.
- Ver `docs/PLAN_IMPLEMENTACION.md` para el diseño pedagógico y el MVP.
