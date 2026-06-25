import os
import random
import string
import csv

# Folder containing .npy files
FOLDER = r"embeddings"

# Length of random filename
RANDOM_NAME_LENGTH = 12

def random_name(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

used_names = set()

mapping = []

for filename in os.listdir(FOLDER):
    if filename.endswith(".npy"):
        old_path = os.path.join(FOLDER, filename)

        # Generate unique random name
        while True:
            new_name = random_name(RANDOM_NAME_LENGTH) + ".npy"
            if new_name not in used_names and not os.path.exists(os.path.join(FOLDER, new_name)):
                used_names.add(new_name)
                break

        new_path = os.path.join(FOLDER, new_name)

        os.rename(old_path, new_path)

        mapping.append([filename, new_name])

        print(f"{filename} -> {new_name}")

# Save mapping
mapping_file = os.path.join(FOLDER, "mapping.csv")

with open(mapping_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Original Filename", "Random Filename"])
    writer.writerows(mapping)

print("\nDone!")
print(f"Mapping saved to: {mapping_file}")