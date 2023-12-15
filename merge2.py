import cv2

img = cv2.imread('./test_img/test_4.jpg', cv2.IMREAD_COLOR)
mask = cv2.imread('./test_img/test_5.png', cv2.IMREAD_UNCHANGED)

# PNG 이미지를 JPEG 이미지와 동일한 크기로 조정
png_resized = cv2.resize(mask, (img.shape[1], img.shape[0]))

# PNG 이미지를 JPEG 이미지 위에 덮어쓰기 (알파 채널 적용)
result = img.copy()
result[0:png_resized.shape[0], 0:png_resized.shape[1]] = png_resized[:, :, :3] * (png_resized[:, :, 3:] / 255.0) + \
    img[0:png_resized.shape[0], 0:png_resized.shape[1]] * (1.0 - png_resized[:, :, 3:] / 255.0)

cv2.imwrite('./test_img/test_6.jpg', result)