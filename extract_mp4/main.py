import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from settings import URLS, OUTPUT_DIR, SOURCE_TYPE

def download_m3u8_to_mp4(m3u8_url, output_path):
    command = [
        "ffmpeg",
        "-i", m3u8_url,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        output_path
    ]
    subprocess.run(command, check=True)

def download_youtube_to_mp4(youtube_url, output_path, playlist_mode=False):
    command = [
        "yt-dlp",
        "-f", "best[ext=mp4]/best",
        "-o", output_path,
        youtube_url
    ]
    if playlist_mode:
        # yt-dlp 기본값이 playlist 전체 다운로드이므로 별도 옵션 필요 없음
        pass
    else:
        command.append("--no-playlist")
    subprocess.run(command, check=True)

# 여러 링크를 settings.py에서 받아서 병렬 처리

def main():
    if not URLS or not isinstance(URLS, list):
        print("settings.py의 URLS 배열에 링크를 입력하세요.")
        sys.exit(1)

    output_dir = OUTPUT_DIR
    source_type = SOURCE_TYPE.lower()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    def process(args):
        idx, url = args
        if source_type == "youtube":
            output_path = os.path.join(output_dir, f"video_%(playlist_index)s.%(ext)s")
            print(f"유튜브(재생목록 포함) 다운로드 중: {url} -> {output_path}")
            try:
                download_youtube_to_mp4(url, output_path, playlist_mode=True)
            except Exception as e:
                print(f"실패: {url} -> {e}")
        else:
            output_path = os.path.join(output_dir, f"video_{idx}.mp4")
            print(f"다운로드 중: {url} -> {output_path}")
            try:
                if source_type == "m3u8":
                    download_m3u8_to_mp4(url, output_path)
                else:
                    print("지원하지 않는 source_type입니다. 'm3u8' 또는 'youtube' 중 하나를 입력하세요.")
                    sys.exit(1)
            except Exception as e:
                print(f"실패: {url} -> {e}")

    with ThreadPoolExecutor() as executor:
        executor.map(process, list(enumerate(URLS, 1)))

if __name__ == "__main__":
    main()