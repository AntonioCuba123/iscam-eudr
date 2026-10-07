# Respaldos — pipeline de DUAs

Copias de seguridad de los libros de trabajo, tomadas antes de cada modificacion
estructural. Los archivos de esta carpeta son el punto de retorno: si una
corrida del pipeline deja algo peor que antes, se restaura el de la fecha
correspondiente.

Los respaldos automaticos que genera el pipeline se quedan en la carpeta
temporal de la sesion (`%TEMP%\kilo\`) y se borran al cerrar. Los de aqui se
copiaron a mano para que sobrevivan.

## Archivos

| Archivo | Que restaura |
|---|---|
| `DUA_CONSOLIDADO_antes_de_atributos_20260930.xlsx` | `fichaduanas\DUA_CONSOLIDADO.xlsx` antes de agregar las 27 columnas de atributos de item y la hoja `PRODUCTORES_ICO` (2026-09-30). |
| `DUA_CONSOLIDADO_con_atributos_20261002.xlsx` | Consolidado con los atributos, 12 hojas y `DETALLE_ITEMS` de 76 columnas. Anterior a la correccion del ICO. |
| `DUA_CONSOLIDADO_antes_series_ico_20261002.xlsx` | El anterior a la correccion de fondo del ICO: antes de separar `serie_ico` de `numero_marca` y antes de las hojas `SERIES_ICO` y `CLAVES_ORIGEN` (2026-10-02). |
| `DUA_CONSOLIDADO_series_ico_20261002.xlsx` | **Punto de retorno del estado actual.** `DETALLE_ITEMS` de 80 columnas, hojas `SERIES_ICO` y `CLAVES_ORIGEN`, `por RUC` de 48 columnas. |
| `MINAGRI_antes_de_bloque_CA_DT_20261001.xlsx` | El directorio de MINAGRI antes de que el bloque de DUAs pasara de CA:DE a CA:DT con las columnas de atributos (2026-10-01). |
| `MINAGRI_antes_de_este_trabajo_20261001.xlsx` | El directorio de MINAGRI antes de la sesion del 2026-10-01 que extrajo los atributos de las descripciones. |
| `MINAGRI_antes_series_ico_20261002.xlsx` | El directorio antes de propagar `serie_ico`, `numero_marca`, `clave_origen` y las columnas de conteo asociadas (2026-10-02). |
| `MINAGRI_series_ico_20261002.xlsx` | **Punto de retorno del estado actual** del directorio: bloque CA:DV con 48 columnas. |

## Como restaurar

Cerrar Excel antes de copiar: si el libro esta abierto, Windows no lo libera y
la copia queda corrupta.

```
Copy-Item "C:\Users\acuba\eudrperu\respaldos\duas\DUA_CONSOLIDADO_antes_de_atributos_20260930.xlsx" `
          "C:\Users\acuba\eudrperu\fichaduanas\DUA_CONSOLIDADO.xlsx" -Force
```

El mismo procedimiento con la ruta del directorio de MINAGRI para los otros
dos.

## Nota sobre nombres

Los respaldos que genera el pipeline llevan marca de tiempo
(`minagri_backup_AAAAMMDD_HHMMSS.xlsx`). Los de esta carpeta tienen nombre
descriptivo a proposito, para que se sepa cual restaura cada uno sin abrirlo.
