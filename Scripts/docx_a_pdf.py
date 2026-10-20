# -*- coding: utf-8 -*-
"""Convierte el DOCX a PDF usando COM automation de Microsoft Word."""
import os
import sys
import time

DOCX_PATH = r"C:\Users\acuba\ISCAM_UU_Peru_EUDR_Dossier_v3.docx"
PDF_PATH   = r"C:\Users\acuba\ISCAM_UU_Peru_EUDR_Dossier_v3.pdf"

def word_to_pdf(docx_path, pdf_path):
    import win32com.client
    import pythoncom

    pythoncom.CoInitialize()

    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0  # wdAlertsNone

        abs_docx = os.path.abspath(docx_path)
        abs_pdf   = os.path.abspath(pdf_path)

        doc = word.Documents.Open(abs_docx, ConfirmConversions=False, ReadOnly=True)
        doc.SaveAs(abs_pdf, FileFormat=17)  # 17 = wdFormatPDF
        doc.Close(SaveChanges=False)
        word.Quit()

        print(f"PDF guardado: {pdf_path}")
        return True

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

    finally:
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    word_to_pdf(DOCX_PATH, PDF_PATH)
