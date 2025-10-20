# Documentación de la API SIFEN (README)

Resumen rápido
- Base URL local (ejemplo): http://localhost:8000
- Prefijo actual en la app: `/Api/sifen`
- Transacciones atómicas: todas las inserciones se confirman solo al final; si hay error se realiza rollback.
- El CDC se genera internamente antes del commit usando los datos en memoria.

Endpoints
1) POST /Api/sifen/FE
- Descripción: Crear Factura Electrónica (FE).
- Código de éxito: 200 (respuesta actual), recomendable 201 Created.
- Errores comunes: 400 (validación, campos faltantes), 422 (Pydantic).

Request JSON de ejemplo (mínimo funcional — ajustar según tu schema):
```json
{
  "id_de": "RUC-20251020001",
  "dverfor": 101,
  "timbrado": {
    "itide": 1,
    "dnumtim": "00001234",
    "dest": "001",
    "dpunexp": "001",
    "dnumdoc": "0000001",
    "dfeinit": "2025-10-20"
  },
  "operacion": {
    "itipemi": 1,
    "ddestipemi": "EMISION",
    "dinfoemi": 0
  },
  "emisor": {
    "drucem": "12345678",
    "itipcont": 2,
    "dnomemi": "ACME S.A.",
    "ddiremi": "C/ Falsa 123",
    "dnumcas": "1",
    "cdepemi": 1,
    "ddesdepemi": "Departamento",
    "cciuemi": 1,
    "ddesciuremi": "Ciudad",
    "dtelem": "021234567",
    "demail": "admin@acme.com",
    "actividades": [
      { "cacteco": "471101", "ddesacteco": "Comercio al por mayor" }
    ]
  },
  "items": [
    {
      "dcodint": "ITEM001",
      "ddesproser": "Producto A",
      "cuni_med": "UND",
      "ddesunimed": "Unidad",
      "dcantproser": "1.00",
      "valor_item": {
        "dpuniproser": "1000.00",
        "dtotbruopeitem": "1000.00",
        "valor_resta": { "ddescitem": "0.00", "dtotopeitem": "1000.00" }
      },
      "iva": {
        "iafeciva": 1,
        "ddesafeciva": "Gravado IVA",
        "dpropiva": "100.00",
        "dtasaiva": "10.00",
        "dbasgraviva": "1000.00",
        "dliqivaitem": "100.00"
      }
    }
  ],
  "totales": {
    "dsubexe": "0.00",
    "dtotope": "1000.00",
    "dtotiva": "100.00"
  }
}
```

Response (ejemplo):
```json
{
  "msg": "Factura electrónica creada correctamente",
  "id_de": "RUC-20251020001"
}
```

2) POST /Api/sifen/NC
- Descripción: Crear Nota de Crédito / Débito.
- Cuerpo similar al de FE; incluye campo `nota_credito_debito` con `imotemi` y `ddesmotemi`.

Request JSON mínimo (ejemplo):
```json
{
  "id_de": "RUC-20251020002",
  "dverfor": 101,
  "timbrado": { "itide": 2, "dnumtim": "00005678", "dest": "001", "dpunexp":"001", "dnumdoc":"0000002", "dfeinit":"2025-10-20" },
  "operacion": { "itipemi": 1, "ddestipemi":"EMISION" },
  "emisor": { "drucem":"12345678", "itipcont":2, "dnomemi":"ACME S.A.", "ddiremi":"C/ Falsa 123", "dnumcas":"1", "cdepemi":1, "ddesdepemi":"Departamento", "cciuemi":1, "ddesciuremi":"Ciudad", "dtelem":"021234567", "demail":"admin@acme.com" },
  "items": [ ... ],
  "nota_credito_debito": { "imotemi": 1, "ddesmotemi": "Devolución por error" },
  "totales": { "dsubexe":"0.00", "dtotope":"1000.00", "dtotiva":"100.00" }
}
```

Response:
```json
{
  "msg": "Nota de crédito/débito creada correctamente",
  "id_de": "RUC-20251020002"
}
```

3) POST /Api/sifen/evento/cancelacion
- Descripción: Registrar evento de cancelación de un documento.
- Requiere `cdc_dte` (CDC del documento a cancelar).

Request JSON (ejemplo):
```json
{
  "id_evento": "E0001",
  "cdc_dte": "cdc_abcdef123456",
  "mototeve": "Motivo de cancelación"
}
```

Response:
```json
{
  "msg": "Evento de cancelación registrado correctamente",
  "id_evento": "E0001"
}
```

4) POST /Api/sifen/evento/inutilizacion
- Descripción: Registrar inutilización (rango) o inutilización puntual.
- Campos requeridos: `dtigde` (2), `dnumtim`, `dest`, `dpunexp`, `dnumin`, `dnumfin`, `itide`.

Request JSON (ejemplo):
```json
{
  "id_evento": "E0002",
  "cdc_dte": "cdc_abcdef123456",
  "dtigde": 2,
  "dnumtim": "00001234",
  "dest": "001",
  "dpunexp": "001",
  "dnumin": "000010",
  "dnumfin": "000020",
  "itide": 1,
  "mototeve": "Inutilización por rango"
}
```

Response:
```json
{
  "msg": "Evento de inutilización registrado correctamente",
  "cdc_dte": "00001234001000010000020"
}
```

5) GET /Api/sifen/consulta/{cdc}
- Descripción: Consulta estado de CDC (último estado guardado o simulación).
- Response 200 con estado o 404 si no existe el CDC.

Response ejemplo:
```json
{
  "cdc": "cdc_abcdef123456",
  "dFecProc": "2025-10-20T15:30:00",
  "dCodRes": "0301",
  "dMsgRes": "Documento procesado correctamente (Aprobado)"
}
```

Errores comunes y formato
- Errores de validación (campos faltantes) devuelven 400 con detalle:
```json
{ "detail": "Faltan campos requeridos para inutilización: dnumtim, dest, dpunexp, itide" }
```
- En caso de excepción interna se retorna 400 (actual) con detalle; recomendable cambiar a 500 en errores del servidor.

Notas operativas y recomendaciones (resumidas)
- Validación: enviar los campos exactamente con los nombres definidos en los schemas (ej. `cuni_med`, `id_de`, `timbrado.dnumtim`).
- Transacciones: si una operación falla se hace rollback y no se persiste nada.
- CDC: se arma internamente (antes del commit) usando los datos en memoria; no lo envíes en el payload.
- Recomendado: usar autenticación (API key / JWT), idempotency-key para POSTs y devolver 201 con Location al crear recursos.

Cómo añadir la documentación al proyecto
- Este archivo ya está listo en `c:\Users\mauri\sifen_api\API_DOCUMENTATION.md`.
- Generar OpenAPI/Swagger adicional: FastAPI ya genera `/docs` y `/openapi.json` con los schemas; protege `/docs` en producción o requiere auth.

Fin.