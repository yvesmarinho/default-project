# Temporary Files Directory

This directory is used for temporary files during development and script execution.

## Purpose
- Store temporary files during script execution
- Safer alternative to /tmp/ for project-specific temporary files
- Automatically cleaned on session end (see cleanup scripts)

## Usage
Scripts should use `./tmp/` instead of `/tmp/` for project-related temporary files.

Example:
```bash
# Instead of
temp_file="/tmp/myfile.txt"

# Use
temp_file="./tmp/myfile.txt"
```

## Cleanup
This directory is automatically cleaned by:
- `.github/prompts/session-end.prompt.md` ritual
- `scripts/cleanup-tmp.sh` (can be run manually)

## .gitignore
All files in this directory are ignored by git (except this README).

