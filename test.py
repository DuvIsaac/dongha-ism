import cv2

webcam = cv2.VideoCapture(1)
width = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(width, height)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

while webcam.isOpened():
    status, frame = webcam.read()

    if status:
        cv2.imshow("test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break

webcam.release()
cv2.destroyAllWindows()