import os
import subprocess
import sys
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from settings import INPUT_DIR, OUTPUT_DIR, FRAME_INTERVAL

def extract_frames_from_mp4(mp4_path, output_dir, interval):
    basename = os.path.splitext(os.path.basename(mp4_path))[0]
    save_dir = os.path.join(output_dir, basename)
    os.makedirs(save_dir, exist_ok=True)
    # ffmpeg 명령어: 지정한 간격마다 프레임 추출
    # 예: frame_%04d.jpg
    command = [
        "ffmpeg",
        "-i", mp4_path,
        "-vf", f"fps=1/{interval}",
        os.path.join(save_dir, "frame_%04d.jpg")
    ]
    subprocess.run(command, check=True)

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"입력 폴더가 존재하지 않습니다: {INPUT_DIR}")
        return
    # OUTPUT_DIR 비우기
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    mp4_files = []
    for root, dirs, files in os.walk(INPUT_DIR):
        for f in files:
            if f.lower().endswith('.mp4'):
                mp4_files.append(os.path.join(root, f))
    if not mp4_files:
        print(f"{INPUT_DIR} 및 하위 폴더에 mp4 파일이 없습니다.")
        return
    for mp4_path in mp4_files:
        print(f"프레임 추출 중: {mp4_path}")
        try:
            extract_frames_from_mp4(mp4_path, OUTPUT_DIR, FRAME_INTERVAL)
        except Exception as e:
            print(f"실패: {mp4_path} -> {e}")

if __name__ == "__main__":
    main()
