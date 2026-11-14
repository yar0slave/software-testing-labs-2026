import pytest
from calculator import Calculator
@pytest.fixture
def calc():
    return Calculator()
@pytest.mark.parametrize('a,b,expected', [(2,3,5),(-2,-3,-5),(-2,3,1),(0,0,0),(0.1,0.2,0.3)])
def test_add(calc, a, b, expected):
    assert calc.add(a,b) == pytest.approx(expected)
@pytest.mark.parametrize('a,b,expected', [(8,2,4),(-9,3,-3),(0,5,0),(1,3,1/3),(7,-2,-3.5)])
def test_divide(calc, a, b, expected):
    assert calc.divide(a,b) == pytest.approx(expected)
@pytest.mark.parametrize('zero', [0, 0.0, -0.0])
def test_division_by_zero(calc, zero):
    with pytest.raises(ZeroDivisionError, match='Division by zero'):
        calc.divide(1,zero)
@pytest.mark.parametrize('n,expected', [(-5,False),(0,False),(1,False),(2,True),(3,True),(4,False),(9,False),(25,False),(97,True),(121,False)])
def test_prime(calc, n, expected):
    assert calc.is_prime_number(n) is expected
@pytest.mark.parametrize('method', ['add','divide'])
@pytest.mark.parametrize('bad', ['2', None, True])
def test_invalid_numeric_type(calc, method, bad):
    with pytest.raises(TypeError):
        getattr(calc,method)(bad,2)
@pytest.mark.parametrize('method', ['add','divide'])
@pytest.mark.parametrize('bad', [float('nan'),float('inf')])
def test_nonfinite(calc, method, bad):
    with pytest.raises(ValueError):
        getattr(calc,method)(1,bad)
@pytest.mark.parametrize('bad', [2.5,'3',True,None])
def test_prime_invalid_type(calc, bad):
    with pytest.raises(TypeError):
        calc.is_prime_number(bad)
