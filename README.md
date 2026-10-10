# MeshSync (`file-sync`)

> **Fast delta directory and config synchronizer with SHA-256 hash verification.**  
> Built and tested autonomously by **Auto Qwen AI**.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🌟 Overview

`MeshSync` synchronizes local directories and configuration trees based on SHA-256 content hashes, avoiding unnecessary writes and preserving filesystem timestamps.

---

## 🚀 Usage

### 1. Synchronize Source to Destination
```bash
python3 main.py --src ./configs --dst ./backup_configs
```

### 2. Preview Changes (Dry-Run)
```bash
python3 main.py --src ./configs --dst ./backup_configs --dry-run
```

### 3. Synchronize with Deletion of Orphaned Files
```bash
python3 main.py --src ./configs --dst ./backup_configs --delete
```

### 4. Output Machine Summary in JSON
```bash
python3 main.py --src ./configs --dst ./backup_configs --json
```

---

## 🧪 Testing

Run automated unit tests:
```bash
python3 -m unittest discover -s tests
```

---

## 👥 Credits

Developed autonomously by **Auto Qwen AI**:
- 🤖 **Autonomous Engine**: Auto Qwen AI Pipeline
- ⚡ **Core Engine**: SHA-256 Delta Content Differencer
- 🛡️ **Quality Assurance**: Automated Filesystem Regression Tests
