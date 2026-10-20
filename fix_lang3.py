# -*- coding: utf-8 -*-
with open(r'C:\Users\acuba\eudrperu\build_iscam_v3.py', encoding='utf-8') as f:
    content = f.read()

content = content.replace("('IV2', '= D1 (baseline=50 si pendiente)', '20%')",
                          "('IV2', '= D1 (base=50 si pendiente)', '20%')")
content = content.replace("('IV3', '= ha>0? 65 : 35 (fragilidad)', '20%')",
                          "('IV3', '= ha>0? -> 65 : 35 (fragilidad)', '20%')")
content = content.replace("('IV4', '= cert=0? 70 : 30 (brecha)', '20%')",
                          "('IV4', '= cert=0? -> 70 : 30 (brecha)', '20%')")
content = content.replace("('IV5', '= tipo Asoc? 65 : 40 (riesgo social)', '20%')",
                          "('IV5', '= tipo Asoc? -> 65 : 40 (riesgo social)', '20%')")

with open(r'C:\Users\acuba\eudrperu\build_iscam_v3.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
