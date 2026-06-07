# Claro IDE Metadata

Claro includes a small editor-integration command:

```text
claro ide
```

It prints JSON that editor plugins and helper tools can read without scraping docs.

## Fields

- `language`: language display name.
- `version`: Claro version string.
- `file_extensions`: file extensions handled by Claro; currently `.claro`.
- `keywords`: beginner-facing language keywords and multi-word commands.
- `types`: supported static type names, including typed containers such as `LIST OF TEXT` and `MAP OF NUMBER`.
- `commands`: CLI commands useful to editors.
- `snippets`: starter snippets an editor may offer.
- `diagnostics`: diagnostic sources and message format.

## Validation

Run:

```text
python tools/validate_ide_metadata.py
python tools/validate_lsp_helper.py
```

The metadata validator checks that `claro ide` prints valid JSON and includes the required editor-support sections.

The LSP helper validator checks that `support/lsp/claro_lsp_stub.py` can return metadata, completions, and JSON diagnostics from `claro check` plus `claro typecheck`.

## Minimal LSP/helper commands

The helper is intentionally small and command-based so editor plugins can use it without implementing the full Language Server Protocol first:

```text
python support/lsp/claro_lsp_stub.py metadata
python support/lsp/claro_lsp_stub.py completions
python support/lsp/claro_lsp_stub.py diagnostics file.claro
```

`diagnostics` returns a JSON list with:

- `source`: `claro check` or `claro typecheck`
- `file`: normalized file path
- `line`: 1-based line number
- `severity`: currently `error`
- `message`: beginner-readable Claro diagnostic text

## Recommended editor flow

1. Run `claro ide` or `python support/lsp/claro_lsp_stub.py metadata` once to load keywords, snippets, and command metadata.
2. Use `python support/lsp/claro_lsp_stub.py completions` for simple keyword/type completions.
3. On save, run `python support/lsp/claro_lsp_stub.py diagnostics file.claro`.
4. Show diagnostics using the returned JSON objects.
