import cv2

image = cv2.imread('C:/digiCamControl/Session1/DSC_0001.jpg')

# 원하는 비율
target_ratio = 92 / 64
# 4컷
# target_ratio = 45 / 64 

# 이미지 크기 가져오기
height, width, _ = image.shape

# 이미지를 원하는 비율로 자르기
current_ratio = width / height

if current_ratio > target_ratio:
    # 이미지의 가로가 더 길 경우, 가로를 자름
    new_width = int(height * target_ratio)
    start_x = (width - new_width) // 2
    cropped_image = image[:, start_x:start_x + new_width]
else:
    # 이미지의 세로가 더 길거나 비율이 같을 경우, 세로를 자름
    new_height = int(width / target_ratio)
    start_y = (height - new_height) // 2
    cropped_image = image[start_y:start_y + new_height, :]
    
cv2.imwrite('./test_img/cut1.jpg', cropped_image)