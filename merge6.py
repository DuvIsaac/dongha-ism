import cv2

def cut(file_path):
        image = cv2.imread(file_path)
        
        image = cv2.resize(image, (2736, 1824))
        
        print(image.shape)
        
        target_ratio = 45 / 64 

        height, width, _ = image.shape
        current_ratio = width / height

        if current_ratio > target_ratio:
            new_width = int(height * target_ratio)
            start_x = (width - new_width) // 2
            cropped_image = image[:, start_x:start_x + new_width]
        else:
            new_height = int(width / target_ratio)
            start_y = (height - new_height) // 2
            cropped_image = image[start_y:start_y + new_height, :]
            
        return cropped_image

def mergeImg(frame_path, file_path_1, file_path_2, file_path_3, file_path_4):
        main_image = cv2.imread('./white.png', cv2.IMREAD_COLOR)
        if file_path_1 == 0:
            file_path_1 = './white_5.png'
        if file_path_2 == 0:
            file_path_2 = './white_5.png'
        if file_path_3 == 0:
            file_path_3 = './white_5.png'
        if file_path_4 == 0:
            file_path_4 = './white_5.png'
        insert_image_1 = cut(file_path_1)
        insert_image_2 = cut(file_path_2)
        insert_image_3 = cut(file_path_3)
        insert_image_4 = cut(file_path_4)

        frame = cv2.imread(frame_path, cv2.IMREAD_COLOR)

        mask = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
        mask = mask[:, :, 3]
        mask = cv2.bitwise_not(mask)

        m = 0.415
        insert_image_1 = cv2.resize(insert_image_1, None, None, m, m, cv2.INTER_CUBIC)
        # insert_image_2 = cv2.resize(insert_image_2, None, None, m, m, cv2.INTER_CUBIC)
        # insert_image_3 = cv2.resize(insert_image_3, None, None, m, m, cv2.INTER_CUBIC)
        # insert_image_4 = cv2.resize(insert_image_4, None, None, m, m, cv2.INTER_CUBIC)

        x_1 = 47
        y_1 = 165

        x_2 = 47
        y_2 = 944
        
        x_3 = 602
        y_3 = 165
        
        x_4 = 602
        y_4 = 944

        insert_height, insert_width, _ = insert_image_1.shape

        main_image[y_1:y_1 + insert_height, x_1:x_1 + insert_width] = insert_image_1
        # main_image[y_2:y_2 + insert_height, x_2:x_2 + insert_width] = insert_image_2
        # main_image[y_3:y_3 + insert_height, x_3:x_3 + insert_width] = insert_image_3
        # main_image[y_4:y_4 + insert_height, x_4:x_4 + insert_width] = insert_image_4

        cv2.copyTo(main_image, mask, frame)
        
        return frame
    
res = mergeImg('./frame_v2/4frame/3.png', "C:\digiCamControl\Session1\DSC_0208.jpg", 0, 0, 0)
cv2.imwrite('./test_img/res33.jpg', res)
# cv2.imshow(res)