import os
from typing import Literal
from uuid import UUID
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field, ConfigDict
from engine.catalog import ROOT, read_knowledge
from engine.money import AccountingError, serialize
from engine.exercises import get_exercise, public_exercise, solve
from engine.feedback import check_answers
from engine.scenarios import park_city
from engine.equation import Ledger
from engine.projections import project
from engine.transactions import apply_operation
from backend.storage import ProgressStore


class CheckRequest(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    attempt_id: str = Field(min_length=36,max_length=36)
    mode: Literal['guided','practice']
    answers: dict[str,str]
    elapsed_seconds: int = Field(ge=0,le=86400)


class SimulationRequest(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    scenario: Literal['empty','park_city']='empty'
    operations: list[dict[str,str]]=Field(default_factory=list,max_length=100)
    prediction: dict[str,Literal['increase','decrease']]=Field(default_factory=dict,max_length=62)


def create_app(db_path=None):
    app=FastAPI(title='Fundamentos de Contabilidad',version='0.1.0')
    if db_path is None:
        db_path=os.getenv('CONTA_DB')
    if not db_path:
        db_path='/tmp/progress.sqlite3' if os.getenv('VERCEL') else str(ROOT/'data/progress.sqlite3')
    store=ProgressStore(db_path)
    app.state.store=store
    allowed_hosts=['localhost','127.0.0.1','testserver','.vercel.app']
    extra_hosts=[h.strip() for h in os.getenv('ALLOWED_HOSTS','').split(',') if h.strip()]
    allowed_hosts.extend(extra_hosts)
    app.add_middleware(TrustedHostMiddleware,allowed_hosts=allowed_hosts)

    def origin_ok(origin:str)->bool:
        from urllib.parse import urlparse
        host=(urlparse(origin).hostname or '').lower()
        if host in ('localhost','127.0.0.1') or host.endswith('.vercel.app'):
            return True
        allowed={h.strip().lower() for h in os.getenv('ALLOWED_ORIGINS','').split(',') if h.strip()}
        return host in allowed or origin.rstrip('/') in allowed

    @app.middleware('http')
    async def local_writes(request:Request,call_next):
        if request.method not in ('GET','HEAD','OPTIONS'):
            origin=request.headers.get('origin')
            if origin and not origin_ok(origin):
                return JSONResponse({'detail':'Origen no permitido para una escritura local.'},status_code=403)
            if int(request.headers.get('content-length','0'))>250000:
                return JSONResponse({'detail':'Solicitud demasiado grande.'},status_code=413)
        response=await call_next(request)
        response.headers['X-Content-Type-Options']='nosniff'
        return response

    @app.exception_handler(AccountingError)
    async def invalid_accounting(request,error):
        return JSONResponse({'detail':str(error)},status_code=422)

    def find(id):
        try: return get_exercise(id)
        except KeyError: raise HTTPException(404,'Ejercicio no encontrado.')

    @app.get('/api/health')
    def health(): return {'status':'ok','engine':'deterministic','version':'0.1.0'}

    @app.get('/api/catalog')
    def catalog():
        return {name:read_knowledge(name) for name in ('accounts','rules','statement_templates','transaction_types')}

    @app.get('/api/exercises')
    def exercises():
        return [{k:ex[k] for k in ('id','title','skill','period')} for ex in read_knowledge('exercises')]

    @app.get('/api/exercises/{id}')
    def exercise(id:str): return public_exercise(find(id))

    @app.get('/api/exercises/{id}/learn')
    def learn(id:str):
        ex=find(id)
        return serialize({'exercise':public_exercise(ex),'solution':solve(ex)})

    @app.post('/api/exercises/{id}/check')
    def check(id:str,body:CheckRequest):
        try: UUID(body.attempt_id)
        except ValueError: raise HTTPException(422,'Identificador de intento inválido.')
        if len(body.answers)>250 or any(len(v)>100 for v in body.answers.values()):
            raise HTTPException(422,'Demasiadas respuestas o valor demasiado largo.')
        ex=find(id);result=check_answers(ex,solve(ex),body.answers)
        try: return store.record(body.attempt_id,id,body.mode,body.elapsed_seconds,body.answers,result)
        except ValueError as error: raise HTTPException(409,str(error))

    @app.get('/api/progress')
    def progress(): return store.report()

    @app.get('/api/progress/export')
    def export():
        return JSONResponse(store.report(),headers={'Content-Disposition':'attachment; filename="progreso-contabilidad.json"'})

    @app.post('/api/simulate')
    def simulate(body:SimulationRequest):
        ledger=park_city() if body.scenario=='park_city' else Ledger()
        before=project(ledger)
        for index,operation in enumerate(body.operations):
            if index==len(body.operations)-1: before=project(ledger)
            apply_operation(ledger,operation)
        after=project(ledger)
        changes=[]
        for key in sorted(set(before['balances'])|set(after['balances'])):
            old=before['balances'].get(key,0);new=after['balances'].get(key,0)
            if old!=new:
                direct=bool(ledger.history and key in ledger.history[-1]['deltas'])
                changes.append({'account':key,'before':old,'after':new,'delta':new-old,'origin':'direct' if direct else 'recalculated'})
        predicted=[]
        if body.operations and body.prediction:
            from engine.catalog import accounts
            if set(body.prediction)-set(accounts()): raise AccountingError('Cuenta de predicción desconocida.')
            direct=ledger.history[-1]['deltas']
            for key in sorted(set(body.prediction)|set(direct)):
                expected=('increase' if direct[key]>0 else 'decrease') if key in direct else None
                guessed=body.prediction.get(key)
                correct=guessed==expected
                if expected is None:
                    message='No tiene efecto directo.'
                elif key not in body.prediction:
                    message='Faltó incluir esta cuenta.'
                elif correct:
                    message='Correcto.'
                else:
                    message='Revisa la dirección del efecto.'
                predicted.append({'account':key,'expected':expected,'correct':correct,'message':message})
        return serialize({'before':before,'after':after,'changes':changes,'operation_count':len(body.operations),'prediction_feedback':predicted})

    build=ROOT/'web/dist'
    if build.exists():
        # Vercel promociona este frontend al CDN; en local sirve web/dist.
        app.frontend('/',directory=build,fallback='index.html',check_dir=False)
    return app


app=create_app()
