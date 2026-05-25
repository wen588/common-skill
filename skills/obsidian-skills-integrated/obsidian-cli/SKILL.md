---
name: obsidian-cli
description: Interact with Obsidian vaults via the Obsidian CLI including plugin and theme development. Use when the user wants to create/read/append notes, search vault, manage properties, or develop plugins/themes for Obsidian.
---

# Obsidian CLI Skill

This skill enables skills-compatible agents to interact with a running Obsidian instance via the `obsidian` CLI. It bridges the system shell and the Obsidian application API, enabling vault operations, note management, and plugin/theme development.

## Requirements

- Obsidian must be running and the Obsidian CLI plugin must be enabled
- The `obsidian` command must be available in the agent's PATH
- CLI communicates with Obsidian via a local HTTP API

## Command Syntax

### Parameters

Parameters are key-value pairs assigned using `=`:

```
obsidian command parameter=value parameter="value with spaces"
```

### Flags

Flags are boolean switches that don't require a value:

```
obsidian command flag
```

Common flags:
- `silent` — prevents the file from opening in the Obsidian UI
- `overwrite` — replaces existing content when creating a file
- `open` — opens the file in Obsidian after the operation
- `--copy` — copies command output to system clipboard
- `total` — with list-based commands, returns a count instead of items

### Multi-line Content

For multi-line content, use HEREDOC syntax to avoid escaping issues:

```bash
obsidian create name="Note" content<<EOF
# Heading

Line 1
Line 2
EOF
```

## Targeting

### File Targeting

| Parameter | Description |
|-----------|-------------|
| `file=<name>` | Resolves like an Obsidian wikilink (name only, path and extension optional) |
| `path=<path>` | Exact path relative to vault root, including extension |

If neither is provided, defaults to the currently active file.

### Vault Targeting

By default, commands target the most recently focused vault. To target a specific vault, use `vault=<name>` as the first parameter.

## Note Management Patterns

| Operation | Command |
|-----------|---------|
| Read a note | `obsidian read file="My Note"` |
| Create a note | `obsidian create name="New Note" content="# Hello" template="Template" silent` |
| Append content | `obsidian append file="My Note" content="New line"` |
| Search vault | `obsidian search query="search term" limit=10` |
| Read daily note | `obsidian daily:read` |
| Append to daily | `obsidian daily:append content="- [ ] Task"` |
| Set property | `obsidian property:set name="status" value="done" file="My Note"` |
| Get property | `obsidian property:get name="status" file="My Note"` |
| List tags | `obsidian tags sort=count counts` |
| Find backlinks | `obsidian backlinks file="My Note"` |
| List tasks | `obsidian tasks daily todo` |

## Plugin & Theme Development

### Workflow

1. Hot reload after code changes:

```bash
obsidian hotreload
```

2. Inspect errors:

```bash
obsidian console
```

3. Visual debugging:

```bash
obsidian screenshot path="relative/output.png"
obsidian css:get selector=".my-class" property="background"
obsidian css:set selector="body" property="--my-var" value="red"
```

4. JavaScript evaluation (backdoor for advanced debugging):

```bash
obsidian eval code="console.log('hello')"
```

Or with multi-line content:

```bash
obsidian eval code<<EOF
const plugin = app.plugins.getPlugin('my-plugin');
console.log(plugin.settings);
EOF
```

## Diagnostics

Check if Obsidian CLI is responding:

```bash
obsidian ping
```
