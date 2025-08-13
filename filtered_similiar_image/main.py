import os
import sys
import shutil
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
from concurrent.futures import ProcessPoolExecutor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import INPUT_DIR, OUTPUT_DIR, SIMILARITY_THRESHOLD, KEEP_OPTION, IMAGE_EXTS

def get_image_files_by_folder(root):
    folder_dict = {}
    for dirpath, _, filenames in os.walk(root):
        rel_folder = os.path.relpath(dirpath, root)
        files = [os.path.join(dirpath, f) for f in sorted(filenames) if f.lower().endswith(IMAGE_EXTS)]
        if files:
            folder_dict[rel_folder] = files
    return folder_dict

def compute_similarity_pair(args):
    img1_path, img2_path = args
    try:
        img1 = np.array(Image.open(img1_path).convert("L").resize((256,256)))
        img2 = np.array(Image.open(img2_path).convert("L").resize((256,256)))
        score, _ = ssim(img1, img2, full=True)
        return score
    except Exception as e:
        print(f"이미지 유사도 계산 오류: {img1_path}, {img2_path} -> {e}")
        return 0

def filter_similar_images(image_files, threshold, keep_option):
    if not image_files:
        return []
    print(f"[1/3] 이미지 유사도 기반 그룹핑 시작 (총 {len(image_files)}장) ...")
    groups = []
    used = [False] * len(image_files)
    with ProcessPoolExecutor() as executor:
        for i in range(len(image_files)):
            if used[i]:
                continue
            current_group = [i]
            used[i] = True
            # 병렬로 SSIM 계산
            pairs = [(image_files[i], image_files[j]) for j in range(i+1, len(image_files)) if not used[j]]
            results = list(executor.map(compute_similarity_pair, pairs))
            for idx, j in enumerate([j for j in range(i+1, len(image_files)) if not used[j]]):
                sim = results[idx]
                if sim >= threshold:
                    current_group.append(j)
                    used[j] = True
            groups.append(current_group)
            if (i+1) % 50 == 0 or i == len(image_files)-1:
                print(f"  진행률: {i+1}/{len(image_files)}장 비교 완료, 현재 그룹 수: {len(groups)}")
    print(f"[2/3] 그룹핑 완료: 총 {len(groups)}개 그룹 생성")
    large_groups = sorted(groups, key=len, reverse=True)[:5]
    for idx, group in enumerate(large_groups):
        if len(group) > 1:
            print(f"  그룹 {idx+1}: {len(group)}개 이미지 (예: {os.path.basename(image_files[group[0]])})")
    keep_indices = []
    total_removed = 0
    for group in groups:
        if len(group) > 1:
            total_removed += len(group) - 1
        if keep_option == "first":
            keep_indices.append(group[0])
        elif keep_option == "middle":
            keep_indices.append(group[len(group)//2])
        else:
            keep_indices.append(group[-1])
    print(f"[2/3] 제거될 중복 이미지: {total_removed}개")
    return [image_files[i] for i in keep_indices]

def main():
    print(f"INPUT_DIR: {INPUT_DIR}")
    print(f"INPUT_DIR 절대경로: {os.path.abspath(INPUT_DIR)}")
    print(f"INPUT_DIR 존재 여부: {os.path.exists(INPUT_DIR)}")
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    folder_dict = get_image_files_by_folder(INPUT_DIR)
    total_images = sum(len(files) for files in folder_dict.values())
    print(f"총 {len(folder_dict)}개 폴더, {total_images}장 이미지 발견")
    total_filtered = 0
    for folder, image_files in folder_dict.items():
        print(f"\n=== 폴더: {folder} ({len(image_files)}장) ===")
        if len(image_files) > 0:
            print(f"  첫 번째 이미지: {image_files[0]}")
            print(f"  마지막 이미지: {image_files[-1]}")
        filtered = filter_similar_images(image_files, SIMILARITY_THRESHOLD, KEEP_OPTION)
        print(f"[3/3] 결과 복사 시작: {len(filtered)}장 남김 ...")
        for idx, f in enumerate(filtered):
            rel = os.path.relpath(f, INPUT_DIR)
            out_path = os.path.join(OUTPUT_DIR, rel)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            shutil.copy2(f, out_path)
            if (idx+1) % 50 == 0 or idx == len(filtered)-1:
                print(f"  복사 진행률: {idx+1}/{len(filtered)}")
        total_filtered += len(filtered)
    print(f"\n필터링 완료: {total_filtered}/{total_images}장 남김. 결과는 {OUTPUT_DIR}에 저장됨.")

if __name__ == "__main__":
    main()
