from __future__ import annotations
from typing import List
from collections import defaultdict, Counter
from .dataset import Dataset
from .hilbert import fit_phase
from .qdt import compute as qdt_compute, Prospect
from .cbd import check as cbd_check

def _to_boolish(x: str):
    t = str(x).strip().lower()
    if t in ("yes","y","true","t","1"): return True
    if t in ("no","n","false","f","0"): return False
    return None

def _categorical_values(values: List[str], max_unique=10):
    uniq = list(dict.fromkeys([v.strip() for v in values if v.strip()!=""]))
    if len(uniq)<=max_unique: return uniq
    boolish = [_to_boolish(v) for v in values]
    if all(b is not None for b in boolish): return ["True","False"]
    return None

class AutoRunner:
    def __init__(self, ds: Dataset):
        self.ds = ds

    def run_hilbert_all(self, limit_pairs: int = 200):
        headers = self.ds.headers
        cols = {h: [r[headers.index(h)] if headers.index(h) < len(r) else '' for r in self.ds.rows] for h in headers}
        cats = {h: _categorical_values(cols[h]) for h in headers}
        cat_headers = [h for h in headers if cats.get(h)]
        results_rows = [["A_col","A_yes","B_col","B_yes","N","nA","nB","nAB","pA","pB|A","pA|B","phi","theta"]]
        count=0
        for i in range(len(cat_headers)):
            for j in range(i+1, len(cat_headers)):
                A, B = cat_headers[i], cat_headers[j]
                A_vals = [v for v in cols[A] if v.strip()!=""]; B_vals = [v for v in cols[B] if v.strip()!=""]
                if not A_vals or not B_vals: continue
                A_yes = Counter(A_vals).most_common(1)[0][0]; B_yes = Counter(B_vals).most_common(1)[0][0]
                N = 0; nA = 0; nB = 0; nAB = 0
                for a,b in zip(cols[A], cols[B]):
                    if a.strip()=="" or b.strip()=="": continue
                    N += 1
                    aY = (a==A_yes); bY = (b==B_yes)
                    if aY: nA += 1
                    if bY: nB += 1
                    if aY and bY: nAB += 1
                if N==0 or nA==0 or nB==0: continue
                pA = nA/N; pB_A = nAB/nA; pA_B = nAB/nB
                res = fit_phase(pA, pB_A, pA_B)
                results_rows.append([A, A_yes, B, B_yes, f"{N}", f"{nA}", f"{nB}", f"{nAB}", f"{pA:.4f}", f"{pB_A:.4f}", f"{pA_B:.4f}", f"{res.phi:.4f}", f"{res.theta:.4f}"])
                count+=1
                if count>=limit_pairs: break
            if count>=limit_pairs: break
        if len(results_rows)==1:
            return {"ok": False, "summary": "Hilbert Auto: no suitable categorical column pairs found.", "tables": {}}
        return {"ok": True, "summary": f"Hilbert Auto: analyzed {len(results_rows)-1} column-pairs (one-vs-rest).", "tables": {"hilbert_pairs": results_rows}}

    def run_qdt_all(self):
        hdrs = set(self.ds.headers)
        if not {"prospect","utility"}.issubset(hdrs):
            return {"ok": False, "summary": "QDT Auto: dataset needs 'prospect' and 'utility' columns (optional: 'freq','experiment').", "tables": {}}
        exp_col = "experiment" if "experiment" in hdrs else None
        rows = self.ds.rows; h_index = {h:i for i,h in enumerate(self.ds.headers)}
        buckets = defaultdict(list)
        for r in rows:
            name = r[h_index["prospect"]] if h_index["prospect"]<len(r) else ""
            util = r[h_index["utility"]] if h_index["utility"]<len(r) else ""
            if name.strip()=="" or util.strip()=="": continue
            freq = r[h_index["freq"]] if "freq" in hdrs and h_index["freq"]<len(r) else None
            expv = r[h_index[exp_col]] if exp_col and h_index[exp_col]<len(r) else "default"
            try:
                utilf = float(util); freqf = (float(freq) if freq not in (None,"") else None)
                buckets[expv].append(Prospect(name=name, utility=utilf, freq=freqf))
            except:
                continue
        if not buckets: return {"ok": False, "summary": "QDT Auto: no valid rows parsed.", "tables": {}}
        master = [["experiment","prospect","utility","utility_factor","final_P"]]
        for exp, plist in buckets.items():
            res = qdt_compute(plist)
            if not res.ok: continue
            for i,nm in enumerate(res.names):
                master.append([exp, nm, f"{plist[i].utility:.4f}", f"{res.utility_factor[i]:.4f}", f"{res.probabilities[i]:.4f}"])
        return {"ok": True, "summary": f"QDT Auto: processed {len(buckets)} experiment group(s).", "tables": {"qdt_all": master}}

    def run_cbd_all(self):
        hdrs = set(self.ds.headers)
        req = {"A1","A2","B1","B2"}
        if not req.issubset(hdrs):
            return {"ok": False, "summary": "CbD Auto: needs columns A1,A2,B1,B2 with ±1 values.", "tables": {}}
        idx = {h:i for i,h in enumerate(self.ds.headers)}
        def tofloat(s): 
            try: return float(s)
            except: return 0.0
        A1=[tofloat(r[idx["A1"]]) if idx["A1"]<len(r) else 0.0 for r in self.ds.rows]
        A2=[tofloat(r[idx["A2"]]) if idx["A2"]<len(r) else 0.0 for r in self.ds.rows]
        B1=[tofloat(r[idx["B1"]]) if idx["B1"]<len(r) else 0.0 for r in self.ds.rows]
        B2=[tofloat(r[idx["B2"]]) if idx["B2"]<len(r) else 0.0 for r in self.ds.rows]
        def mean(vs): xs=[x for x in vs if x in (-1.0,1.0)]; return sum(xs)/len(xs) if xs else 0.0
        def mean_prod(a,b): xs=[ai*bi for ai,bi in zip(a,b) if ai in (-1.0,1.0) and bi in (-1.0,1.0)]; return sum(xs)/len(xs) if xs else 0.0
        vals = {"E11": mean_prod(A1,B1), "E12": mean_prod(A1,B2), "E21": mean_prod(A2,B1), "E22": mean_prod(A2,B2), "mA1": mean(A1), "mA2": mean(A2), "mB1": mean(B1), "mB2": mean(B2)}
        r = cbd_check(**vals)
        tbl = [["Metric","Value"], ["S_odd", f"{r.S_odd:.4f}"], ["ICC", f"{r.ICC:.4f}"], ["Threshold", f"{2+r.ICC:.4f}"], ["Contextual?", str(r.contextual)]]
        return {"ok": True, "summary": "CbD Auto: computed S_odd and ICC.", "tables": {"cbd": tbl}}
