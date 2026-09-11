"""Transcribe independent expected cells. Does NOT import or run the engine."""
from pathlib import Path
from decimal import Decimal
import json

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'docs/evidence'
OUT=ROOT/'tests/fixtures'
OUT.mkdir(parents=True,exist_ok=True)

def book(fragment):
    paths=[p for p in EVIDENCE.glob('*.json') if fragment in p.stem]
    assert len(paths)==1,(fragment,paths)
    return json.loads(paths[0].read_text(encoding='utf-8'))

def val(b,s,c):
    v=b['sheets'][s].get(c,{}).get('value')
    return str(v) if v is not None else '0'

def save(id,kind,b,s,data,expected,refs,**meta):
    payload={'id':id,'kind':kind,'source':b['source'],'sha256':b['sha256'],'sheet':s,
        'input':data,'expected':expected,'expected_cells':refs,'tolerance':'0.000001',**meta}
    (OUT/f'{id}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')

def matrix(id,fragment,s,cols,start,end,total,opening_row=None,closing=None,**meta):
    b=book(fragment)
    opening={k:val(b,s,f'{c}{opening_row}') for c,k in cols.items()} if opening_row else {}
    rows=[]
    for r in range(start,end+1):
        deltas={k:val(b,s,f'{c}{r}') for c,k in cols.items() if Decimal(val(b,s,f'{c}{r}'))}
        if not deltas: continue
        rows.append({'label':f'{s}, operación fila {r}','deltas':deltas,'source_row':r})
    refs={k:f'{c}{total}' for c,k in cols.items()}
    save(id,'matrix',b,s,{'opening':opening,'rows':rows,'closing':closing},
         {k:val(b,s,c) for k,c in refs.items()},refs,**meta)

matrix('semana1_caso1','solucionario ejercicio 2','caso 1',dict(zip('BCDEFHIJK',['cash','receivables','inventory','equipment','buildings','salaries_payable','other_payables','capital','retained'])),3,15,16)
matrix('semana1_caso2','solucionario ejercicio 2','caso 2',dict(zip('BCDEFHIJK',['cash','receivables','inventory','equipment','furniture','payables','other_payables','capital','retained'])),3,16,17)
matrix('pd1_ecuacion','PD 1 Solucionario','Ejercicio 2',dict(zip('CDEFGHIJKMNOPRS',['cash','receivables','inventory','intangibles','prepaid_rent','prepaid_insurance','investments_lp','vehicles','equipment','salaries_payable','payables','other_payables','loan_lp','capital','retained'])),3,29,30)
matrix('pd2_esf','PD 2 Solucionario','E2',dict(zip('CDEFGHIJKLMNO',['cash','receivables','investments_cp','inventory','supplier_advance','equipment','dep_equipment','intangibles','amort_intangibles','payables','other_payables','capital','retained'])),3,18,19)
matrix('pc1_p2','PC1 2026-2 Solucionario','Sol_P2',dict(zip('BCDEFGHIJKLNOPQSTU',['cash','investments_cp','receivables','other_receivables','inventory','prepaid_insurance','land','buildings','equipment','dep_buildings','dep_equipment','tax_payable','payables','customer_advance','other_payables','capital','reserve','retained'])),4,20,23,3,{'tax_rate':'0.295','reserve_rate':'0.10'},private=True)
matrix('super_smash','solejercicio 4','ecuacion contable',dict(zip('BCDEFGHIJKLMOPQRST',['cash','receivables','notes_receivable','staff_receivables','inventory','prepaid_rent','prepaid_rent_lp','investments_lp','equipment','dep_equipment','vehicles','dep_vehicles','tax_payable','payables','salaries_payable','capital','reserve','retained'])),3,24,28,closing={'tax_rate':'0.30','reserve_rate':'0.10'},triage='SS-01: tasa histórica 30%, impuesto C4. La cifra UAIR C3 se contrasta contra la matriz.')

b=book('PD 1 Solucionario');s='Ejercicio 1'
class_ids=['receivables','sales','payables','other_receivables','reserve','staff_receivables','equipment','benefits_payable','benefits_expense','dep_equipment','capital','prepaid_rent','customer_advance','rent_expense','loan_lp','marketing','tax_payable','furniture','dep_expense','amort_expense','supplier_advance','service_income','prepaid_insurance','utilities','other_payables','retained','inventory','intangibles','buildings']
answers={}; refs={}
for r,key in enumerate(class_ids,3):
    col=next(c for c in 'CDEFG' if val(b,s,f'{c}{r}')=='X')
    answers[key]={'C':'Activo','D':'Pasivo','E':'Patrimonio Neto','F':'Ingreso','G':'Gasto'}[col];refs[key]=f'{col}{r}'
save('pd1_clasificacion','classification',b,s,{'accounts':class_ids},answers,refs)

b=book('PD 2 Solucionario');s='E1'
for id,row,cost,salvage,years,months in [('edificio',4,'465000','105000','30','69'),('maquinaria',5,'94000','9400','5','29'),('muebles',6,'32000','2000','10','55'),('vehiculo',7,'45000','15000','5','11')]:
    save('pd2_dep_'+id,'depreciation',b,s,dict(cost=cost,salvage=salvage,years=years,months=months),{'amount':val(b,s,f'H{row}')},{'amount':f'H{row}'})

b=book('PC1 2026-2 Solucionario');s='Sol_P1'
save('pc1_p1_close','close',b,s,{'profit_items':['20000','-6000','-2000','-625','-1250'],'capital':'36000'},
     {'tax':str(-Decimal(val(b,s,'L10'))),'reserve':val(b,s,'G20'),'retained':val(b,s,'G21')}, {'tax':'L10','reserve':'G20','retained':'G21'},private=True)

def er(id,fragment,s,balances,refs,**meta):
    b=book(fragment)
    save(id,'er',b,s,{'balances':balances},{k:str(abs(Decimal(val(b,s,c)))) if k in ('tax','cost') else val(b,s,c) for k,c in refs.items()},refs,**meta)
er('pd3_er','PD 3 Solucionario','E1 ER',{'sales':'1000000','sales_returns':'10000','sales_discount':'250','cost':'350000','salary_expense':'36000','utilities':'14400','rent_expense':'150000','dep_expense':'27600','bad_debt':'10150','donation_expense':'5400','asset_gain':'20000','exchange_income':'13500','interest_expense':'5000','interest_income':'3500'}, {'net_sales':'G18','gross_profit':'G20','operating_profit':'G32','profit_before_tax':'G38','tax':'G40','net_profit':'G41'})
er('poder_er','Ejemplo de Estado','Ejemplo de ER',{'sales':'650000','sales_returns':'2000','cost':'320000','insurance_expense':'25000','salary_expense':'28000','utilities':'5000','donation_income':'50000','dep_expense':'3000','interest_expense':'500','interest_income':'2500'}, {'net_sales':'C8','gross_profit':'C10','operating_profit':'C22','profit_before_tax':'C30','tax':'C32','net_profit':'C34'})
er('las_vegas_er','LAs Vegas','pregunta 1',{'sales':'1500000','sales_returns':'85000','sales_discount':'12000','cost':'890000','salary_expense':'85000','utilities':'45000','bad_debt':'1500','rent_expense':'21000','dep_expense':'8458.333333333333333333333333','amort_expense':'5500','theft':'5000','interest_expense':'8900'}, {'net_sales':'C10','cost':'C11','gross_profit':'C12','operating_profit':'C24','profit_before_tax':'C30','tax':'C31','net_profit':'C32'})

def efe(id,fragment,s,groups,initial,refs):
    b=book(fragment);flows=[]
    for activity,cells in groups.items():
        for cell in cells:
            label_col=chr(ord(cell[0])-1)
            flows.append({'label':val(b,s,label_col+cell[1:]),'activity':activity,'amount':val(b,s,cell)})
    save(id,'efe',b,s,{'initial':val(b,s,initial),'flows':flows},{k:val(b,s,c) for k,c in refs.items()},refs)
efe('pd3_efe','PD 3 Solucionario','E3 EFE',{'AO':['B18','B19','B20','B21'],'AI':['B26','B27'],'AF':['B32','B33','B34']},'B39',{'AO':'B22','AI':'B28','AF':'B35','change':'B38','final':'B40'})
efe('pd4_terracan','PD4 26-2 Solución','Pregunta 1- sol',{'AO':['C9','C10','C11','C12','C13'],'AI':['C18'],'AF':['C23','C24','C25']},'C29',{'AO':'C14','AI':'C19','AF':'C26','change':'C28','final':'C30'})
efe('las_vegas_efe','LAs Vegas','pregunta 1',{'AO':[f'C{r}' for r in range(41,49)],'AI':['C52','C53'],'AF':['C57','C58','C59','C60']},'C65',{'AO':'C49','AI':'C54','AF':'C61','change':'C63','final':'C67'})

b=book('PD 3 Solucionario');s='E2 ECPTN'
save('pd3_ecpn','ecpn',b,s,{'opening':{'capital':'300000','reserve':'50000','retained':'200000'},'profit':'70000','contribution':'180000','voluntary':'40000','dividends':'80000'},
     {k:val(b,s,c) for k,c in {'capital':'B30','reserve':'C30','voluntary_reserve':'D30','retained':'E30','total':'F30'}.items()}, {'capital':'B30','reserve':'C30','voluntary_reserve':'D30','retained':'E30','total':'F30'})
b=book('LAs Vegas');s='Pregunta 2'
save('valparaiso_ecpn','ecpn',b,s,{'opening':{'capital':'980000','reserve':'99000','retained':'521000'},'profit':'150000','contribution':'300000','capitalization':'221000','voluntary':'7500','dividends':'75000'},
     {k:val(b,s,c) for k,c in {'capital':'C17','reserve':'D17','voluntary_reserve':'E17','retained':'F17'}.items()}, {'capital':'C17','reserve':'D17','voluntary_reserve':'E17','retained':'F17'})
print(f'{len(list(OUT.glob("*.json")))} fixtures; expected solo desde celdas del corpus.')
