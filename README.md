# File Growth Watcher

A small polling demonstration that reports rapid growth or repeated small writes
to regular files in the current folder. It measures file sizes; it does not read
file contents or record keystrokes.

## Run

Use Python 3.12 or newer. No third-party packages are required.

```sh
python file_growth_watcher.py
```

The folder you run the command from is the folder being watched. Run from a test
folder and append text to a file there to see alerts. Stop with Ctrl+C.

Defaults: poll every second, alert on growth of at least 500 bytes, or four
consecutive increases of 1–300 bytes. The constants near the top of the script
can be edited to change these thresholds.

This is not a keylogger detector, malware detector, or security monitor. Normal
applications can trigger alerts. It cannot identify the writing process; it does
not recurse into subfolders, and changes between polls can be missed. A newly
observed file establishes a baseline before growth is measured. Deleted files
are removed from the stored state.

## Test

```sh
python -m unittest -v
```

## Project history

See [CHANGES.md](CHANGES.md) for the preparation notes.

No distribution license has been selected for this project.
