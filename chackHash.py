import imagehash
from PIL import Image
import os
import glob
from tqdm import tqdm # Optional: for progress bar

def compute_hashes(directory):
    """
    Computes pHash for all images in a directory (and subdirectories).
    Returns a dictionary: { hash_object: [file_path, ...] }
    """
    hashes = {}
    # Walk through all files in directory
    image_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                image_paths.append(os.path.join(root, file))

    print(f"Processing {len(image_paths)} images in {directory}...")

    for path in tqdm(image_paths):
        try:
            with Image.open(path) as img:
                # pHash is robust to resizing and minor color changes
                h = imagehash.phash(img)
                
                # Store hash (handle potential collisions within the same set)
                if h in hashes:
                    hashes[h].append(path)
                else:
                    hashes[h] = [path]
        except Exception as e:
            print(f"Error processing {path}: {e}")
            
    return hashes

def find_leakage(train_dir, test_dir, hash_cutoff=5):
    """
    Compares Train hashes vs Test hashes.
    cutoff=0 -> Exact duplicates only.
    cutoff=5 -> Allows for slight modifications (resize/compression/crop).
    """
    print("--- Computing Train Hashes ---")
    train_hashes = compute_hashes(train_dir)
    
    print("\n--- Computing Test Hashes ---")
    test_hashes = compute_hashes(test_dir)

    leaks = []
    
    print("\n--- Checking for Leakage ---")
    # Iterate through all Test hashes and compare with Train hashes
    for test_h, test_paths in tqdm(test_hashes.items()):
        for train_h, train_paths in train_hashes.items():
            # Calculate Hamming distance between hashes
            diff = test_h - train_h
            
            if diff <= hash_cutoff:
                # Leak found!
                for t_path in test_paths:
                    for tr_path in train_paths:
                        leaks.append({
                            'test_image': t_path,
                            'train_image': tr_path,
                            'distance': diff
                        })

    return leaks

# ==========================================
# CONFIGURATION
# ==========================================
TRAIN_DIR = r'C:\Users\Dbaiv\Desktop\SDP_Plant\Grape_disease\train'  # <--- UPDATE THIS
TEST_DIR = r'C:\Users\Dbaiv\Desktop\SDP_Plant\Grape_disease\valid'    # <--- UPDATE THIS

# Cutoff 0 = Exact match. 
# Cutoff < 5 = Very similar (likely just resized or compressed)
LEAKAGE_THRESHOLD = 5 

# ==========================================
# EXECUTION
# ==========================================
leaks = find_leakage(TRAIN_DIR, TEST_DIR, LEAKAGE_THRESHOLD)

print(f"\nResult: Found {len(leaks)} potential leaks between Train and Test.")

if leaks:
    print("\nSample Leaks:")
    for leak in leaks[:10]: # Print first 10
        print(f"Distance: {leak['distance']}")
        print(f"  Test:  {leak['test_image']}")
        print(f"  Train: {leak['train_image']}")
        print("-" * 30)
    
    print("\nSuggest removing these files from the Training set and retraining.")
else:
    print("✅ No data leakage detected! Your 99% accuracy is likely genuine.")