import os
import sys
import shutil
from PIL import Image
import imagehash
from concurrent.futures import ThreadPoolExecutor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import INPUT_DIR, OUTPUT_DIR, SIMILARITY_THRESHOLD, KEEP_OPTION, IMAGE_EXTS

def get_image_files(root):
    files = []
    for dirpath, _, filenames in os.walk(root):
        for f in sorted(filenames):
            if f.lower().endswith(IMAGE_EXTS):
                files.append(os.path.join(dirpath, f))
    return files

def compute_hash(path):
    return imagehash.phash(Image.open(path))

def filter_similar_images(image_files, threshold, keep_option):
    if not image_files:
        return []
    with ThreadPoolExecutor() as executor:
        hashes = list(executor.map(compute_hash, image_files))
    groups = []
    current_group = [0]
    for i in range(1, len(hashes)):
        if hashes[i-1] - hashes[i] <= threshold:
            current_group.append(i)
        else:
            groups.append(current_group)
            current_group = [i]
    groups.append(current_group)
    # 그룹별로 keep_option에 따라 인덱스 선택
    keep_indices = []
    for group in groups:
        if keep_option == "first":
            keep_indices.append(group[0])
        elif keep_option == "middle":
            keep_indices.append(group[len(group)//2])
        else:  # last
            keep_indices.append(group[-1])
    return [image_files[i] for i in keep_indices]

def main():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    image_files = get_image_files(INPUT_DIR)
    filtered = filter_similar_images(image_files, SIMILARITY_THRESHOLD, KEEP_OPTION)
    for f in filtered:
        rel = os.path.relpath(f, INPUT_DIR)
        out_path = os.path.join(OUTPUT_DIR, rel)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        shutil.copy2(f, out_path)
    print(f"필터링 완료: {len(filtered)}/{len(image_files)}장 남김. 결과는 {OUTPUT_DIR}에 저장됨.")

if __name__ == "__main__":
    main()
