# 폐렴 여부 및 위치 분석

### 주제
* 의학 분야에 AI기술을 접목시키는 사례가 증가하고 있다.
* 딥러닝을 통해 폐질환의 오진을 방지하고자 빠른 치료가 가능하도록 하고자 한다.

### 데이터
* Kaggle : RSNA Pneumonia Detection Challenge

*** 사용한 모델
* YOLO V3
* YOLO V4

*** 특이사항
1. Test Set의 라벨이 존재하지 않았다.


-> Train Set을 Train / Var / Test로 분할

2. YOLO 모델이 요구한 Boundary Box 양식과 주어진 데이터 셋의 양식 달랐다.


-> 양식에 맞게 좌표 값 및 Boundary Box 정보 수정하였다
