from PIL import Image, ImageWin, ImageOps
import win32ui
import win32print

def print_rotated_image(file_path, printer_name, num):
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
        
        for _ in range(num):
                hdc.StartDoc('Print Job')
                hdc.StartPage()
                dib = ImageWin.Dib(rotated_image)
                dib.draw(hdc.GetHandleOutput(), (0, 0, rotated_image.size[0], rotated_image.size[1]))
                hdc.EndPage()
                hdc.EndDoc()
            
        hdc.DeleteDC()
        win32print.ClosePrinter(printer)
    
    except Exception as e:
        print("에러 발생:", e)

# 파일 경로와 프린터 이름 지정
printer_name = "Canon SELPHY CP1300"

# 함수 호출
print_rotated_image("./frame_v2/2frame/9.png", printer_name, 1)
