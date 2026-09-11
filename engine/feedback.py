from .money import number, display, AccountingError
from .catalog import read_knowledge


def check_answers(exercise, expected, submitted):
    rules=read_knowledge('rules')
    if set(submitted)-{t['id'] for t in exercise['tasks']}:
        raise AccountingError('Hay respuestas para campos ajenos a este ejercicio.')
    feedback=[]
    for task in exercise['tasks']:
        key=task['id'];target=expected.get(key,0);answer=submitted.get(key,'').strip()
        correct=False;kind='missing'
        if task['type']=='choice':
            if answer:
                correct=answer==target
                kind='structure' if key.startswith('section_') else 'efe' if task['skill']=='efe' else 'classification'
            shown=target
        else:
            shown=display(target)
            if answer:
                try:
                    parsed=number(answer)
                    # Compare against displayed cent precision; a larger tolerance could hide errors.
                    correct=parsed==number(shown)
                    kind='sign' if parsed==-number(shown) and parsed!=0 else 'relationship' if key in ('net_profit','final') else 'equity' if task['skill']=='ecpn' else 'calculation'
                except AccountingError: kind='invalid'
        if correct: kind='correct'
        messages={'correct':'Correcto.','missing':'Completa esta respuesta.','invalid':'Escribe un número finito sin separador de miles.',
                  'sign':'La magnitud coincide; revisa el signo.','structure':'Revisa si corresponde a corto o largo plazo y su sección.',
                  'efe':'Distingue operación, inversión y financiamiento.','classification':'Revisa el elemento al que pertenece la cuenta.',
                  'calculation':'Revisa los importes y las operaciones del cálculo.','relationship':'Comprueba la relación entre el resultado y los estados.',
                  'equity':'Separa aportes, utilidad, reservas y dividendos.'}
        feedback.append({'id':key,'label':task['label'],'correct':correct,'error_type':kind,'expected':shown,
            'received':answer,'rule_id':task['rule_id'],'message':messages[kind], 'explanation':rules[task['rule_id']]['text'],'source':rules[task['rule_id']]['source'],'skill':task['skill']})
    correct=sum(f['correct'] for f in feedback)
    return {'correct':correct,'total':len(feedback),'completed':correct==len(feedback),'feedback':feedback}
