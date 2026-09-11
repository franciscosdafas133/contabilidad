from dataclasses import dataclass, field
from copy import deepcopy
from .catalog import account, accounts, trace
from .money import ZERO, EPSILON, AccountingError, number


def equation_difference(balances):
    catalog = accounts()
    total = ZERO
    for key, value in balances.items():
        if key not in catalog:
            raise AccountingError(f'Cuenta desconocida: {key}')
        sign = 1 if catalog[key]['element'] in ('Activo', 'Gasto') else -1
        total += number(value) * sign
    return total


@dataclass
class Ledger:
    balances: dict = field(default_factory=dict)
    flows: list = field(default_factory=list)
    history: list = field(default_factory=list)
    opening: dict = field(init=False)

    def __post_init__(self):
        self.balances = {k: number(v) for k, v in self.balances.items()}
        self.validate(self.balances)
        if any(account(k)['element'] in ('Ingreso','Gasto') and v for k,v in self.balances.items()):
            raise AccountingError('Los saldos iniciales deben pertenecer al ESF, sin ingresos ni gastos del período anterior.')
        self.opening = deepcopy(self.balances)

    @staticmethod
    def validate(balances):
        if abs(equation_difference(balances)) > EPSILON:
            raise AccountingError('La ecuación no cuadra: Activo + Gasto = Pasivo + Patrimonio + Ingreso.')
        for key, value in balances.items():
            a = account(key)
            if a['contra'] and value > EPSILON:
                raise AccountingError(f'{a["name"]} debe tener signo negativo.')
            if not a['contra'] and key not in ('cash', 'retained') and value < -EPSILON:
                raise AccountingError(f'Saldo insuficiente o signo incorrecto: {a["name"]}.')

    def apply(self, deltas, label, *, cash_activity=None, rule_id='equation'):
        parsed = {k: number(v) for k, v in deltas.items() if number(v) != 0}
        if len(parsed) < 2:
            raise AccountingError('Una operación requiere al menos dos cuentas con movimiento.')
        if abs(equation_difference(parsed)) > EPSILON:
            raise AccountingError('La operación rompe la ecuación contable.')
        cash = parsed.get('cash', ZERO)
        if cash and cash_activity not in ('AO', 'AI', 'AF'):
            raise AccountingError('Todo cobro o pago necesita clasificación AO, AI o AF.')
        if not cash and cash_activity is not None:
            raise AccountingError('Una operación no monetaria no pertenece al EFE.')
        updated = deepcopy(self.balances)
        for key, value in parsed.items():
            updated[key] = updated.get(key, ZERO) + value
        self.validate(updated)
        self.balances = updated
        if cash:
            self.flows.append({'label': label, 'activity': cash_activity, 'amount': cash})
        elements={account(k)['element'] for k in parsed}
        statements=['equation','ESF']
        if elements & {'Ingreso','Gasto'}: statements.append('ER')
        if elements & {'Ingreso','Gasto','Patrimonio Neto'}: statements.append('ECPN')
        if cash: statements.append('EFE')
        item = trace(rule_id, parsed, deepcopy(updated), statements)
        item['label'] = label
        item['deltas'] = parsed
        self.history.append(item)
        return item
