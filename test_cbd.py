from quanecon.cbd import check

def test_cbd_threshold():
    r = check(0.7,0.6,0.6,0.7, 0.2,0.1,0.05,0.02)
    assert r.ok and isinstance(r.S_odd, float) and isinstance(r.ICC, float)
