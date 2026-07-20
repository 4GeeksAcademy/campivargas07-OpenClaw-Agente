---
name: learning-journal
description: >-
  Formatea apuntes de aprendizaje diario y los guarda en Google Docs y memory/.
  Usa cuando el usuario diga qué aprendió hoy, quiera registrar una lección,
  añadir al diario de conocimiento, o practicar vocabulario de inglés técnico.
---

# Diario de Aprendizaje (AI + Inglés)

Captura lo que Carlos aprendió y lo estructura en su diario persistente.

## Prerrequisitos

- Google Docs/Drive vía Composio (`mcporter`)
- Carpeta `memory/` en el workspace
- Intereses de Carlos: AI Engineering, Python, inglés, automatización (USER.md)

## Configuración (primera vez)

Si no existe en TOOLS.md, preguntar y guardar:

```markdown
### 📓 Diario de Aprendizaje
- **Google Doc:** [nombre o ID del doc]
- **Doc URL:** https://docs.google.com/document/d/DOC_ID/edit
```

Si no hay Doc aún, crear uno:

```bash
mcporter call composio.COMPOSIO_SEARCH_TOOLS \
  queries='[{"use_case": "create a new Google Doc document"}]' \
  session='{"generate_id": true}'
```

Título sugerido: `Diario de Aprendizaje — Carlos Vargas`

## Flujo

### 1. Recibir input del usuario

Aceptar 2–5 bullets en texto libre. Ejemplos:

```
hoy aprendí:
- async/await en Python con asyncio
- qué es un MCP server y cómo se conecta
- vocab: trade-off, bottleneck
```

Si el input es vago, pedir al menos un punto concreto antes de guardar.

### 2. Estructurar la entrada

```markdown
## 2026-07-20 — Async Python y MCP

**Qué aprendí:**
- `async/await` permite I/O concurrente sin threads
- MCP (Model Context Protocol) estandariza cómo los agentes usan herramientas externas

**Cómo lo aplicaría:**
- Refactorizar scripts de scraping con asyncio
- Conectar un MCP server propio para ClickUp

**Vocabulario EN:**
- *trade-off* — compromiso entre dos opciones
- *bottleneck* — cuello de botella, punto que limita rendimiento

**Tags:** #python #ai-engineering #mcp
```

**Reglas de formato:**
- Fecha en timezone México
- Tema principal en el título (inferir del contenido)
- Vocabulario EN solo si el usuario mencionó inglés o términos técnicos en inglés
- Tags: máximo 4, relevantes a intereses de Carlos

### 3. Guardar en Google Doc

Buscar el doc:

```bash
mcporter call composio.COMPOSIO_MULTI_EXECUTE_TOOL \
  tools='[{"tool_slug": "GOOGLEDRIVE_FIND_FILE", "arguments": {"q": "name = '\''Diario de Aprendizaje'\'' and mimeType = '\''application/vnd.google-apps.document'\''"}}]' \
  sync_response_to_workbench=false
```

Append al final del documento (buscar herramienta `GOOGLEDOCS_*` vía `COMPOSIO_SEARCH_TOOLS` si no está documentada):

```bash
mcporter call composio.COMPOSIO_SEARCH_TOOLS \
  queries='[{"use_case": "append text to end of Google Doc"}]' \
  session='{"generate_id": true}'
```

### 4. Guardar en memoria local

Añadir sección a `memory/YYYY-MM-DD.md` (crear si no existe):

```markdown
## Aprendizaje

### [tema principal]
- [puntos estructurados]
- Doc actualizado: [link]
```

Leer el archivo primero (AGENTS.md) y escribir solo actualizaciones concretas.

### 5. Confirmar

```
✅ Entrada guardada en tu diario

📓 2026-07-20 — Async Python y MCP
   🔗 [Abrir en Google Docs](https://docs.google.com/document/d/...)
   📝 También en memory/2026-07-20.md
```

## Reglas

- No inventar aprendizajes — solo formatear lo que Carlos dijo
- Si mezcla español e inglés, mantener el idioma original del usuario
- Una entrada por día (si ya existe, append como sub-sección con hora)
- No guardar secretos, API keys ni credenciales

## Triggers

- "qué aprendí hoy"
- "añade al diario"
- "registra esto en mi diario de aprendizaje"
- "guarda esta lección"
- "vocabulario: ..."
