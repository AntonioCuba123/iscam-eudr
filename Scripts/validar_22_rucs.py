# -*- coding: utf-8 -*-
import requests, json, time

API = 'http://localhost:4006/api/contribuyentes/'

rucs = ['20132509876','20357021058','20484328162','20486973219','20487107949',
        '20525315607','20525612644','20525955843','20526179367','20568190450',
        '20601710456','20603557825','20603734255','20603820691','20603862369',
        '20604409811','20604876126','20606281804','20607105929','20608057529',
        '20609098989','20609224666']

results = {}
for ruc in rucs:
    try:
        r = requests.get(API + ruc, timeout=10)
        if r.status_code == 200:
            d = r.json()
            results[ruc] = {
                'status': 200,
                'razonSocial': d.get('razonSocial',''),
                'estado': d.get('estadoContribuyente',''),
                'condicion': d.get('condicionDomicilio',''),
                'ubigeo': d.get('ubigeo',''),
                'direccion': d.get('direccion',''),
                'fob_total': 0,  # will fill from SUNAT data
            }
        else:
            results[ruc] = {'status': r.status_code, 'error': r.text[:50]}
    except Exception as e:
        results[ruc] = {'error': str(e)[:80]}
    time.sleep(0.3)

print(json.dumps(results, indent=2, ensure_ascii=False))
