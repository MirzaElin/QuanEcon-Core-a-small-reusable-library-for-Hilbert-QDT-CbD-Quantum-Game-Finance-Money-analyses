from quanecon.qmoney import simulate

def test_qmoney_length():
    r = simulate(T=10)
    assert r.ok and len(r.trajectory["H"]) == 10
