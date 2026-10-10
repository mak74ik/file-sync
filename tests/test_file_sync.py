import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import sync_directories


class TestFileSync(unittest.TestCase):
    def setUp(self):
        self.src_dir = tempfile.mkdtemp()
        self.dst_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.src_dir, ignore_errors=True)
        shutil.rmtree(self.dst_dir, ignore_errors=True)

    def test_sync_new_and_update(self):
        # 1. Create file in src
        file_a = os.path.join(self.src_dir, "test.txt")
        with open(file_a, "w") as f:
            f.write("Initial content")

        copied, updated, deleted = sync_directories(self.src_dir, self.dst_dir)
        self.assertEqual(copied, 1)
        self.assertEqual(updated, 0)
        self.assertTrue(os.path.isfile(os.path.join(self.dst_dir, "test.txt")))

        # 2. Modify file in src
        with open(file_a, "w") as f:
            f.write("Updated content version 2")

        copied, updated, deleted = sync_directories(self.src_dir, self.dst_dir)
        self.assertEqual(copied, 0)
        self.assertEqual(updated, 1)

        with open(os.path.join(self.dst_dir, "test.txt")) as f:
            self.assertEqual(f.read(), "Updated content version 2")

    def test_sync_with_deletion(self):
        # Create file in dst that is not in src
        orphan = os.path.join(self.dst_dir, "orphan.txt")
        with open(orphan, "w") as f:
            f.write("Orphan")

        copied, updated, deleted = sync_directories(self.src_dir, self.dst_dir, delete_orphan=True)
        self.assertEqual(deleted, 1)
        self.assertFalse(os.path.exists(orphan))


if __name__ == "__main__":
    unittest.main()
