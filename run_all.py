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

    # 1. extract_mp4/main.py
    run_subprocess(os.path.join("extract_mp4", "main.py"), root)

    # 2. extract_mp4/output_videos -> extract_frames/input_videos
    src1 = os.path.join(root, "extract_mp4", "output_videos")
    dst1 = os.path.join(root, "extract_frames", "input_videos")
    copytree_force(src1, dst1)

    # 3. extract_frames/main.py
    run_subprocess(os.path.join("extract_frames", "main.py"), root)

    # 4. extract_frames/frames_output -> pdf_from_images/input_images
    src2 = os.path.join(root, "extract_frames", "frames_output")
    dst2 = os.path.join(root, "pdf_from_images", "input_images")
    copytree_force(src2, dst2)

    # 5. pdf_from_images/main.py
    run_subprocess(os.path.join("pdf_from_images", "main.py"), root)

    print("모든 작업이 완료되었습니다.")
