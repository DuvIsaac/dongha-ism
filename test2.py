from PIL import Image
import cv2

# 이미지 크기 설정
height, width, _ = cv2.imread('./frame_v2/frame_capture/3_1.png').shape

print(height)
print(width)

# 투명 배경 이미지 생성
transparent_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # 알파 채널 값 (0, 0, 0, 0)은 완전히 투명한 값을 의미합니다.

# 이미지 저장
transparent_image.save('./no.png')  # 이미지 파일로 저장하거나,
transparent_image.show()  # 이미지를 보여줄 수 있습니다.