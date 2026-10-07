import pandas as pd

D = r"C:/Users/acuba/eudrperu/ficharucsunat/ppaconsultamultiple/"
PPA_TXT = r"C:/Users/acuba/eudrperu/ficharucsunat/ruc-padron-ppa.txt"

master = set()
for src in ("rucs_lote_01.txt", "rucs_lote_02.txt"):
    with open(D + src, encoding="utf-8") as fh:
        for ln in fh:
            r = ln.strip().rstrip("|").strip()
            if r:
                master.add(r)

ppa = pd.read_csv(PPA_TXT, sep="|", dtype=str)
ppa_rucs = set(ppa["ruc"].str.strip())
inter = sorted(master & ppa_rucs)

print("master:", len(master))
print("ppa_registered:", len(ppa_rucs))
print("master IN ppa (interno):", len(inter))
print("rucs en PPA internos:", inter[:25])
