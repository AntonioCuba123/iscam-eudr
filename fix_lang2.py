# -*- coding: utf-8 -*-
"""Corrige headers de grupo y elementos mezclados en build_iscam_v3.py"""
with open(r'C:\Users\acuba\eudrperu\build_iscam_v3.py', encoding='utf-8') as f:
    content = f.read()

# Fix: 'AMBIENTALES + PERFORMANCE' -> 'AMBIENTALES + DESEMPEÑO'
content = content.replace("'AMBIENTALES + PERFORMANCE', VERDE_H)", "'AMBIENTALES + DESEMPENO', VERDE_H)")

# Fix: IV2 nota 'baseline=50' -> 'base=50'
content = content.replace("IV2=D1(baseline=50)", "IV2=D1(base=50)")

with open(r'C:\Users\acuba\eudrperu\build_iscam_v3.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - fixes applied")
