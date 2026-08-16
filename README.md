# cursor-rules

Machine-local [Cursor](https://cursor.com) user rules for `~/.cursor/rules/`.

These rules apply globally in every Cursor session on a machine where they are installed (`alwaysApply: true`).

## Rules

| File | Purpose |
|------|---------|
| `build-parallelism.mdc` | Leave one CPU core free when running parallel builds (`cargo`, `make`, `cmake`, etc.) |
| `linear-post-approval.mdc` | Require explicit user approval before posting or editing Linear content |
| `pkexec-sudo-auth.mdc` | Use `pkexec` instead of interactive `sudo` for privilege escalation |

## Install

Clone and symlink (recommended):

```bash
git clone git@github.com:rustechs/cursor-rules.git ~/git/cursor-rules
mkdir -p ~/.cursor
# If ~/.cursor/rules already exists as a directory, move or remove it first.
ln -sfn ~/git/cursor-rules/.cursor/rules ~/.cursor/rules
```

Or copy files directly:

```bash
mkdir -p ~/.cursor/rules
cp ~/git/cursor-rules/.cursor/rules/*.mdc ~/.cursor/rules/
```

Restart Cursor or start a new chat for rule changes to take effect.

## Updating

Edit rules in this repo, commit, push, then pull on other machines:

```bash
cd ~/git/cursor-rules && git pull
```

Symlink installs pick up file changes after `git pull`; restart Cursor or start a
new chat so an active session reloads the rules. Copy installs need a fresh
`cp` of the `.mdc` files.

## CI

`.github/workflows/validate-rules.yml` runs on pull requests and on pushes to
`main`/`master`. It checks every `.cursor/rules/*.mdc` file for required YAML
frontmatter (`description`, `alwaysApply`).

Run the same check locally:

```bash
python3 scripts/validate-rules.py
```
