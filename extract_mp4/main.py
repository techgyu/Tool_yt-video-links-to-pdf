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

def download_youtube_to_mp4(youtube_url, output_path, playlist_mode=False, quality="best"):
    if quality == "best":
        format_option = "bestvideo+bestaudio/best"
    else:
        format_option = "worst[ext=mp4]/worst"
    command = [
        "yt-dlp",
        "-f", format_option,
        "--merge-output-format", "mp4",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "--cookies", "cookies.txt",  # 크롬에서 추출한 cookies.txt 경로
        "-o", output_path,
        youtube_url
    ]
    if not playlist_mode:
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
            # Windows에서 안전한 파일명으로 저장 (특수문자 자동 처리)
            output_path = os.path.join(output_dir, "%(title).100s.%(ext)s")
            quality = "best"
            print(f"유튜브 다운로드 중 (최고화질): {url}")
            try:
                download_youtube_to_mp4(url, output_path, playlist_mode=False, quality=quality)
                print(f"성공: {url}")
            except subprocess.CalledProcessError as e:
                print(f"다운로드 실패: {url} -> 오류 코드: {e.returncode}")
                # 대안 포맷으로 재시도
                try:
                    print(f"대안 포맷으로 재시도: {url}")
                    fallback_command = [
                        "yt-dlp",
                        "-f", "worst[ext=mp4]/worst",
                        "-o", output_path,
                        "--no-playlist",
                        url
                    ]
                    subprocess.run(fallback_command, check=True)
                    print(f"대안 포맷으로 성공: {url}")
                except Exception as fallback_error:
                    print(f"완전 실패: {url} -> {fallback_error}")
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

    # 순차 처리로 변경하여 파일 충돌 방지
    for idx, url in enumerate(URLS, 1):
        process((idx, url))

if __name__ == "__main__":
    main()