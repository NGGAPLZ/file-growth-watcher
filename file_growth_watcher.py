"""
file_growth_watcher.py
Behavioral detector: raises alerts for fast or frequent small file writes.
No external libraries required.(no admin needed).

How it works (brief):
 - Every CHECK_INTERVAL seconds it records file sizes.
 - If a file grows by >= GROWTH_THRESHOLD bytes within one interval -> alert.
 - Also counts consecutive intervals where a file grows by a small amount (SMALL_WRITE_MAX).
   If that count reaches SMALL_WRITE_COUNT -> alert (many small writes).
 - Does NOT look for filenames. Purely behavioral.

Run:
 python file_growth_watcher.py
"""
import os
import time
from collections import defaultdict

CHECK_INTERVAL = 1.0            # seconds between checks
GROWTH_THRESHOLD = 500          # bytes growth in one interval reported by the watcher
SMALL_WRITE_MAX = 300           # bytes considered a "small write" event
SMALL_WRITE_COUNT = 4           # number of consecutive small-write intervals to flag
QUIET_MODE = False              # set True to reduce output noise

def seed_state(path='.'):
    sizes = {}
    for fname in os.listdir(path):
        try:
            full_path = os.path.join(path, fname)
            if os.path.isfile(full_path):
                sizes[fname] = os.path.getsize(full_path)
        except OSError:
            continue
    return sizes

def human(n):
    # human-readable bytes
    for unit in ('B','KB','MB','GB'):
        if n < 1024:
            return f"{n:.0f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"

def main():
    print("Generic fast-write watcher started. Monitoring current folder.")
    print("Alerts: rapid growth >= {} bytes or {} consecutive small writes (<= {} bytes)."
          .format(GROWTH_THRESHOLD, SMALL_WRITE_COUNT, SMALL_WRITE_MAX))
    sizes = seed_state('.')
    small_write_streaks = defaultdict(int)

    try:
        while True:
            any_alert = False
            snapshot = seed_state('.')
            for missing in set(sizes) - set(snapshot):
                sizes.pop(missing, None)
                small_write_streaks.pop(missing, None)
            for fname, cur in snapshot.items():
                prev = sizes.get(fname, cur)
                delta = cur - prev

                # update stored size
                sizes[fname] = cur

                # check large single-interval growth
                if delta >= GROWTH_THRESHOLD:
                    print("\n[ALERT] Rapid file growth detected:", fname)
                    print("  Growth:", human(delta), "in last", CHECK_INTERVAL, "s")
                    any_alert = True
                    small_write_streaks[fname] = 0
                    continue

                # check many small writes in a row
                if 0 < delta <= SMALL_WRITE_MAX:
                    small_write_streaks[fname] += 1
                    if small_write_streaks[fname] >= SMALL_WRITE_COUNT:
                        print("\n[ALERT] Consecutive small writes detected:", fname)
                        print("  Recent small writes count:", small_write_streaks[fname],
                              "latest growth:", human(delta))
                        any_alert = True
                        # reset streak after alert to avoid spam
                        small_write_streaks[fname] = 0
                else:
                    # reset streak if no recent small write
                    small_write_streaks[fname] = 0

            if not QUIET_MODE and not any_alert:
                # lightweight heartbeat so audience sees the tool is live
                print(".", end="", flush=True)

            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nWatcher stopped by user. Exiting.")

if __name__ == "__main__":
    main()