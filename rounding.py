
import math

def _round(value, digits, funk):
    mul = 10 ** digits
    rounded = funk(value * mul) / mul
    return rounded

def roundUp(value, digits):
    return _round(value, digits, math.ceil)

def roundDown(value, digits):
    return _round(value, digits, math.floor)
