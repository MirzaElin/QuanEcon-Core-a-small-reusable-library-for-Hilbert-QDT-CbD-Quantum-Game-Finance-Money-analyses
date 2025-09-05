from quanecon.qgame import solve

def test_qgame_runs():
    r = solve(R=3,S=0,T=5,P=1,gamma=0.6)
    assert r.ok and len(r.best_profiles) >= 1 and r.best_value == max(sum(v) for v in r.payoffs.values())
