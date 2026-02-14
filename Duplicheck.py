import os
import hashlib
from collections import defaultdict

def get_file_hash(filepath, chunk_size=8192):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def scan_folder(folder_path):
    hash_dict = {}
    name_dict = defaultdict(list)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png','.jpg','.jpeg','.bmp','.gif','.webp')):
                full_path = os.path.join(root, file)

                # Store filename
                name_dict[file].append(full_path)

                # Store content hash
                file_hash = get_file_hash(full_path)
                hash_dict[file_hash] = full_path

    return hash_dict, name_dict


def check_train_val_leakage(train_path, val_path):
    print("Scanning Train & Validation folders...\n")

    train_hash, train_name = scan_folder(train_path)
    val_hash, val_name = scan_folder(val_path)

    # 🔴 Content Leakage
    content_overlap = set(train_hash.keys()) & set(val_hash.keys())

    print("🔴 CONTENT Leakage (same image copied)")
    if content_overlap:
        print(f"Found {len(content_overlap)} duplicate images!\n")
        for h in content_overlap:
            print("Train:", train_hash[h])
            print("Valid:", val_hash[h])
            print("-" * 60)
    else:
        print("✅ No content leakage found.\n")

    # 🟡 Filename Leakage
    name_overlap = set(train_name.keys()) & set(val_name.keys())

    print("\n🟡 FILENAME Leakage (same filename)")
    if name_overlap:
        print(f"Found {len(name_overlap)} same filenames!\n")
        for name in name_overlap:
            print("Filename:", name)
    else:
        print("✅ No filename leakage found.")


# 🔽 CHANGE PATHS
train_path = r"C:\Users\Dbaiv\Desktop\SDP_Plant\Tomato_disease\train"
val_path   = r"C:\Users\Dbaiv\Desktop\SDP_Plant\Tomato_disease\valid"

check_train_val_leakage(train_path, val_path)