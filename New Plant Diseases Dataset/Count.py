import os

root = r"C:\Users\Dbaiv\Desktop\SDP_Plant\Grape_disease\valid"
total_count = 0

for subfolder in os.listdir(root):
    sub_path = os.path.join(root, subfolder)
    if os.path.isdir(sub_path):
        count = 0
        for _, _, files in os.walk(sub_path):
            count += len(files)

        print(subfolder, "->", count)
        total_count += count   # ✅ Correct place

print("Total count:", total_count)
