from quanecon.qdt import compute, Prospect

def test_qdt_probs_sum():
    ps = [Prospect("A",0.1,0.35), Prospect("B",0.25,0.45), Prospect("C",0.15,0.20)]
    r = compute(ps, tau=1.0, quarter=0.25)
    assert r.ok and abs(sum(r.probabilities)-1.0) < 1e-8 and len(r.names)==3
