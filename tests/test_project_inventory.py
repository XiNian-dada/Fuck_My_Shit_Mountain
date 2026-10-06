"""Inventory remains bounded and does not descend into excluded surfaces."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'fuck-my-shit-mountain/scripts'))
import project_inventory as inventory


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'package.json').write_text(json.dumps({'dependencies': {'react':'1.0', 'express':'1.0'}}))
        (self.root / 'src').mkdir()
        (self.root / 'src/index.tsx').write_text('export default function App() {}')

    def test_excluded_directories_are_never_enumerated(self):
        dependency = self.root / 'node_modules'
        dependency.mkdir()
        (dependency / 'secret.js').write_text('dependency')
        cache = self.root / '.git'
        cache.mkdir()
        (cache / 'config').write_text('config')
        scanned = []
        real_scandir = os.scandir
        def record(path):
            scanned.append(Path(path))
            return real_scandir(path)
        with patch.object(inventory.os, 'scandir', side_effect=record):
            report = inventory.build_inventory(self.root, 20)
        self.assertNotIn(dependency, scanned)
        self.assertNotIn(cache, scanned)
        self.assertEqual(report['files_scanned'], 2)
        self.assertIn('frontend', {s['id'] for s in report['surfaces']})
        self.assertIn('backend_api', {s['id'] for s in report['surfaces']})

    def test_file_limit_stops_before_descending(self):
        scanned = []
        real_scandir = os.scandir
        def record(path):
            scanned.append(Path(path))
            return real_scandir(path)
        with patch.object(inventory.os, 'scandir', side_effect=record):
            report = inventory.build_inventory(self.root, 1)
        self.assertEqual(report['files_scanned'], 1)
        self.assertTrue(report['scan_limit_reached'])
        self.assertNotIn(self.root / 'src', scanned)

    def test_symlinks_do_not_expand_scope(self):
        outside = self.root.parent / 'outside-manifest.json'
        (self.root / 'outside-link.json').symlink_to(outside)
        (self.root / 'src/recursive').symlink_to(self.root, target_is_directory=True)
        self.assertEqual(len(inventory.iter_files(self.root, 20)), 2)

    def test_manifest_reads_are_bounded_and_invalid_limits_rejected(self):
        path = self.root / 'large.txt'
        path.write_text('x' * 1000)
        self.assertEqual(inventory.read_text(path, 10), 'x' * 10)
        with self.assertRaises(ValueError):
            inventory.iter_files(self.root, 0)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as result:
            inventory.main([str(self.root), '--max-files', '-1'])
        self.assertEqual(result.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
