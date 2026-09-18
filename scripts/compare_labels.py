import glob
import os
import hashlib
import shutil

DATASET_ROOT = "/Users/nafizimtiazlabib/Downloads/Fabric Defects Dataset"
TARGET_DIR = "/Users/nafizimtiazlabib/FYDP/FYDP/scratch/img_compare"
os.makedirs(TARGET_DIR, exist_ok=True)

def get_hash(fpath):
    with open(fpath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

print("=== CHECK 1: hole/line_2018-10-11*.jpg vs lines/line_2018-10-10*.jpg ===")
hole_oct = sorted(glob.glob(os.path.join(DATASET_ROOT, "hole/line_2018-10-11*")))
lines_oct = sorted(glob.glob(os.path.join(DATASET_ROOT, "lines/line_2018-10-10*")))
print(f"hole oct files ({len(hole_oct)}):")
for f in hole_oct:
    sz = os.path.getsize(f)
    h = get_hash(f)
    print(f"  {os.path.basename(f)} size={sz} md5={h}")
    shutil.copy2(f, os.path.join(TARGET_DIR, "hole_" + os.path.basename(f)))

print(f"lines oct files ({len(lines_oct)}):")
for f in lines_oct:
    sz = os.path.getsize(f)
    h = get_hash(f)
    print(f"  {os.path.basename(f)} size={sz} md5={h}")
    shutil.copy2(f, os.path.join(TARGET_DIR, "lines_" + os.path.basename(f)))

print("\n=== CHECK 2: hole/20180531_*.jpg vs lines/20180531_*.jpg ===")
hole_may = sorted(glob.glob(os.path.join(DATASET_ROOT, "hole/20180531_*")))
lines_may = sorted(glob.glob(os.path.join(DATASET_ROOT, "lines/20180531_*")))
print(f"hole may files ({len(hole_may)}):")
for f in hole_may:
    sz = os.path.getsize(f)
    h = get_hash(f)
    print(f"  {os.path.basename(f)} size={sz} md5={h}")
    shutil.copy2(f, os.path.join(TARGET_DIR, "hole_" + os.path.basename(f)))

print(f"lines may files ({len(lines_may)}):")
for f in lines_may:
    sz = os.path.getsize(f)
    h = get_hash(f)
    print(f"  {os.path.basename(f)} size={sz} md5={h}")
    shutil.copy2(f, os.path.join(TARGET_DIR, "lines_" + os.path.basename(f)))
