from __future__ import annotations
import argparse, json
from .hilbert import fit_phase
from .qdt import compute as qdt_compute, Prospect
from .cbd import check as cbd_check
from .qgame import solve as qgame_solve
from .qfinance import binomial_call
from .qmoney import simulate as money_sim
from .dataset import Dataset
from .auto import AutoRunner

def _load_json_value(arg):
    try:
        if arg and arg.strip().startswith('@'):  # @file.json
            path = arg.strip()[1:]
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return json.loads(arg)
    except Exception:
        return None

def main(argv=None):
    p = argparse.ArgumentParser(prog="quanecon", description="QuanEcon Core CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("hilbert")
    sp.add_argument("--pA", type=float, required=True)
    sp.add_argument("--pB_given_A", type=float, required=True)
    sp.add_argument("--pA_given_B", type=float, required=True)

    sp = sub.add_parser("qdt")
    sp.add_argument("--prospects", required=True, help="JSON array or @file.json [{name, utility, freq?}, ...]")
    sp.add_argument("--tau", type=float, default=1.0)
    sp.add_argument("--quarter", type=float, default=0.25)

    sp = sub.add_parser("cbd")
    for k in ["E11","E21","E22","E12","mA1","mA2","mB1","mB2"]:
        sp.add_argument(f"--{k}", type=float, required=True)

    sp = sub.add_parser("qgame")
    sp.add_argument("--R", type=float, default=3)
    sp.add_argument("--S", type=float, default=0)
    sp.add_argument("--T", type=float, default=5)
    sp.add_argument("--P", type=float, default=1)
    sp.add_argument("--gamma", type=float, default=0.6)

    sp = sub.add_parser("qfinance")
    sp.add_argument("--S0", type=float, required=True)
    sp.add_argument("--K", type=float, required=True)
    sp.add_argument("--r", type=float, required=True)
    sp.add_argument("--sigma", type=float, required=True)
    sp.add_argument("--T", type=float, required=True)
    sp.add_argument("--steps", type=int, default=150)

    sp = sub.add_parser("qmoney")
    for k,d in [("T",40),("c0",1.0),("c1",0.05),("rD",0.01),("rL",0.03),("inv0",0.5),("cash_share",0.5),("corr",0.2),("H0",100.0),("D0",50.0),("L0",20.0)]:
        sp.add_argument(f"--{k}", type=float, default=d)

    sp = sub.add_parser("auto")
    sp.add_argument("data_path", help="CSV or XLSX dataset")

    args = p.parse_args(argv)

    if args.cmd == "hilbert":
        res = fit_phase(args.pA, args.pB_given_A, args.pA_given_B)
        print(json.dumps({"phi":res.phi, "theta":res.theta, "pA|B_est":res.pA_given_B_est}, indent=2)); return

    if args.cmd == "qdt":
        arr = _load_json_value(args.prospects)
        if not isinstance(arr, list):
            raise SystemExit("qdt --prospects expects a JSON list or @file.json")
        plist = [Prospect(name=str(d.get("name","")), utility=float(d.get("utility",0.0)), freq=(float(d["freq"]) if "freq" in d and d["freq"] is not None else None)) for d in arr]
        res = qdt_compute(plist, tau=args.tau, quarter=args.quarter)
        print(json.dumps({"names":res.names,"utility_factor":res.utility_factor,"probabilities":res.probabilities}, indent=2)); return

    if args.cmd == "cbd":
        res = cbd_check(args.E11,args.E21,args.E22,args.E12,args.mA1,args.mA2,args.mB1,args.mB2)
        print(json.dumps({"S_odd":res.S_odd,"ICC":res.ICC,"contextual":res.contextual}, indent=2)); return

    if args.cmd == "qgame":
        res = qgame_solve(args.R,args.S,args.T,args.P,args.gamma)
        out = {"best_value": res.best_value, "best_profiles": [(a,b,EA,EB) for a,b,EA,EB in res.best_profiles]}
        print(json.dumps(out, indent=2)); return

    if args.cmd == "qfinance":
        res = binomial_call(args.S0,args.K,args.r,args.sigma,args.T,args.steps)
        print(json.dumps({"binomial_price": res.binomial_price}, indent=2)); return

    if args.cmd == "qmoney":
        res = money_sim(args.T,args.c0,args.c1,args.rD,args.rL,args.inv0,args.cash_share,args.corr,args.H0,args.D0,args.L0)
        print(json.dumps(res.trajectory, indent=2)); return

    if args.cmd == "auto":
        ds = Dataset.from_xlsx(args.data_path) if args.data_path.lower().endswith(".xlsx") else Dataset.from_csv(args.data_path)
        auto = AutoRunner(ds)
        parts = []
        for fn in [auto.run_hilbert_all, auto.run_qdt_all, auto.run_cbd_all]:
            try:
                parts.append(fn())
            except Exception as e:
                parts.append({"ok": False, "summary": f"Error: {e}", "tables": {}})
        print(json.dumps({"runs": parts}, indent=2)); return
