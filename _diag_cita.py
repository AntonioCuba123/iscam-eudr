# -*- coding: utf-8 -*-
import sys
print('inicio', flush=True)
import fix_idioma as fi
print('import ok', flush=True)

a = 'EUDR preparaci\u00f3n assessment'
line = open('Instrumentos/DOC_TRABAJO_Instrumento2_ISCAM_v2.md', encoding='utf-8').read()
j = line.find('preparaci\u00f3n assessment')
print('idx en file:', j, flush=True)
if j >= 0:
    frag = line[j - 12:j + 24]
    print('frag :', repr(frag), flush=True)
    print('esc  :', frag.encode('unicode_escape'), flush=True)
    print('a in frag :', a in frag, flush=True)
    print('norm :', repr(fi.normaliza(frag)), flush=True)
    for m in fi.PROT_RE.finditer(frag):
        print('PROT :', repr(m.group(0)), flush=True)
