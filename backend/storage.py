import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


class ProgressStore:
    def __init__(self,path):
        self.path=str(path)
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS attempts (
                id TEXT PRIMARY KEY, exercise TEXT NOT NULL, mode TEXT NOT NULL,
                created_at TEXT NOT NULL, elapsed_seconds INTEGER NOT NULL,
                fingerprint TEXT NOT NULL, result TEXT NOT NULL)''')

    def connect(self):
        return sqlite3.connect(self.path,timeout=10)

    def record(self,id,exercise,mode,elapsed,answers,result):
        fingerprint=hashlib.sha256(json.dumps([exercise,mode,answers],sort_keys=True).encode()).hexdigest()
        with self.connect() as db:
            db.execute('INSERT OR IGNORE INTO attempts VALUES (?,?,?,?,?,?,?)',
                (id,exercise,mode,datetime.now(timezone.utc).isoformat(),elapsed,fingerprint,json.dumps(result,ensure_ascii=False)))
            saved=db.execute('SELECT fingerprint,result FROM attempts WHERE id=?',(id,)).fetchone()
            if saved[0]!=fingerprint: raise ValueError('Este intento ya fue guardado con otras respuestas.')
            return json.loads(saved[1])

    def report(self):
        with self.connect() as db:
            rows=db.execute('SELECT exercise,mode,created_at,elapsed_seconds,result FROM attempts ORDER BY created_at').fetchall()
        skills={};errors={};attempts=[]
        for exercise,mode,created,elapsed,raw in rows:
            result=json.loads(raw)
            attempts.append({'exercise':exercise,'mode':mode,'created_at':created,'elapsed_seconds':elapsed,
                             'correct':result['correct'],'total':result['total'],'completed':result['completed']})
            for feedback in result['feedback']:
                skill=skills.setdefault(feedback['skill'],{'correct':0,'total':0})
                skill['correct']+=int(feedback['correct']);skill['total']+=1
                if not feedback['correct']: errors[feedback['error_type']]=errors.get(feedback['error_type'],0)+1
        recommendations=[{'skill':k,'message':'Practica un ejercicio guiado antes de volver al modo sin ayuda.'}
                         for k,v in skills.items() if v['correct']/v['total']<.7]
        return {'attempts':attempts,'skills':skills,'errors':errors,'recommendations':recommendations}
