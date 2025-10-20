Perfecto.
Te dejo tu **documentación completamente actualizada** con los **nombres amigables (alias PascalCase)** y todos los campos coherentes con tus nuevos `schemas`.
Está lista para guardar directamente como `API_DOCUMENTATION.md`.

---

# 📘 Documentación de la API SIFEN

### ⚙️ Resumen rápido

* **Base URL local:** `http://localhost:8000`
* **Prefijo:** `/Api/sifen`
* **Transacciones:** atómicas — si hay error, se hace rollback completo.
* **CDC:** se genera internamente antes del commit con los datos de la factura.

---

## 🔹 Endpoints principales

---

### **1️⃣ POST /Api/sifen/FE**

**Descripción:**
Crear una **Factura Electrónica (FE)**.

**Código de éxito:** `201 Created` (recomendado)
**Errores comunes:**

* `400`: validación o datos faltantes.
* `422`: error de tipo Pydantic.

---

#### 🧾 Request JSON (ejemplo funcional)

```json
{
  "IdDE": "RUC-20251020001",
  "VersionFormato": 101,
  "Operacion": {
    "TipoEmision": 1,
    "DescriTipoEmision": "EMISION",
    "CodigoSeguridad": "123456789",
    "InfoEmisor": "Generación normal"
  },
  "Timbrado": {
    "TipoDocumento": 1,
    "DescriTipoDocumento": "Factura Electrónica",
    "NumeroTimbrado": "00001234",
    "Establecimiento": "001",
    "PuntoExpedicion": "001",
    "NumeroDocumento": "0000001",
    "SerieNumero": "A1",
    "FechaInicioVigencia": "2025-10-20"
  },
  "Emisor": {
    "RucEmisor": "12345678",
    "TipoContribuyente": 2,
    "TipoRegimen": 1,
    "RazonSocial": "ACME S.A.",
    "NombreFantasia": "ACME Store",
    "Direccion": "Calle Falsa 123",
    "NumeroCasa": "1",
    "ComplementoDir1": "Zona Centro",
    "CodigoDepartamento": 1,
    "DescriDepartamento": "Central",
    "CodigoCiudadEmision": 1,
    "DescriCiudadEmision": "Asunción",
    "TelefonoEmisor": "021234567",
    "EmailEmisor": "admin@acme.com",
    "Actividades": [
      { "CodigoActividad": "471101", "DescripcionActividad": "Comercio al por mayor" }
    ]
  },
  "Receptor": {
    "NaturalezaReceptor": 1,
    "TipoOperacion": 1,
    "CodigoPais": "PRY",
    "DescripcionPais": "Paraguay",
    "NombreReceptor": "Cliente Ejemplo",
    "DireccionReceptor": "Av. Siempre Viva 742",
    "TelefonoReceptor": "0981000000",
    "CodigoCliente": "CLI001"
  },
  "Items": [
    {
      "CodigoInterno": "ITEM001",
      "DescripcionProductoServicio": "Producto A",
      "CodigoUnidadMedida": "UND",
      "DescripcionUnidadMedida": "Unidad",
      "CantidadProductoServicio": 1.00,
      "InformacionItem": "Producto genérico",
      "ValorItem": {
        "PrecioUnitario": 1000.00,
        "TotalBrutoOperacionItem": 1000.00,
        "ValorResta": {
          "DescuentoItem": 0.00,
          "PorcentajeDescuentoItem": 0.00,
          "DescuentoGlobalItem": 0.00,
          "TotalOperacionItem": 1000.00
        }
      },
      "IVA": {
        "AfectacionIVA": 1,
        "DescriAfectacionIVA": "Gravado IVA",
        "ProporcionIVA": 100.00,
        "TasaIVA": 10.00,
        "BaseGravadaIVA": 1000.00,
        "LiquidoIVAItem": 100.00
      }
    }
  ],
  "Totales": {
    "SubExentas": 0.00,
    "SubExoneradas": 0.00,
    "Sub5": 0.00,
    "Sub10": 1000.00,
    "TotalOperacion": 1000.00,
    "TotalIVA": 100.00,
    "TotalGralOperacion": 1100.00
  },
  "OperacionComercial": {
    "TipoTransaccion": 1,
    "DescriTipoTransaccion": "Contado",
    "TipoImpuesto": 1,
    "DescriTipoImpuesto": "IVA",
    "MonedaOperacion": "PYG",
    "DescriMonedaOperacion": "Guaraníes"
  }
}
```

#### ✅ Response

```json
{
  "msg": "Factura electrónica creada correctamente",
  "IdDE": "RUC-20251020001"
}
```

---

### **2️⃣ POST /Api/sifen/NC**

**Descripción:**
Crear una **Nota de Crédito o Débito Electrónica**.

#### 🧾 Request JSON (ejemplo mínimo)

```json
{
  "IdDE": "RUC-20251020002",
  "VersionFormato": 101,
  "Operacion": {
    "TipoEmision": 1,
    "DescriTipoEmision": "EMISION"
  },
  "Timbrado": {
    "TipoDocumento": 2,
    "DescriTipoDocumento": "Nota de Crédito",
    "NumeroTimbrado": "00005678",
    "Establecimiento": "001",
    "PuntoExpedicion": "001",
    "NumeroDocumento": "0000002",
    "FechaInicioVigencia": "2025-10-20"
  },
  "Emisor": {
    "RucEmisor": "12345678",
    "TipoContribuyente": 2,
    "RazonSocial": "ACME S.A.",
    "Direccion": "C/ Falsa 123",
    "NumeroCasa": "1",
    "CodigoDepartamento": 1,
    "DescriDepartamento": "Central",
    "CodigoCiudadEmision": 1,
    "DescriCiudadEmision": "Asunción",
    "TelefonoEmisor": "021234567",
    "EmailEmisor": "admin@acme.com"
  },
  "Items": [
    {
      "CodigoInterno": "ITEM002",
      "DescripcionProductoServicio": "Producto Devuelto",
      "CodigoUnidadMedida": "UND",
      "DescripcionUnidadMedida": "Unidad",
      "CantidadProductoServicio": 1.00,
      "ValorItem": {
        "PrecioUnitario": 1000.00,
        "TotalBrutoOperacionItem": 1000.00,
        "ValorResta": { "DescuentoItem": 0.00, "TotalOperacionItem": 1000.00 }
      },
      "IVA": {
        "AfectacionIVA": 1,
        "DescriAfectacionIVA": "Gravado IVA",
        "ProporcionIVA": 100.00,
        "TasaIVA": 10.00,
        "BaseGravadaIVA": 1000.00,
        "LiquidoIVAItem": 100.00
      }
    }
  ],
  "NotaCreditoDebito": {
    "MotivoEmision": 1,
    "DescriMotivoEmision": "Devolución por error"
  },
  "Totales": {
    "SubExentas": 0.00,
    "Sub10": 1000.00,
    "TotalOperacion": 1000.00,
    "TotalIVA": 100.00,
    "TotalGralOperacion": 1100.00
  }
}
```

#### ✅ Response

```json
{
  "msg": "Nota de crédito/débito creada correctamente",
  "IdDE": "RUC-20251020002"
}
```

---

### **3️⃣ POST /Api/sifen/evento/cancelacion**

**Descripción:** Registrar **evento de cancelación** de un documento.

#### 🧾 Request JSON

```json
{
  "IdEvento": "E0001",
  "CodigoDeControl": "CDC_abcdef123456789",
  "MotivoEvento": "Cancelación por error de carga"
}
```

#### ✅ Response

```json
{
  "msg": "Evento de cancelación registrado correctamente",
  "IdEvento": "E0001"
}
```

---

### **4️⃣ POST /Api/sifen/evento/inutilizacion**

**Descripción:** Registrar **inutilización de rango o puntual**.

#### 🧾 Request JSON

```json
{
  "IdEvento": "E0002",
  "NumeroTimbrado": "00001234",
  "Establecimiento": "001",
  "PuntoExpedicion": "001",
  "NumeroInicio": "000010",
  "NumeroFin": "000020",
  "TipoDocumento": 1,
  "MotivoEvento": "Inutilización por rango"
}
```

#### ✅ Response

```json
{
  "msg": "Evento de inutilización registrado correctamente",
  "IdEvento": "E0002"
}
```

---

### **5️⃣ GET /Api/sifen/consulta/{cdc}**

**Descripción:**
Consultar el **estado del documento electrónico** (CDC).

#### ✅ Response ejemplo

```json
{
  "CDC": "cdc_abcdef123456",
  "FechaProcesamiento": "2025-10-20T15:30:00",
  "CodigoResultado": "0301",
  "MensajeResultado": "Documento procesado correctamente (Aprobado)"
}
```

---

## ⚠️ Errores comunes

#### ❌ Validación

```json
{ "detail": "Faltan campos requeridos para inutilización: NumeroTimbrado, Establecimiento, PuntoExpedicion, TipoDocumento" }
```

#### ⚙️ Error interno (rollback)

```json
{ "detail": "Error al insertar datos, operación revertida" }
```

---

## 🧩 Notas operativas

* **Validación:** enviar los campos con sus alias (`CodigoInterno`, `TipoEmision`, etc.).
* **Transacciones:** si un insert falla, se hace rollback automático.
* **CDC:** lo genera internamente el backend; no se envía en el JSON.
* **Recomendado:**

  * Usar autenticación (API key o JWT).
  * Devolver `201 Created` con encabezado `Location`.
  * Implementar `idempotency-key` en los POST.

---

## 🧠 Documentación técnica

FastAPI genera automáticamente:

* Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)
* OpenAPI JSON → [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

> ⚠️ En producción: proteger `/docs` o requerir autenticación.

---

¿Querés que te agregue una sección final con **estructura de carpetas del proyecto** (para documentar `main.py`, `routers/`, `schemas/`, `models/`, etc.)?
Eso sirve si vas a entregar esto como documentación técnica formal o a compañeros.

