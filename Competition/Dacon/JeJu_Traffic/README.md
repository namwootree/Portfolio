# DACON 제주도 도로 교통량 예측 AI 경진대회 [(Link)](https://dacon.io/competitions/official/235985/leaderboard)

---

## 대회 소개

### 목표

* 제주도의 교통 정보로부터 도로 교통량 (평균 속도) 회귀 예측
* 제주도 도로 교통량 예측 AI 알고리즘 개발

### 참여 기간

* 2022.10.03 ~ 2022.11.14

### 참여자

* 권남우 [(Git Hub)](https://github.com/namwootree)
  - 대회 총괄 
  - 데이터 전처리 및 시각화
  - 모델링
  
* 정동한 [(Git Hub)](https://github.com/HansJeoung)
  - 데이터 전처리

### 사용한 Tool

* Python
* Pandas / Numpy / Pytimekr / Scikit - Learn / Matplotlib / Seaborn / Catboost / Optuna
* Tensor Flow
* Colab / Visual Studio Code

### 결과

* PRIVATE 3.15579
* 총 712개의 팀 중 68등 (상위 10% 이내)
* [EDA] Column의 Value별 Target 분포 (Histogram & Box Plot) 코드 공유 [(DACON)](https://dacon.io/competitions/official/235985/codeshare/6794?page=1&dtype=recent)

---

## 데이터셋 소개

### Data Info

* 각각의 칼럼에 대한 설명
* Features 
  * 아이디 / 날짜 / 요일 / 시간대 / 차로 수 / 도로 등급 / 중용구간 여부 / 연결로 코드 / 최고 속도 제한 / 통과 제한 하중 / 통과 제한 높이 / 도로 유형 / 시작 지점 위도 / 시작 지점 경도 / 도착 지점 위도 / 도착 지점 경도 / 시작 지점 회전 제한 여부 / 도착 지점 회전 제힌 여부 / 도로 명 / 시작 지점 명 / 도작 지점 명 / 통과 제한 차량
* Target
  * 평균 속도 (KM)

### Train Set

* Rows : 4,701,217 개
* Columns : 24 개
  * float64 : 9 개
  * int64 : 8 개
  * object : 7개

### Test Set

* Rows : 291,241 개
* Columns : 23 개
  * float64 : 8 개
  * int64 : 8 개
  * object : 7개
  
---

## 프로세스

**1. EDA** [(Link)](https://github.com/namwootree/Portfolio/blob/main/Competition/Dacon/JeJu_Traffic/Visualization_Data_Set.ipynb)

  * 불균형한 칼럼이 있음을 확인
  * 칼럼의 Value 별 Target 분포(최대값, 최소값, 최빈값)가 크게 달라지는 칼럼이 있음을 확인
  * 도로명이 '-'으로 Null 값이 존재함을 확인
  * 동일한 도로라도 요일 및 시간대에 따라 Target 값이 변하는 것을 확인
  
**2. Preprocessing Data Set** [(Link)](https://github.com/namwootree/Portfolio/blob/main/Competition/Dacon/JeJu_Traffic/Preprocessing.ipynb)

  * 다양한 전처리 시도를 통해 예측 결과가 좋았던 3가지의 전처리된 데이터 셋을 최종 사용
  
    * 대부분의 칼럼들이 카테고리 형식을 가지기에 숫자형인 데이터를 범주형으로 변경
    * 범주형 데이터끼리 결헙하여 파생 변수 생성
    * base_hour 칼럼을 범주형(카테고리)으로 변형한 파생 변수 생성
    * 기존 변수 유사한 데이터를 가진 파생 변수 추가 생성
    * 주말, 성수기, 공휴일 여부를 나타내는 파생 변수 생성
    * 도로명이 '-'인 데이터를 출발 도로명 및 도착 도로명으로 변경
    * 불필요한 변수 제거

**3. Modeling** [(Link)](https://github.com/namwootree/Portfolio/blob/main/Competition/Dacon/JeJu_Traffic/Catboost.ipynb)

  * CatBoostRegressor 모델 사용
  * 칼럼 수의 증가 (데이터 복잡도 증가)에 따른 하이퍼 파라미터 depth 증가 (모델 복잡도 증가)
  * 교차 검증 활용
  * 앙상블
  
**추가 시도 사항** (최종 결과 도출에는 비사용)
  * Optuna 활용 [(Link)](https://github.com/namwootree/Portfolio/blob/main/Competition/Dacon/JeJu_Traffic/Optuna.ipynb)
  * LGBM Regressor 및 neural network Model 사용 [LGBM](https://github.com/namwootree/Portfolio/blob/main/Competition/Dacon/JeJu_Traffic/LGBM.ipynb) / [Neural Network](https://github.com/namwootree/Portfolio/blob/main/Competition/Dacon/JeJu_Traffic/TF_Neural_Network.ipynb)
  * 다양한 하이퍼 파라미터 수정 시도 (depth, learning rate, features weight)
  * 다양한 KFold K 변경
  * CV 기반의 스태킹 앙상블 [{Link}](https://github.com/namwootree/Portfolio/blob/main/Competition/Dacon/JeJu_Traffic/CV_Stacking.ipynb)
    * Meta Model : LinearSVR 및 Logistic Regression [(Link)](https://github.com/namwootree/Portfolio/blob/main/Competition/Dacon/JeJu_Traffic/meta_model.ipynb)

---

## 느낀 점

### 머선러닝 엔지니어링 기본 이론에 집중

* **데이터 복잡도에 따라 필요한 머신러닝 엔지니어링**

  * ***데이터 복잡도에 맞는 모델 복잡도***
  
    - CatBoost 모델의 경우 별도의 하이퍼 파라미터 설정 없이 좋은 성능을 내는 것으로 알려져있다 [(Link)](https://catboost.ai/)
    
    - 그러나 Train Set의 예측 결과 보다 Vaild Set의 결과가 좋은 현상이 발생
    
    - depth 수를 최대값이 16으로 변경한 결과, 문제를 해결할 수 있었으며 Test Set에 대한 결과 또한 좋아짐
  
  * ***차원의 저주***
  
    - 파생 변수를 생성한 결과, 차원의 수가 2배 가까이 증가하게 되었다.
    
    - KFold를 수행함에 있어 K값을 5를 주는 것보다 7 혹은 10을 주어 Train Set의 사이즈를 키운 것이 성능 향상에 도움이 됨
    
    - Feature Importance를 확인하여 불필요한 변수를 제거한 결과, 차원의 수가 줄어들어 성능 향상에 도움이 됨
  
* **과소적합과 과대적합**

  * ***과소적합 문제 해결***
  
    - 모델의 복잡도를 증가시킨 결과, 문제 해결에 도움이 됨
    
    - 동일한 value를 가진 파생 변수들을 생성하여 성능 향상 시킴
    
    - 불균형 value를 가진 변수들을 결합하여 파생변수를 생성
    
    - 외부 데이터를 가져와 공휴일, 성수기, 주말 여부 등의 변수를 가져왔지만 성능이 낮아짐. 실제로 Feature Importance가 낮은 것을 확인함. 그러나 Feature Importance가 낮은 변수들 끼리 결합하여 여러 파생변수를 생성한 결과 성능 향상에 도움이 됨

    - CV 기반의 스테킹 앙상블 통하여 성능을 향상시킬 수 있었음
  
  * ***과대적합 문제 해결***
    
    - 모델의 depth를 최대값인 16이 아닌 14 혹은 12로 줄인 결과 과적합 문제를 개선할 수 있었음

    - 서로 다르게 전처리된 데이터 셋을 학습시킨 모델을 앙상블한 결과 과적합 문제를 개선할 수 있었음

    - 동일하게 전처리된 데이터 셋이라도 KFold의 K 값을 다르게 준 모델의 결과를 앙상블한 결과 과적합 문제를 개선할 수 

### 다양한 시도의 필요성

  * 파라미터 수정

    - CatBoost의 L2 규제 값을 높여으면 일반화에 도움이 될 것으로 에상
    - CV 기반의 스테킹 앙상블의 Meta Model인 LinearSVR의 epsilon 및 C의 하이퍼 파라미터 값을 수정하였으면 성능 향상에 도움이 될 것으로 예상

  * **파생변수 생성**

    - 2022년 8월 이전 데이터만 사용할 수 있기에 외부 데이터를 어떻게 사용해야 하는 지 충분히 숙지하지 못함
        
        * 날짜 별 날씨, 월별 제주도 방문자 수, 렌터카 관련 정보 등등을 활용하지 못함
    
    - K-Modes Algorithm을 통해 범주형 데이터를 클러스터링 하려 시도하엿느나 각 변수의 Unique한 값이 많기에 시간이 너무 오래 거려 활용하지 못함

  * **CatBoost외에 LGBM 및 Neural Network 활용**

    - CatBoost의 학습 속도가 빠르며 범주형 데이터에 우수한 성능한 성능을 보이기에 최종 결과 예측에 CatBoost 모델만 사용

    - LGBM 및 Neural Network를 학습하여 성능을 확인하였으며 CatBoost의 성능에 크게 못미치는 것을 확인하여 비사용하게 됨

    - 그러나 상위권의 코드를 확인한 결과, 다양한 모델을 시도한 것을 확인

    - 시간 및 하드웨어 자원이 충분하다면 LGBM 및 Neural Network의 최적의 성능을 낼 수 있는 하이퍼 파라미터를 찾는 것을 다음에는 시도하기로 다짐함
  
  * **Optuna**

    - Optuna를 통해 Catboost의 최적의 파라미터를 찾으려고 시도

    - 그러나 최적의 파라미터를 찾기 위해서는 많은 시간이 소요됨

    - 상대적으로 작은 시간을 통해 찾은 파라미터를 모델에 적용하였으나 성능이 크게 낮음

    - 다음에는 Optuna를 제대로 사용할 수 있기를 기대함
  

### 상위권의 코드 공유를 통한 피드백

  - **비슷하게 전처리를 시도한 경우도 있었으나 새로운 전처리 시도가 많았음**

    * 변수 별 Target 분포 값 (평균 및 표준편차)을 파생 변수로 생성

    * 최고 기온 월별 평균값, 무인 교통 단속 카메라, 전국초중등학교 기본 정보, 어린이 보호 구역, 주차장 정보, 제주 공항으로부터 거리 등의 외부 데이터 활용

  - **다양한 모델의 예측값을 앙상블** 

    * 자체 제작   Neural Network, XGBoost, LGBM 모델 등 다양한 모델 앙상블

    * Optuna 및 GridSearchCV를 통한 최적의 파라미터 찾음
