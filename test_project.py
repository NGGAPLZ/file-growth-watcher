import contextlib
import io
from pathlib import Path
import unittest
from unittest.mock import patch
import file_growth_watcher as watcher

import contextlib
import uuid

@contextlib.contextmanager
def test_folder():
    # A unique local directory also works in restricted Windows environments.
    folder = Path.cwd() / (".test-" + uuid.uuid4().hex)
    folder.mkdir()
    try:
        yield str(folder)
    finally:
        for child in folder.iterdir():
            if child.is_dir():
                child.rmdir()
            else:
                child.unlink()
        folder.rmdir()

class WatcherTests(unittest.TestCase):
    def test_snapshot_respects_directory(self):
        with test_folder() as folder:
            (Path(folder)/'sample.txt').write_bytes(b'abc')
            (Path(folder)/'subdirectory').mkdir()
            self.assertEqual(watcher.seed_state(folder), {'sample.txt':3})

    def run_snapshots(self, snapshots):
        out = io.StringIO()
        with patch.object(watcher, 'seed_state', side_effect=snapshots + [KeyboardInterrupt()]), patch.object(watcher.time, 'sleep'), contextlib.redirect_stdout(out):
            watcher.main()
        return out.getvalue()

    def test_rapid_growth(self):
        self.assertIn('Rapid file growth detected', self.run_snapshots([{'a':0},{'a':600}]))

    def test_consecutive_small_writes(self):
        self.assertIn('Consecutive small writes', self.run_snapshots([{'a':0},{'a':10},{'a':20},{'a':30},{'a':40}]))

    def test_deleted_file_resets_streak(self):
        out = self.run_snapshots([{'a':0},{'a':10},{'a':20},{'a':30},{},{'a':100},{'a':110}])
        self.assertNotIn('[ALERT]', out)

if __name__ == '__main__':
    unittest.main()
