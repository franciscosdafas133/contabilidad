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

## Deploy (recomendado: Render)

Vercel ha dado problemas con este stack (front estático + FastAPI + varios proyectos). Usa **Render**:

1. Entra a [https://render.com](https://render.com) e importa `franciscosdafas133/contabilidad`.
2. Elige **Blueprint** (`render.yaml`) o **Web Service** con Dockerfile.
3. Deploy. Health check: `/api/health`.

### Vercel (si lo sigues usando)

1. Deja **un solo** proyecto Vercel ligado al repo (borra duplicados: `web`, `*-trkn`, etc.).
2. Root Directory: `./`
3. Framework: FastAPI
4. **Desactiva Deployment Protection** (Settings → Deployment Protection → Off).
5. Commit actual: debe ser `2b12ee4` o más nuevo.

El progreso en hosting serverless/efímero usa SQLite en `/tmp` cuando aplica.

## Notas

- Los materiales originales del curso (`OneDrive_…`) **no** se suben al repositorio.
- Ver `docs/PLAN_IMPLEMENTACION.md` para el diseño pedagógico y el MVP.
