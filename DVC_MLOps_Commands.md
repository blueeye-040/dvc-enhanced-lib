# DVC MLOps Enhanced Commands Documentation

This project extends DVC with powerful MLOps commands for experiment tracking, dataset management, metrics comparison, and tagging, making DVC more like Git for ML workflows.

---

dvc logs [-n N] [--dataset DATASET] [--show-all]

## Key Enhancements Overview

- **Dual push history system:**
	- Internal log: `.dvc/push_history.json` (versioned, changes with checkout)
	- External/global log: configurable (default: `~/.dvc_push_history_global.json`), append-only, never changes with checkout
	- Logs are strictly separated: no syncing, deduplication, or cross-reading between them

- **Configurable global log path:**
	- Use `dvc configure --global-log-path /custom/path.json` to set the global log file location
	- All commands will use this path for the global log

- **Universal `--internal` flag:**
	- All major commands (`logs`, `exp-list`, `dataset-list`, `metrics-diff`) accept `--internal` to switch between global and internal logs

- **Tag filtering and visibility:**
	- Use `--tag TAG` with `dvc logs` to filter by tag
	- Tags are always shown in log summaries

- **Strict log separation:**
	- Internal and external logs are never merged, deduplicated, or cross-read
	- Each log is updated independently on push

---


### 1. `dvc logs`
Show the history of DVC pushes, including commit info, artifacts, experiment name, metrics, and tags.

**Usage:**
```sh
dvc logs [-n N] [--dataset DATASET] [--show-all] [--internal] [--tag TAG]
```
- `-n N`, `--number N`: Show the last N pushes (default: all)
- `--dataset DATASET`: Filter logs by dataset name
dvc exp-list [--internal]
- `--internal`: Show only the internal (repo) push history for the current commit/branch
> **Tip:** To filter experiments by tag, first use `dvc logs --tag TAGNAME` to find the commit hash for that tag, then use that hash in other commands as needed.
---


### 2. `dvc exp-list`
List all experiments and their metrics from push history.

dvc metrics-diff <commit1> <commit2> [--internal]
```sh
> **Tip:** To compare metrics for a specific tag, first run `dvc logs --tag TAGNAME` to get the commit hash, then use that hash in `dvc metrics-diff`.
- Use `--internal` to show only the internal (repo) log.

---


### 3. `dvc tag`
dvc dataset-list [--internal]

> **Tip:** To see datasets for a specific tag, use `dvc logs --tag TAGNAME` to find the commit hash, then use that hash to filter or reference in your workflow.
dvc tag <tag-name> <commit-hash>
## Example Tutorial Workflow
- Example: `dvc tag v1.0 1234abc`
- Tags can be viewed in all `dvc logs` output and filtered with `--tag`.
# 1. Add and track a dataset

---


### 4. `dvc metrics-diff`
Show the difference in metrics between two commits.

**Usage:**
dvc tag v1.0 <commit-hash>
```sh
dvc metrics-diff <commit1> <commit2> [--internal]
```
- Example: `dvc metrics-diff 1234abc 5678def`
- Shows the value of each metric in both commits.
- Use `--internal` to show only the internal (repo) log.

---


### 5. `dvc dataset-list`
List all datasets tracked in the push history.

**Usage:**
```sh
dvc dataset-list [--internal]
```
- Lists all unique dataset names/paths found in the push history.
- Use `--internal` to show only the internal (repo) log.

---

## Example Workflow

```sh
# Add and track a dataset
dvc add data/sample.txt

# Commit and push as usual (your custom push logic will record extra info)
git add data/sample.txt.dvc .gitignore
git commit -m "Add sample dataset"
dvc push

# Tag a commit
dvc tag v1.0 <commit-hash>

# List experiments
dvc exp-list

# List datasets
dvc dataset-list

# Show metrics difference between two commits
dvc metrics-diff <commit1> <commit2>

# Show push logs with all details
dvc logs --show-all
```

---



## Manual Global Log Path Configuration

You can also manually set the global log file path (instead of using `dvc configure`) by editing the config file directly:

**Edit `~/.dvc_enhance_config.json` and set:**
```json
{
  "global_log_path": "/your/custom/path.json"
}
```
All DVC MLOps commands will use this path for the global log.

**Relevant code (for advanced users):**
The function that reads this config is in `dvc/repo/logs.py`:
```python
def get_global_history_file():
	config_path = os.path.expanduser("~/.dvc_enhance_config.json")
	if os.path.exists(config_path):
		import json
		with open(config_path, "r") as f:
			cfg = json.load(f)
		if "global_log_path" in cfg:
			return os.path.expanduser(cfg["global_log_path"])
	return os.path.expanduser("~/.dvc_push_history_global.json")
```
This function is used by all log-related commands to determine the global log file location.

---

## Notes
- Pushes are now recorded in two places:
	- `.dvc/push_history.json` (internal, versioned, changes with checkout)
	- Global log (default: `~/.dvc_push_history_global.json`, configurable)
- Use `dvc configure --global-log-path /custom/path.json` to set the global log file location.
- By default, all commands use the global file for a complete history, but you can use `--internal` to see only the current repo state.
- All commands work on the push history and are designed for MLOps workflows.
- Internal and external logs are strictly separated and never merged or deduplicated.
- You can extend these commands for more advanced features as needed.

---

For help or issues, visit [https://dvc.org/support](https://dvc.org/support)
