from decimal import Decimal, InvalidOperation, localcontext, ROUND_HALF_UP

ZERO = Decimal('0')
EPSILON = Decimal('0.000000000000000001')


class AccountingError(ValueError):
    pass


def number(value):
    if isinstance(value, (bool, float)):
        raise AccountingError('Use importes decimales como texto, sin coma de miles.')
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise AccountingError('Importe decimal inválido.') from None
    if not result.is_finite() or abs(result) > Decimal('1e15') or result.as_tuple().exponent < -28:
        raise AccountingError('Importe fuera de rango o no finito.')
    return result


def positive(value, allow_zero=False):
    result = number(value)
    if result < 0 or (not allow_zero and result == 0):
        raise AccountingError('El importe debe ser positivo.')
    return result


def rate(value):
    result = number(value)
    if not 0 <= result <= 1:
        raise AccountingError('La tasa debe estar entre 0 y 1.')
    return result


def display(value):
    with localcontext() as ctx:
        ctx.prec = 50
        return str(number(value).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))


def serialize(value):
    if isinstance(value, Decimal):
        return display(value)
    if isinstance(value, dict):
        return {k: serialize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(v) for v in value]
    return value

