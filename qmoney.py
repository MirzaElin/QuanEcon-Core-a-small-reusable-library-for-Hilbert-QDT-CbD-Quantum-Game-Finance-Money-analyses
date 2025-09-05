from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class MoneyResult:
    ok: bool
    trajectory: Dict[str, List[float]]

def simulate(T=40, c0=1.0, c1=0.05, rD=0.01, rL=0.03, inv0=0.5, cash_share=0.5, corr=0.2, H0=100.0, D0=50.0, L0=20.0) -> MoneyResult:
    cash_share=max(0.0,min(1.0,float(cash_share))); corr=max(0.0,min(1.0,float(corr)))
    H=float(H0); D=float(D0); L=float(L0)
    out={k:[] for k in ["H","D","L","C","Y","cash","account"]}
    for t in range(int(T)):
        C=c0+c1*H; Y=C
        Hn=H+Y-C+rD*D-rL*L + corr*(D-L)*0.01
        Dn=D+Y-C
        Ln=max(0.0, L+inv0-(Y-C))
        cash=cash_share*Dn; account=(1-cash_share)*Dn
        H,D,L=Hn,Dn,Ln
        out["H"].append(H); out["D"].append(D); out["L"].append(L); out["C"].append(C); out["Y"].append(Y); out["cash"].append(cash); out["account"].append(account)
    return MoneyResult(True, out)
