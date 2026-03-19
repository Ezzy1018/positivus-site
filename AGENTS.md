# AGENTS.md

## Project Overview

Figma-to-HTML design system pipeline. Figma JSON exports are parsed by Python scripts to generate pixel-perfect HTML/CSS, then pushed back to Figma via MCP (Model Context Protocol).

**Languages:** Python 3, JavaScript (ES modules `.mjs`), HTML5, CSS3
**No build system, bundler, or TypeScript configured.**

## Directory Structure

- `positivus_figma.json` — Raw Figma API export
- `parse_positivus.py` — Simple Figma JSON parser (text dump)
- `strict_parse.py` — Figma JSON to CSS-styled HTML generator
- `ast_compiler.py` — Figma AST to full HTML compiler
- `trigger_mcp.py` — MCP client calling Figma MCP tool
- `positivus_complete/` — Node.js MCP integration scripts + built HTML/CSS
  - `push_to_figma.mjs` — MCP stdio client → `figma-developer-mcp`
  - `push_h2d.mjs` — MCP SSE client → html.to.design MCP
  - `push_sse.mjs` — MCP SSE client → official Figma MCP
  - `list_h2d_tools.mjs` — Lists tools from html.to.design MCP
- `designer-system/` — CSS design tokens, components, rendered HTML pages
  - `styles/tokens.css`, `components.css`, `forms.css` — iOS 16 design system
  - `positivus.css`, `unsia.css` — Page-specific styles

## Commands

### Running Python scripts

```bash
python3 parse_positivus.py              # Parse Figma JSON to text
python3 strict_parse.py                 # Generate CSS-styled HTML from Figma JSON
python3 ast_compiler.py                 # Compile Figma AST to full HTML
python3 trigger_mcp.py                  # Run MCP client
```

### Running Node.js scripts

```bash
cd positivus_complete
npm install                             # Install dependencies (first time only)
node push_to_figma.mjs                  # Push HTML to Figma via local MCP
node push_h2d.mjs                       # Push via html.to.design MCP (SSE)
node push_sse.mjs                       # Push via official Figma MCP (SSE)
node list_h2d_tools.mjs                 # List available html.to.design MCP tools
```

### Tests

No test framework is configured. The `package.json` test script is a placeholder stub.

### Linting

No linter or formatter is configured. No `.eslintrc`, `.prettierrc`, or `ruff.toml` exists.

## Code Style

### Python

- **Indentation:** 4 spaces
- **Entry point:** `if __name__ == "__main__": main()`
- **Functions:** Simple procedural style, no type hints, no docstrings
- **Imports:** Standard library only (`json`, `sys`) except `trigger_mcp.py` which uses `mcp` and `asyncio`
- **Strings:** Inconsistent quoting (mix of single and double quotes) — prefer double quotes for consistency
- **Conditionals:** Compact one-liners are acceptable (`if mode == "HORIZONTAL": return "row"`)
- **I/O:** Use `json.load()` / `json.dump()` for JSON file operations
- **Error handling:** Minimal; scripts assume valid input

### JavaScript (Node.js)

- **Indentation:** 2 spaces
- **Module format:** ES modules via `.mjs` file extension
- **Imports:** Use `import ... from` syntax
- **Async pattern:** Single top-level `async function run()` with `run().catch(console.error)` at bottom
- **Logging:** `console.log` for output, `console.error` for errors
- **Shutdown:** `process.exit(0)` for graceful exit
- **Semicolons:** Always use semicolons
- **Strings:** Prefer template literals for interpolation
- **Error handling:** `.catch()` on the top-level run function; throw on unexpected failures

### HTML

- Use semantic HTML5 elements (`<header>`, `<main>`, `<section>`, `<footer>`)
- Include Google Fonts import for Space Grotesk in `<head>`
- Mobile-first responsive design with `@media(max-width: 900px)` breakpoints

### CSS

- Use CSS custom properties (variables) for design tokens
- BEM-like class naming: `.service-card`, `.process-card`, `.btn-dark`
- Responsive typography via `clamp()`
- Layout via CSS Grid and Flexbox
- Design palette: green `#B9FF66`, dark `#191A23`, gray `#F3F3F3`, white `#FFFFFF`
- Border radius convention: `45px` for cards (brutalist style)
- Hard borders and drop shadows for visual emphasis

## MCP Integration Notes

- `push_to_figma.mjs` uses stdio transport to connect to a local `figma-developer-mcp` server
- `push_sse.mjs` connects to `mcp.figma.com` via SSE
- `push_h2d.mjs` connects to `h2d-mcp.divriots.com` via SSE
- All MCP scripts follow the same pattern: connect → list tools → call tool → disconnect
- Dependencies: `@modelcontextprotocol/sdk`, `@figma/code-connect`, `eventsource`
