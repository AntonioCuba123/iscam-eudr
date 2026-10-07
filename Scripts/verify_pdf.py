# -*- coding: utf-8 -*-
pdf = r'C:\Users\acuba\eudrperu\docs\FUNDAMENTOS_UNIVERSO_ENCUESTABLE.pdf'
with open(pdf, 'rb') as f:
    data = f.read()

print('File size:', len(data))
# Search around encuesta region
pos = data.find(b'encuestable')
if pos >= 0:
    snippet = data[pos-20:pos+50]
    try:
        decoded = snippet.decode('utf-8', errors='replace')
    except:
        decoded = repr(snippet)
    print('Context:', repr(snippet))
    print('Decoded:', decoded)

# Check garbage
garbage = b'\xe6\xaf\x8d\xe5\xa5\xb3'
print('Garbage母女:', data.count(garbage))
print('母女 (utf8):', '母女'.encode('utf-8') in data)

# Show first 200 bytes of actual stream
print('First 200 bytes:', data[:200])
