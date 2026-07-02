/**
 * ============================================================================
 *  CEREBRO DE CLAUDE PARA GOOGLE SHEETS  ("HOJA DEL PRODUCTOR 2026")
 * ============================================================================
 *
 *  Qué hace:
 *   - Lee los datos de una pestaña de origen (por defecto "Datos").
 *   - Los envía al modelo de Claude (API de Anthropic) con una instrucción.
 *   - Escribe la respuesta/análisis en una pestaña de destino (por defecto
 *     "Análisis"), de forma automática.
 *
 *  Cómo instalarlo: ver README.md (Extensiones > Apps Script, pegar este
 *  archivo, guardar la API key con el menú "🤖 Claude" y autorizar).
 *
 *  IMPORTANTE: este script NO guarda la API key en el código. Se guarda de
 *  forma segura en las Propiedades del Script (Script Properties).
 * ============================================================================
 */

// ---------------------------------------------------------------------------
// CONFIGURACIÓN  (ajusta estos valores a tu archivo)
// ---------------------------------------------------------------------------
const CONFIG = {
  // Nombre EXACTO de la pestaña de la que se leen los datos.
  PESTANA_ORIGEN: 'Datos',

  // Nombre EXACTO de la pestaña donde se escribe la respuesta de Claude.
  // Si no existe, el script la crea.
  PESTANA_DESTINO: 'Análisis',

  // Celda donde empieza a escribirse la respuesta.
  CELDA_DESTINO: 'A1',

  // Modelo de Claude. Alternativas: 'claude-haiku-4-5-20251001' (más barato/rápido).
  MODELO: 'claude-sonnet-5',

  // Límite de tokens de la respuesta.
  MAX_TOKENS: 2000,

  // Cuántas filas de la pestaña de origen leer como máximo (evita costos altos).
  MAX_FILAS: 500,

  // Instrucción base para Claude. Describe QUÉ debe analizar y CÓMO responder.
  INSTRUCCION: [
    'Eres un analista de datos para "HOJA DEL PRODUCTOR 2026".',
    'A continuación recibirás los datos de una pestaña en formato de tabla.',
    'Analiza los datos y devuelve un resumen ejecutivo claro y accionable:',
    '- Hallazgos principales.',
    '- Cifras o totales relevantes.',
    '- Riesgos o datos faltantes que detectes.',
    '- Recomendaciones concretas.',
    'Responde en español, en texto plano, sin markdown ni tablas.'
  ].join('\n')
};

// ---------------------------------------------------------------------------
// MENÚ EN LA HOJA
// ---------------------------------------------------------------------------
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('🤖 Claude')
    .addItem('Analizar datos ahora', 'analizarConClaude')
    .addSeparator()
    .addItem('Configurar API key', 'configurarApiKey')
    .addItem('Activar análisis automático (al editar)', 'activarTriggerAlEditar')
    .addItem('Desactivar análisis automático', 'desactivarTriggers')
    .addToUi();
}

// ---------------------------------------------------------------------------
// GUARDAR LA API KEY DE ANTHROPIC (se pide una sola vez)
// ---------------------------------------------------------------------------
function configurarApiKey() {
  const ui = SpreadsheetApp.getUi();
  const resp = ui.prompt(
    'Configurar API key de Anthropic',
    'Pega tu API key (empieza con "sk-ant-..."). Se guarda de forma segura y no queda en el código.',
    ui.ButtonSet.OK_CANCEL
  );
  if (resp.getSelectedButton() !== ui.Button.OK) return;

  const key = resp.getResponseText().trim();
  if (!key) {
    ui.alert('No se guardó nada: la API key estaba vacía.');
    return;
  }
  PropertiesService.getScriptProperties().setProperty('ANTHROPIC_API_KEY', key);
  ui.alert('✅ API key guardada correctamente.');
}

// ---------------------------------------------------------------------------
// FUNCIÓN PRINCIPAL: leer datos, llamar a Claude y escribir la respuesta
// ---------------------------------------------------------------------------
function analizarConClaude() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const hojaOrigen = ss.getSheetByName(CONFIG.PESTANA_ORIGEN);
  if (!hojaOrigen) {
    _avisar('No se encontró la pestaña de origen: "' + CONFIG.PESTANA_ORIGEN + '".');
    return;
  }

  // 1) Leer los datos de la pestaña de origen.
  const datos = _leerDatosComoTexto(hojaOrigen);
  if (!datos) {
    _avisar('La pestaña "' + CONFIG.PESTANA_ORIGEN + '" está vacía.');
    return;
  }

  // 2) Llamar a Claude.
  let respuesta;
  try {
    respuesta = _llamarClaude(CONFIG.INSTRUCCION + '\n\nDATOS:\n' + datos);
  } catch (err) {
    _avisar('Error al llamar a Claude: ' + err.message);
    return;
  }

  // 3) Escribir la respuesta en la pestaña de destino.
  const hojaDestino = _obtenerOCrearHoja(ss, CONFIG.PESTANA_DESTINO);
  const celda = hojaDestino.getRange(CONFIG.CELDA_DESTINO);
  celda.setValue(respuesta);
  celda.offset(0, 1).setValue('Actualizado: ' + new Date());

  _avisar('✅ Análisis generado en la pestaña "' + CONFIG.PESTANA_DESTINO + '".');
}

// ---------------------------------------------------------------------------
// LLAMADA A LA API DE ANTHROPIC (Claude)
// ---------------------------------------------------------------------------
function _llamarClaude(prompt) {
  const apiKey = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');
  if (!apiKey) {
    throw new Error('Falta la API key. Usa el menú "🤖 Claude" > "Configurar API key".');
  }

  const payload = {
    model: CONFIG.MODELO,
    max_tokens: CONFIG.MAX_TOKENS,
    messages: [{ role: 'user', content: prompt }]
  };

  const opciones = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const res = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', opciones);
  const codigo = res.getResponseCode();
  const cuerpo = res.getContentText();

  if (codigo !== 200) {
    throw new Error('HTTP ' + codigo + ' - ' + cuerpo);
  }

  const json = JSON.parse(cuerpo);
  if (!json.content || !json.content.length) {
    throw new Error('Respuesta vacía de la API.');
  }
  // Concatena todos los bloques de texto de la respuesta.
  return json.content.map(function (b) { return b.text || ''; }).join('').trim();
}

// ---------------------------------------------------------------------------
// LEER LOS DATOS DE UNA HOJA COMO TEXTO TABULADO
// ---------------------------------------------------------------------------
function _leerDatosComoTexto(hoja) {
  const rango = hoja.getDataRange();
  let valores = rango.getValues();
  if (!valores.length) return '';

  // Limita el número de filas para controlar el costo.
  if (valores.length > CONFIG.MAX_FILAS) {
    valores = valores.slice(0, CONFIG.MAX_FILAS);
  }

  return valores
    .map(function (fila) {
      return fila
        .map(function (c) { return (c === null || c === undefined) ? '' : String(c); })
        .join('\t');
    })
    .join('\n');
}

// ---------------------------------------------------------------------------
// AUTOMATIZACIÓN: ejecutar al editar la pestaña de origen
// ---------------------------------------------------------------------------
function activarTriggerAlEditar() {
  desactivarTriggers();
  ScriptApp.newTrigger('_onEditAutomatico')
    .forSpreadsheet(SpreadsheetApp.getActiveSpreadsheet())
    .onEdit()
    .create();
  _avisar('✅ Análisis automático activado. Se ejecutará al editar la pestaña "' +
          CONFIG.PESTANA_ORIGEN + '".');
}

function desactivarTriggers() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === '_onEditAutomatico') {
      ScriptApp.deleteTrigger(t);
    }
  });
}

function _onEditAutomatico(e) {
  // Solo reacciona a ediciones dentro de la pestaña de origen.
  if (!e || !e.range) return;
  if (e.range.getSheet().getName() !== CONFIG.PESTANA_ORIGEN) return;
  analizarConClaude();
}

// ---------------------------------------------------------------------------
// UTILIDADES
// ---------------------------------------------------------------------------
function _obtenerOCrearHoja(ss, nombre) {
  return ss.getSheetByName(nombre) || ss.insertSheet(nombre);
}

function _avisar(mensaje) {
  try {
    SpreadsheetApp.getUi().alert(mensaje);
  } catch (e) {
    // Si corre desde un trigger sin UI, se registra en el log.
    Logger.log(mensaje);
  }
}
