import cv2
import numpy as np

# # 첫 번째 이미지 읽기
# img1 = cv2.imread("C:\digiCamControl\Session1\DSC_0020.jpg")  # 이미지 경로에 맞게 수정

# # 두 번째 이미지 읽기
# img2 = cv2.imread("C:\digiCamControl\Session1\DSC_0021.jpg")  # 이미지 경로에 맞게 수정

img1 = cv2.imread('./frame/8.png', cv2.IMREAD_UNCHANGED)
img2 = cv2.imread('./frame/9.png', cv2.IMREAD_UNCHANGED)

#############################################################################

# # 이미지 크기 조정 (같은 크기로 조정)
# width = max(img1.shape[1], img2.shape[1])
# height = max(img1.shape[0], img2.shape[0])

# resized_img1 = cv2.resize(img1, (width, height))
# resized_img2 = cv2.resize(img2, (width, height))

# # 하얀 배경 생성
# white_background = np.zeros((height, width, 3), dtype=np.uint8)
# white_background.fill(255)  # 하얀색 배경으로 채우기

# # 첫 번째 이미지와 두 번째 이미지를 하얀 배경 위에 합치기
# combined_image = cv2.addWeighted(white_background, 1, resized_img1, 1, 0)
# combined_image = cv2.addWeighted(combined_image, 1, resized_img2, 1, 0)

#############################################################################

# # 이미지 크기 맞추기
# width = max(img1.shape[1], img2.shape[1])
# height = max(img1.shape[0], img2.shape[0])

# resized_img1 = cv2.resize(img1, (width, height))
# resized_img2 = cv2.resize(img2, (width, height))

# # 두 이미지 합치기
# combined_image = cv2.add(resized_img1, resized_img2)

#############################################################################

# 이미지 크기 맞추기 (가로 크기 동일하게)
width = max(img1.shape[1], img2.shape[1])
resized_img1 = cv2.resize(img1, (width, img1.shape[0]))
resized_img2 = cv2.resize(img2, (width, img2.shape[0]))

# 두 이미지 위아래로 합치기
combined_image = cv2.vconcat([resized_img1, resized_img2])

#############################################################################

# 합쳐진 이미지 저장
cv2.imwrite(f'./test_img/test_5.png', combined_image)