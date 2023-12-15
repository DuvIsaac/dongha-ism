from PIL import Image, ImageWin, ImageOps
import win32ui
import win32print

def print_rotated_image_multiple_times(file_path, printer_name, num_copies):
    try:
        # 이미지 열기
        image = Image.open(file_path)

        # 이미지 90도 회전
        rotated_image = image.rotate(90, expand=True)
        
        move_left = 40
        move_up = 38
        rotated_image = ImageOps.expand(rotated_image, border=(move_left, move_up, 0, 0), fill='white')

        # 프린터에 이미지 출력
        printer = win32print.OpenPrinter(printer_name)
        hprinter = win32print.GetPrinter(printer, 2)['pPrinterName']
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        
        for _ in range(num_copies):  # 지정된 횟수만큼 이미지 반복 출력
            hdc.StartDoc('Print Job')
            hdc.StartPage()
            dib = ImageWin.Dib(rotated_image)
            dib.draw(hdc.GetHandleOutput(), (0, 0, rotated_image.size[0], rotated_image.size[1]))  # 이미지 출력
            hdc.EndPage()
            hdc.EndDoc()

        hdc.DeleteDC()
        win32print.ClosePrinter(printer)
    
    except Exception as e:
        print("에러 발생:", e)

# 파일 경로와 프린터 이름, 복사 횟수 지정
file_path = "./test_img/res23.jpg"
printer_name = "Canon SELPHY CP1300"
num_copies = 5  # 출력할 횟수

# 함수 호출
print_rotated_image_multiple_times(file_path, printer_name, num_copies)