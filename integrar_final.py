import pandas as pd

file_path = r'C:\Users\acuba\eudrperu\LISTA_DEFINITIVA_FINAL_AUDITORIA.xlsx'

try:
    # Load sheets specifying engine
    df_final = pd.read_excel(file_path, sheet_name='Lista Definitiva', engine='openpyxl')
    df_174 = pd.read_excel(file_path, sheet_//name='Matriz Hallazgos 174', engine='openpyxl') # Fix a lity
"