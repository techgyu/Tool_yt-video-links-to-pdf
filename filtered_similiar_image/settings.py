# settings.py
# 유사 이미지 필터링 기준 및 동작 옵션을 이 파일에서 관리하세요.

INPUT_DIR = "02_frames_output"  # 원본 이미지 폴더(하위 폴더 포함)
OUTPUT_DIR = "03_output_filtered_images"  # 필터링된 이미지 저장 폴더
SIMILARITY_THRESHOLD = 0.91  # 허용되는 이미지 해밍 거리(0~255, 낮을수록 엄격)
KEEP_OPTION = "last"  # 'first', 'middle', 'last' 중 하나 선택
IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.bmp')
