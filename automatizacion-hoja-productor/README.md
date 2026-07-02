# Bloqueo de pestañas + "Cerebro" de Claude para la HOJA DEL PRODUCTOR 2026

Esta carpeta contiene todo lo necesario para dos cosas que pediste sobre el
archivo que te compartió Green Gusto (`sourcing@greengusto.com.mx`):

1. **Restringir pestañas por persona** (que solo quien tú autorices pueda ver o
   editar ciertas pestañas).
2. Un **"cerebro" con Claude** que lee los datos de una pestaña, los analiza y
   escribe la respuesta en otra pestaña, de forma automática.

> **Importante sobre el archivo:** lo que te llegó no es un `.xlsx` de Excel,
> es una **Hoja de cálculo de Google (Google Sheets)** y te invitaron como
> **editor**, no como propietario. El dueño es Green Gusto, una organización
> externa. Esto cambia lo que es posible hacer (ver más abajo).

---

## Parte 1 — Restringir/bloquear pestañas por persona

### La verdad técnica (léela antes de empezar)

En un **único** archivo (sea Google Sheets o Excel) hay una diferencia clave:

| Lo que quieres | ¿Se puede en un solo archivo? |
|---|---|
| Que solo ciertas personas **editen** una pestaña (los demás solo la ven) | ✅ **Sí** |
| Que ciertas personas **ni siquiera vean** una pestaña | ❌ **No de forma segura** |

Motivo: la protección de hojas controla **quién edita**, no **quién ve**.
Cualquiera con acceso al archivo puede abrir todas las pestañas. "Ocultar" una
pestaña no es seguridad: cualquier editor puede volver a mostrarla.

Por eso hay **dos caminos**, según lo que de verdad necesites:

---

### Camino A — Todos ven todo, pero cada quien solo edita SU pestaña

Es lo más rápido y lo que la mayoría necesita. Pasos en Google Sheets:

1. Abre la pestaña que quieres proteger.
2. Menú **Datos → Proteger hojas y rangos**.
3. Clic en **Añadir una hoja o rango → pestaña "Hoja"** y elige la pestaña.
4. Clic en **Establecer permisos**.
5. Elige **"Restringir quién puede editar este rango"** y añade únicamente los
   correos de las personas autorizadas para esa pestaña.
6. Repite por cada pestaña con su lista de personas.

Resultado: todos ven todas las pestañas, pero solo los autorizados pueden
modificar cada una. El resto recibe un aviso de "no tienes permiso para editar".

> Como a ti te invitaron solo como **editor**, puedes crear estas protecciones,
> pero el **propietario (Green Gusto) siempre puede quitarlas u omitirlas**. Si
> esto es un control serio, pídeles a ellos que te hagan **propietario** o que
> apliquen ellos las protecciones.

---

### Camino B — Que cada persona SOLO PUEDA VER su pestaña (aislamiento real)

Si de verdad necesitas que alguien **no vea** las demás pestañas, no se puede en
un solo archivo. Se hace con arquitectura de **archivo maestro + archivos por
persona**:

1. **Archivo MAESTRO** (privado, solo tú): tiene todas las pestañas y los datos.
2. Por cada persona/grupo creas un **archivo aparte** que le compartes solo a esa
   persona.
3. En cada archivo por persona usas la función `IMPORTRANGE` para "traer" solo la
   pestaña que esa persona sí puede ver:

   ```
   =IMPORTRANGE("URL_DEL_ARCHIVO_MAESTRO", "NombreDePestaña!A1:Z1000")
   ```

4. Compartes cada archivo individual **solo con su dueño** (como lector o editor).

Así, cada persona abre su propio archivo y físicamente no tiene acceso a los
demás datos. Es más trabajo de mantener, pero es el **único** aislamiento real
de visualización.

> Equivalente en Excel real (`.xlsx`): Revisar → Proteger hoja (con contraseña) y
> "Permitir que los usuarios modifiquen rangos" por usuario. Igual que arriba,
> **proteger ≠ ocultar de la vista**: para aislar la visualización necesitas
> archivos separados por persona.

### ¿Qué te recomiendo?

- Si solo quieres orden y evitar que se pisen ediciones → **Camino A**.
- Si hay datos confidenciales que cierta gente NO debe ver → **Camino B**.

---

## Parte 2 — El "cerebro" de Claude (análisis automático de una pestaña a otra)

El archivo [`Codigo.gs`](./Codigo.gs) es un **Google Apps Script** que:

- Lee los datos de una pestaña de origen (por defecto **"Datos"**).
- Los envía a **Claude** (API de Anthropic).
- Escribe el análisis/respuesta en otra pestaña (por defecto **"Análisis"**).
- Puede correr **manualmente** (con un botón de menú) o **automáticamente** cada
  vez que se edita la pestaña de origen.

### Requisitos

- Una **API key de Anthropic** (se obtiene en <https://console.anthropic.com> →
  *API Keys*). Esto tiene un costo por uso según el modelo; empieza barato con
  `claude-haiku-4-5-20251001`.
- Poder abrir el editor de Apps Script del archivo (**Extensiones → Apps
  Script**). Como el archivo es de Green Gusto, quizá te convenga primero hacer
  una **copia tuya** (*Archivo → Hacer una copia*) y montar el cerebro ahí, o
  pedirles a ellos permiso para instalar el script.

### Instalación (paso a paso)

1. Abre la hoja de Google Sheets donde quieres el cerebro.
2. Menú **Extensiones → Apps Script**.
3. Borra el contenido de ejemplo y **pega todo** el contenido de `Codigo.gs`.
4. Guarda (💾) y ponle nombre al proyecto.
5. Recarga la hoja de cálculo. Aparecerá un nuevo menú **🤖 Claude**.
6. Menú **🤖 Claude → Configurar API key**, pega tu key (`sk-ant-...`) y acepta.
   - La key se guarda cifrada en las *Script Properties*, **nunca** en el código.
7. Ajusta los nombres de las pestañas si los tuyos son distintos: en `Codigo.gs`,
   edita `PESTANA_ORIGEN` y `PESTANA_DESTINO` en el bloque `CONFIG`.
8. La primera vez que ejecutes, Google pedirá **autorizar** los permisos del
   script (leer la hoja y hacer la llamada a la API). Acepta.

### Uso

- **Manual:** menú **🤖 Claude → Analizar datos ahora**. Lee "Datos", llama a
  Claude y escribe el resultado en "Análisis".
- **Automático:** menú **🤖 Claude → Activar análisis automático (al editar)**.
  A partir de ahí, cada edición en la pestaña de origen dispara el análisis.
  Para apagarlo: **Desactivar análisis automático**.

### Personalizar QUÉ analiza

En `Codigo.gs`, dentro de `CONFIG.INSTRUCCION`, está el "cerebro" con lenguaje
natural. Cambia ese texto para pedir lo que necesites (por ejemplo: "clasifica
cada productor por riesgo", "calcula totales por zona", "detecta datos faltantes
y genera un correo de seguimiento", etc.).

### Notas de costo y límites

- Cada análisis consume tokens (se cobra por uso). `MAX_FILAS` limita cuántas
  filas se envían para controlar el gasto; ajústalo a tu tamaño real.
- El modo automático se dispara con **cada** edición; si editas mucho, considera
  usar solo el modo manual o un disparador por tiempo.

---

## Lo que NO se puede hacer "solo con Claude" dentro del archivo

Para ser claro y no venderte humo:

- Claude **no vive dentro** de Excel/Sheets reaccionando por su cuenta. La
  automatización real requiere el puente de arriba (Apps Script + API key).
- La API key la tienes que poner **tú**: por seguridad no puede quedar dentro
  del documento compartido con terceros.
- El bloqueo de **visualización** por persona requiere archivos separados
  (Camino B); en un solo archivo solo se puede bloquear la **edición**.

Cualquier ajuste (nombres de pestañas, el prompt, aislar visualización) me lo
dices y lo dejamos afinado.
