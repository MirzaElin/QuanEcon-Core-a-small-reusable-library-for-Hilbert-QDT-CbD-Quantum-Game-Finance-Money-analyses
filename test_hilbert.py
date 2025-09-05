from quanecon.hilbert import fit_phase

def test_hilbert_basic():
    r = fit_phase(0.6, 0.7, 0.65, grid=180)
    assert r.ok and 0.0 <= r.phi <= 6.4 and 0.0 <= r.pA_given_B_est <= 1.0
