---
title: Language servers
description: Let agents navigate code by meaning - definitions, references, symbols - through the language servers you have installed.
---

With a language server installed, agents can use the `lsp` tool to find their way through code by meaning rather than by text search:

| Operation | Answers |
|---|---|
| `goToDefinition` | where a symbol is defined |
| `findReferences` | every use of a symbol |
| `goToImplementation` | the implementations of an interface or behaviour |
| `hover` | the type and documentation at a position |
| `documentSymbol` | the symbols of one file |
| `workspaceSymbol` | a symbol anywhere in the project |

{{product}} starts one server per project and language when an agent first needs it, and stops it again after five minutes without a request. Each request has 30 seconds. Paths stay confined to the project.

## Default servers

{{product}} does not install language servers. It runs these commands when they are on your `PATH`:

| Language | Command |
|---|---|
| Elixir | `elixir-ls --stdio` |
| TypeScript, JavaScript | `typescript-language-server --stdio` |
| Python | `pyright-langserver --stdio` |
| Rust | `rust-analyzer` |
| Go | `gopls serve` |
| C, C++ | `clangd --log=error` |
| Ruby | `solargraph stdio` |
| Java | `jdtls` |
| Swift | `sourcekit-lsp` |
| Zig | `zls` |
| Erlang | none; set one yourself |

## Using another command

Settings → **Language servers** has one row per language. Set your own command there, or from a shell:

```sh
{{cmd}} config set lsp.python "basedpyright-langserver --stdio"
{{cmd}} config reset lsp.python
```

A changed command applies to the next server that starts.

<!-- source: C:apps/swarm_code_daemon/lib/swarm_code/domain/tools/lsp.ex:8,23-24, C:apps/swarm_code_daemon/lib/swarm_code/domain/lsp/client.ex:14,193, C:apps/swarm_code_daemon/lib/swarm_code/domain/lsp.ex:35, C:docs/settings.md:67-83, C:README.md:243, C:apps/swarm_code_cli/lib/swarm_code_cli/release/config_command.ex:48-49 -->
