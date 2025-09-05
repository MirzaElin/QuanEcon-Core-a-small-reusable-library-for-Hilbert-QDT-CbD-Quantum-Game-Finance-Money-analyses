from quanecon.qfinance import binomial_call

def test_binomial_positive():
    r = binomial_call(100,100,0.01,0.2,1.0,steps=50)
    assert r.ok and r.binomial_price >= 0.0
