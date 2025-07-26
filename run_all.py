import os
import shutil
import subprocess
import sys

def run_subprocess(pyfile, cwd):
    print(f"실행: {pyfile}")
    result = subprocess.run([sys.executable, pyfile], cwd=cwd)
    if result.returncode != 0:
        print(f"실패: {pyfile}")
        sys.exit(1)

def copytree_force(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))

    # 1. mp4 다운로드
    run_subprocess(os.path.join("extract_mp4", "main.py"), root)

    # 2. mp4 결과 복사 → 프레임 추출 입력
    src1 = os.path.join(root, "extract_mp4", "output_videos")
    dst1 = os.path.join(root, "extract_frames", "input_videos")
    copytree_force(src1, dst1)

    # 3. 프레임 추출
    run_subprocess(os.path.join("extract_frames", "main.py"), root)

    # 4. 프레임 결과 복사 → 유사 이미지 필터 입력
    src2 = os.path.join(root, "extract_frames", "frames_output")
    dst2 = os.path.join(root, "filtered_similiar_image", "input_images")
    copytree_force(src2, dst2)

    # 5. 유사 이미지 필터링
    run_subprocess(os.path.join("filtered_similiar_image", "main.py"), root)

    # 6. 필터링 결과 복사 → PDF 변환 입력
    src3 = os.path.join(root, "filtered_similiar_image", "output_filtered_images")
    dst3 = os.path.join(root, "pdf_from_images", "input_images")
    copytree_force(src3, dst3)

    # 7. PDF 변환
    run_subprocess(os.path.join("pdf_from_images", "main.py"), root)

    print("모든 작업이 완료되었습니다.")
