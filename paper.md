---
title: "QuanEcon Core: a small, reusable library for Hilbert/QDT/CbD/Quantum‑Game/Finance/Money analyses"
tags:
  - quantum cognition
  - decision making
  - Python
authors:
  - name: Mirza Niaz Zaman Elin
    ORCID ID: https://orcid.org/0000-0001-9577-7821
    affiliation: 1
affiliations:
  - name: AMAL Youth & Family Centre, St. John's, NL, Canada
    index: 1
date: 2025-09-05
bibliography: paper.bib
---

# Summary

# Summary

QuanEcon Core is a small, reusable Python library—plus a command-line interface—that exposes headless implementations of several compact analyses originally bundled in a GUI: a Hilbert-space fit for conditional probabilities, a Quantum Decision Theory (QDT) utility-plus-attraction model, a Contextuality-by-Default (CbD) check, a lightweight Eisert-style quantum game explorer, a Cox–Ross–Rubinstein binomial option pricer, and a toy monetary sandbox. The package is designed for transparent, reproducible research: it provides an importable API and a simple CLI, includes examples for quick trials, and ships with unit tests and GitHub Actions CI. By separating computation from any user interface and keeping dependencies light, QuanEcon Core enables scripting in notebooks and pipelines, classroom demonstrations, and small research prototypes without coupling to a desktop app.

# Statement of need

Researchers and instructors exploring quantum‑like models often require *scriptable* tools to run small experiments and reproduce figures outside of desktop applications. By shipping the computation as a minimal Python library (NumPy/pandas ecosystem) with examples, tests and CI, these methods can be embedded in notebooks and pipelines.

# Functionality

- Hilbert: given \(p(A)\), \(p(B\mid A)\), and a target \(p(A\mid B)\), search a relative phase \(\varphi\) to match the target under a 2‑dimensional Hilbert model (Born‑rule projection).  
- QDT: compute utility factors via softmax \((\tau)\) and attraction corrections (either alternating \(\pm\tfrac{1}{4}\) or fitted to observed frequencies), producing a normalized choice probability vector.  
- CbD: compute \(S_{\mathrm{odd}}\) over the eight odd‑sign combinations and the inconsistency index \(\mathrm{ICC}=|m_{A1}-m_{A2}|+|m_{B1}-m_{B2}|\); contextuality holds if \(S_{\mathrm{odd}} > 2 + \mathrm{ICC}\).  
- Quantum Game: evaluate the Eisert–Wilkens–Lewenstein scheme for the 3×3 strategy set {C,D,Q}×{C,D,Q} at entanglement \(\gamma\), reporting the profile(s) maximizing \(E_A+E_B\).  
- Finance: price a European call via the Cox–Ross–Rubinstein binomial tree.  
- Money: simulate a small deterministic household/flow sandbox.

# Quality control

Unit tests cover numerical sanity for each module (probability normalization, thresholds, payoff search, positive option price, trajectory length). GitHub Actions runs tests on each push/PR. CSV demos are included for quick trials.

# State of the field

The package is a pragmatic, educational collection rather than a novel contribution. It draws on standard references in quantum cognition [@BusemeyerBruza2012; @YukalovSornette2016], contextuality [@DzhafarovKujala2016], quantum games [@Eisert1999], and option pricing [@CoxRossRubinstein1979], and relies on the scientific Python stack [@Harris2020; @McKinney2010].


# Conflict of interest

The author declares no competing interests.
