# file-sync.py

import os
import shutil

classFileSync = "sync"

def sync_files(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file in os.listdir(src_dir):
        if file == classFileSync:
            continue
        src_file_path = os.path.join(src_dir, file)
        dst_file_path = os.path.join(dst_dir, file)
        if os.path.exists(dst_file_path):
            shutil.copy2(src_file_path, dst_file_path)
        else:
            shutil.copy2(src_file_path, dst_file_path)

def sync_configs(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file in os.listdir(src_dir):
        if file == classFileSync:
            continue
        src_file_path = os.path.join(src_dir, file)
        dst_file_path = os.path.join(dst_dir, file)
        if os.path.exists(dst_file_path):
            with open(src_file_path, "r") as src_file:
                with open(dst_file_path, "w") as dst_file:
                    dst_file.write(src_file.read())
        else:
            shutil.copy2(src_file_path, dst_file_path)

def main():
    src_dir = input("Введите путь к директории с файлами для синхронизации: ")
    dst_dir = input("Введите путь к директории для синхронизации файлов: ")
    sync_files(src_dir, dst_dir)
    sync_configs(src_dir, dst_dir)

if __name__ == "__main__":
    main()