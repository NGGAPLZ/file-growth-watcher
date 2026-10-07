# Coursework background

NGGAPLZ originally presented this project alongside a consent-based local keyboard
logging demonstration. The presentation contrasted a program that writes key
events with a polling loop that notices file-size growth.

## What the demonstration explored

The logging example asked for typed consent, timestamped key events, stopped on
Escape, and offered a cleanup step. The watcher recorded file sizes, compared
successive observations and counted repeated small increases.

The important boundary is that **file growth is not proof of keylogging**. Editors,
application logs and many legitimate programs also append small amounts of data.
The watcher cannot identify the writing process or determine the meaning of data.
It can also miss activity outside its watched folder or between polling intervals.

The current repository accurately calls this a file-growth watcher. Its cleaned
implementation also respects the supplied directory during initial size sampling
and resets state for deleted files. The classroom presentation predates those fixes.

## Demonstration without recording keystrokes

Run the watcher in a disposable folder and append harmless text to a file there
from a second terminal. Compare a large append with several small appends separated
by the polling interval. Observe both alerts and missed/benign events. This exercises
the same file-growth logic without needing to capture real keyboard input.

The original presentation's embedded video and slide backgrounds are omitted.
The video has not been privacy-reviewed, and the source artwork's redistribution
provenance is unclear. No claims of reliable malware detection are made.
