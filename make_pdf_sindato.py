# -*- coding: utf-8 -*-
import win32com.client as wc
import os, time

DOC = r"C:\Users\acuba\eudrperu\ISCAM\Metodologia - Instrumento 2 e Indice ISCAM.docx"
PDF = r"C:\Users\acuba\eudrperu\ISCAM\Metodologia - Instrumento 2 e Indice ISCAM.pdf"
if os.path.exists(PDF):
    os.remove(PDF)

app = wc.DispatchEx("Word.Application")
app.Visible = False
doc = app.Documents.Open(DOC, ReadOnly=True)
print("paginas:", doc.ComputeStatistics(2), "| tablas:", doc.Tables.Count)
# OptimizeFor=1 (pantalla), CreateBookmarks=1, BitmapMissingFonts=False
doc.ExportAsFixedFormat(
    OutputFileName=PDF, ExportFormat=17, OpenAfterExport=False,
    OptimizeFor=1, CreateBookmarks=1, DocStructureTags=True, BitmapMissingFonts=False)
doc.Close(SaveChanges=0)
app.Quit()
time.sleep(1)
print("PDF:", os.path.exists(PDF), os.path.getsize(PDF), "bytes")
