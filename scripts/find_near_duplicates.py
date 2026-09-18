import glob
import os
import subprocess
import struct

SCRATCH = "scratch/img_compare"
THUMB_DIR = "scratch/thumbs"
os.makedirs(THUMB_DIR, exist_ok=True)

def make_thumb(src_path, thumb_path):
    cmd = ["sips", "-z", "64", "64", "-s", "format", "bmp", src_path, "--out", thumb_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def read_bmp_pixels(bmp_path):
    with open(bmp_path, "rb") as f:
        data = f.read()
    # BMP header: offset to pixel data is at byte 10 (4 bytes uint32)
    pixel_offset = struct.unpack_from("<I", data, 10)[0]
    return data[pixel_offset:]

def compare_sets(set1_pattern, set2_pattern, label1, label2):
    files1 = sorted(glob.glob(os.path.join(SCRATCH, set1_pattern)))
    files2 = sorted(glob.glob(os.path.join(SCRATCH, set2_pattern)))
    
    print(f"Comparing {label1} ({len(files1)} files) vs {label2} ({len(files2)} files)...")
    
    thumbs1 = {}
    for f in files1:
        base = os.path.basename(f)
        thumb = os.path.join(THUMB_DIR, f"{base}.bmp")
        make_thumb(f, thumb)
        thumbs1[base] = read_bmp_pixels(thumb)
        
    thumbs2 = {}
    for f in files2:
        base = os.path.basename(f)
        thumb = os.path.join(THUMB_DIR, f"{base}.bmp")
        make_thumb(f, thumb)
        thumbs2[base] = read_bmp_pixels(thumb)
        
    # Find minimum distance pairs
    min_pairs = []
    for b1, p1 in thumbs1.items():
        for b2, p2 in thumbs2.items():
            if len(p1) != len(p2):
                continue
            # Mean absolute pixel difference
            diff = sum(abs(x - y) for x, y in zip(p1, p2)) / len(p1)
            min_pairs.append((diff, b1, b2))
            
    min_pairs.sort(key=lambda x: x[0])
    print(f"Top 10 closest pairs:")
    for diff, b1, b2 in min_pairs[:10]:
        print(f"  diff={diff:6.2f} | {b1} <---> {b2}")
    
    return min_pairs

print("=== CHECK 1: Oct 2018 (hole line_2018-10-11 vs lines line_2018-10-10) ===")
compare_sets("hole_line_2018-10-11*", "lines_line_2018-10-10*", "hole Oct 11", "lines Oct 10")

print("\n=== CHECK 2: May 2018 (hole 20180531 vs lines 20180531) ===")
compare_sets("hole_20180531_*", "lines_20180531_*", "hole May 31", "lines May 31")

