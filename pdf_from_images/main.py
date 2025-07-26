import os
import sys
from PIL import Image
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import INPUT_DIR, OUTPUT_DIR

def images_to_pdf(image_paths, pdf_path):
    images = [Image.open(p).convert('RGB') for p in image_paths]
    if images:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"입력 폴더가 존재하지 않습니다: {INPUT_DIR}")
        return
    if os.path.exists(OUTPUT_DIR):
        for f in os.listdir(OUTPUT_DIR):
            os.remove(os.path.join(OUTPUT_DIR, f))
    else:
        os.makedirs(OUTPUT_DIR)

    # 하위 폴더가 없는 경우: INPUT_DIR의 이미지 전체를 하나의 PDF로
    has_subdir = any(os.path.isdir(os.path.join(INPUT_DIR, d)) for d in os.listdir(INPUT_DIR))
    image_exts = ('.jpg', '.jpeg', '.png', '.bmp')

    if not has_subdir:
        image_files = [os.path.join(INPUT_DIR, f) for f in sorted(os.listdir(INPUT_DIR)) if f.lower().endswith(image_exts)]
        if image_files:
            pdf_path = os.path.join(OUTPUT_DIR, 'output.pdf')
            print(f"PDF 생성: {pdf_path}")
            images_to_pdf(image_files, pdf_path)
        else:
            print(f"{INPUT_DIR}에 이미지 파일이 없습니다.")
        return

    # 하위 폴더가 있는 경우: 각 폴더별로 PDF 생성
    for folder in sorted(os.listdir(INPUT_DIR)):
        folder_path = os.path.join(INPUT_DIR, folder)
        if not os.path.isdir(folder_path):
            continue
        image_files = [os.path.join(folder_path, f) for f in sorted(os.listdir(folder_path)) if f.lower().endswith(image_exts)]
        if image_files:
            pdf_path = os.path.join(OUTPUT_DIR, f"{folder}.pdf")
            print(f"PDF 생성: {pdf_path}")
            images_to_pdf(image_files, pdf_path)
        else:
            print(f"{folder_path}에 이미지 파일이 없습니다.")

if __name__ == "__main__":
    main()
