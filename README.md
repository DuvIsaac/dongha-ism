<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
</p>

# 충북과학고등학교 사름제 인생네컷 부스

## 주요 코드 및 파일/폴더 설명
### 2022년도 충곽하컷 부스
main : ./main_v2.py   
ui : ./page_ui_v2   
frame : ./frame   
ui 속 이미지 : ./img/pages_v2   
최종 저장 : ./result

### 2023년도 동하이즘 부스
main : ./main_v3.py   
ui : ./page_ui_v3   
frame : ./frame_v2 (2frame : 2컷 사진 프레임, 4frame : 4컷 사진 프레임, frame_capture : 프레임별 사진 찍을 때 미리보기)   
ui 속 이미지 : ./img/pages_v4   
최종 저장 : ./result

### 부가 설명
main 코드를 보며 등장하는 여러 파일들은 알아서 이해하기  
main 코드 이외의 다른 코드는 테스트 코드임

## setup
### digiCamControl download [https://digicamcontrol.com/download]

### digiCamControl 열고 라이브로 띄우기, 실시간 화면 전체로 바꾸고 라이브 하나 더 띄우기 위치 조정하기 (실시간 화면 위치 + Capture 버튼 위치)
개선 필요

### digiCamControl 파일 저장 위치 확인

## 개선 해야하는 점
### 사진 촬영 방법 개선 
현 : digiCamControl 앱 열고 마우스 위치 조정 후 클릭으로 촬영   
개선 : 프로그램상에서 카메라의 정보 가져오기, 참고자료 [https://github.com/jtcass01/DigiCam] (참고용)

### 사진 선택화면에서 선택지 이미지 깨짐

### 프린트 시간이 다소 길어 회전이 빠르지 않음
대안 1 : 부스의 수 늘리기   
대안 2 : 더 좋은 프린터기   
대안 3 : ???
