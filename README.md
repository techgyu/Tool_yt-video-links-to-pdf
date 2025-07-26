# tool_yt-video-links-to-pdf

유튜브/스트리밍(m3u8) 영상 링크 → mp4 다운로드 → 프레임 추출 → PDF 변환까지 자동화하는 파이프라인 도구입니다.

## 주요 기능
- 유튜브(단일/재생목록) 및 m3u8 영상 다운로드 (extract_mp4)
- mp4 영상에서 프레임 이미지 추출 (extract_frames)
- 이미지들을 PDF로 변환 (pdf_from_images)
- `run_all.py`로 전체 자동 실행 및 중간 결과 폴더 자동 연결

## 폴더 구조
```
extract_mp4/         # 영상 다운로드 (main.py, settings.py)
extract_frames/      # 프레임 추출 (main.py, settings.py)
pdf_from_images/     # 이미지 → PDF (main.py, settings.py)
run_all.py           # 전체 자동 실행 스크립트
```

## 사용법
1. **extract_mp4/settings.py**
   - URLS: 다운로드할 영상 링크 리스트 (유튜브/재생목록/m3u8)
   - OUTPUT_DIR: mp4 저장 폴더명
   - SOURCE_TYPE: 'youtube' 또는 'm3u8'

2. **extract_frames/settings.py**
   - INPUT_DIR: mp4 파일이 들어있는 폴더명 (재귀적으로 순회)
   - OUTPUT_DIR: 프레임 이미지 저장 폴더명
   - FRAME_INTERVAL: 프레임 추출 간격(초)

3. **pdf_from_images/settings.py**
   - INPUT_DIR: 이미지가 들어있는 폴더(하위 폴더 포함)
   - OUTPUT_DIR: PDF 저장 폴더명

4. **전체 자동 실행**
   ```bash
   python run_all.py
   ```
   - 각 단계별 결과 폴더가 자동으로 연결/복사되어 전체 파이프라인이 한 번에 실행됩니다.

## 의존 패키지
- ffmpeg (시스템에 설치 필요)
    - [공식 다운로드 페이지](https://ffmpeg.org/download.html)에서 OS에 맞는 ffmpeg를 설치하세요.
    - Windows 사용자는 ffmpeg.exe를 받아 환경변수에 등록하거나, 실행 폴더에 두면 됩니다.
- yt-dlp (pip install yt-dlp)
- pillow (pip install pillow)

## 예시
- 유튜브 재생목록, m3u8 등 다양한 영상 소스를 지원하며, 프레임 추출 및 PDF 변환까지 자동화됩니다.

---

**문의/기여**: PR/이슈 환영합니다!