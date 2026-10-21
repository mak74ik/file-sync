#!/usr/bin/env python3
"""
MeshSync (file-sync): High-performance delta file & config synchronizer CLI.
Built autonomously by Yoshi.
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
import time
from typing import Dict, List, Tuple


def get_file_hash(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def scan_dir(root: str) -> Dict[str, dict]:
    result = {}
    root = os.path.abspath(root)
    if not os.path.exists(root):
        return result

    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            full_p = os.path.join(dirpath, fname)
            rel_p = os.path.relpath(full_p, root)
            try:
                st = os.stat(full_p)
                result[rel_p] = {
                    "size": st.st_size,
                    "mtime": st.st_mtime,
                    "hash": get_file_hash(full_p),
                }
            except Exception:
                pass
    return result


def sync_directories(src_dir: str, dst_dir: str, delete_orphan: bool = False, dry_run: bool = False) -> Tuple[int, int, int]:
    """
    Synchronizes files from src_dir to dst_dir based on SHA-256 content hashes.
    Returns (copied_count, updated_count, deleted_count).
    """
    src_abs = os.path.abspath(src_dir)
    dst_abs = os.path.abspath(dst_dir)

    if not os.path.exists(src_abs):
        raise FileNotFoundError(f"Source directory does not exist: {src_abs}")

    if not dry_run:
        os.makedirs(dst_abs, exist_ok=True)

    src_files = scan_dir(src_abs)
    dst_files = scan_dir(dst_abs)

    copied = 0
    updated = 0
    deleted = 0

    # 1. Copy / Update from src to dst
    for rel_p, meta in src_files.items():
        src_p = os.path.join(src_abs, rel_p)
        dst_p = os.path.join(dst_abs, rel_p)

        if rel_p not in dst_files:
            print(f"[+] COPY: {rel_p} ({meta['size']} bytes)")
            copied += 1
            if not dry_run:
                os.makedirs(os.path.dirname(dst_p), exist_ok=True)
                shutil.copy2(src_p, dst_p)
        elif dst_files[rel_p]["hash"] != meta["hash"]:
            print(f"[*] UPDATE: {rel_p}")
            updated += 1
            if not dry_run:
                shutil.copy2(src_p, dst_p)

    # 2. Delete orphans in dst if requested
    if delete_orphan:
        for rel_p in dst_files:
            if rel_p not in src_files:
                dst_p = os.path.join(dst_abs, rel_p)
                print(f"[-] DELETE: {rel_p}")
                deleted += 1
                if not dry_run:
                    if os.path.isfile(dst_p):
                        os.remove(dst_p)

    return copied, updated, deleted


def main():
    parser = argparse.ArgumentParser(description="MeshSync: Fast delta directory & config synchronizer")
    parser.add_argument("--src", required=True, help="Source directory")
    parser.add_argument("--dst", required=True, help="Destination directory")
    parser.add_argument("--delete", action="store_true", help="Delete files in destination that do not exist in source")
    parser.add_argument("--dry-run", action="store_true", help="Preview file changes without applying them")
    parser.add_argument("--json", action="store_true", help="Output summary in JSON format")

    args = parser.parse_args()

    copied, updated, deleted = sync_directories(
        src_dir=args.src, dst_dir=args.dst, delete_orphan=args.delete, dry_run=args.dry_run
    )

    if args.json:
        print(json.dumps({"copied": copied, "updated": updated, "deleted": deleted}))
    else:
        status = " (DRY-RUN)" if args.dry_run else ""
        print(f"\nSync complete{status}: {copied} copied, {updated} updated, {deleted} deleted.")


if __name__ == "__main__":
    main()