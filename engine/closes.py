from .money import ZERO, AccountingError, number, positive, rate


def depreciation(cost, salvage, years, months, *, land=False, accumulated='0'):
    cost, salvage = positive(cost, True), positive(salvage, True)
    accumulated = positive(accumulated, True)
    months = positive(months, True)
    if salvage > cost or accumulated > cost - salvage:
        raise AccountingError('El rescate o la depreciación acumulada exceden la base depreciable.')
    if land:
        return ZERO
    years = positive(years)
    return min((cost - salvage) / years * months / 12, cost - salvage - accumulated)


def amortization(cost, years, months, accumulated='0'):
    return depreciation(cost, '0', years, months, accumulated=accumulated)


def prorate(amount, elapsed, total):
    amount, elapsed, total = positive(amount, True), positive(elapsed, True), positive(total)
    if elapsed > total:
        raise AccountingError('El período consumido supera el plazo contratado.')
    return amount * elapsed / total


def income_tax(profit, tax_rate='0.295'):
    # Política P: pérdidas no generan crédito fiscal automático.
    return max(ZERO, number(profit)) * rate(tax_rate)


def legal_reserve(profit, capital, current='0', reserve_rate='0.10', cap_rate='0.20'):
    room = max(ZERO, positive(capital, True) * rate(cap_rate) - positive(current, True))
    return min(max(ZERO, number(profit)) * rate(reserve_rate), room)


def periodic_cost(initial, purchases, final, freight='0', returns='0', theft='0', theft_policy='separate'):
    if theft_policy not in ('separate', 'cost'):
        raise AccountingError('Indique si el robo se presenta separado o dentro del costo.')
    vals = [positive(v, True) for v in (initial, purchases, final, freight, returns, theft)]
    initial, purchases, final, freight, returns, theft = vals
    result = initial + purchases + freight - returns - final
    if theft_policy == 'separate':
        result -= theft
    if result < 0:
        raise AccountingError('Inventario final y ajustes exceden las existencias disponibles.')
    return result

