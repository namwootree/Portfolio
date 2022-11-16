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

**1. EDA**

  * 불균형한 칼럼이 있음을 확인
  * 칼럼의 Value 별 Target 분포(최대값, 최소값, 최빈값)가 크게 달라지는 칼럼이 있음을 확인
  * 도로명이 '-'으로 Null 값이 존재함을 확인
  * 동일한 도로라도 요일 및 시간대에 따라 Target 값이 변하는 것을 확인
  
**2. Preprocessing Data Set**

  * 다양한 전처리 시도를 통해 예측 결과가 좋았던 3가지의 전처리된 데이터 셋을 최종 사용
  
    * 대부분의 칼럼들이 카테고리 형식을 가지기에 숫자형인 데이터를 범주형으로 변경
    * 범주형 데이터끼리 결헙하여 파생 변수 생성
    * base_hour 칼럼을 범주형(카테고리)으로 변형한 파생 변수 생성
    * 기존 변수 유사한 데이터를 가진 파생 변수 추가 생성
    * 주말, 성수기, 공휴일 여부를 나타내는 파생 변수 생성
    * 도로명이 '-'인 데이터를 출발 도로명 및 도착 도로명으로 변경
    * 불필요한 변수 제거

**3. Modeling**

  * CatBoostRegressor 모델 사용
  * 칼럼 수의 증가 (데이터 복잡도 증가)에 따른 하이퍼 파라미터 depth 증가 (모델 복잡도 증가)
  * 교차 검증 활용
  * 앙상블
  
**추가 시도 사항** (최종 결과 도출에는 비사용)
  * Optuna 활용
  * LGBM Regressor 및 neural network Model 사용
  * 다양한 하이퍼 파라미터 수정 시도 (depth, learning rate, features weight)
  * 다양한 KFold K 변경
  * CV 기반의 스태킹 앙상블
    * Meta Model : LinearSVR 및 Logistic Regression

---

## 느낀 점

### 머선러닝 엔지니어링 기본 이론에 집중

* **데이터 복잡도에 따라 필요한 머신러닝 엔지니어링**

  * 데이터 복잡도에 맞는 모델 복잡도
  
    - CatBoost 모델의 경우 별도의 하이퍼 파라미터 설정 없이 좋은 성능을 내는 것으로 알려져있다 [(Link)](https://catboost.ai/)
    
    - 그러나 Train Set의 예측 결과 보다 Vaild Set의 결과가 좋은 현상이 발생
    
    - depth 수를 최대값이 16으로 변경한 결과, 문제를 해결할 수 있었으며 Test Set에 대한 결과 또한 좋아짐
  
  * 차원의 저주
  
    - 파생 변수를 생성한 결과, 차원의 수가 2배 가까이 증가하게 되었다.
    
    - KFold를 수행함에 있어 K값을 5를 주는 것보다 7 혹은 10을 주어 Train Set의 사이즈를 키운 것이 성능 향상에 도움이 됨
    
    - Feature Importance를 확인하여 불필요한 변수를 제거한 결과, 차원의 수가 줄어들어 성능 향상에 도움이 됨
  
* **과소적합과 과대적합**

  * 과소적합 문제 해결
  
    - 모델의 복잡도를 증가시킨 결과, 문제 해결에 도움이 됨
    
    - 동일한 value를 가진 파생 변수들을 생성하여 성능 향상 시킴
    
    - 불균형 value를 가진 변수들을 결합하여 파생변수를 생성
    
    - 외부 데이터를 가져와 공휴일, 성수기, 주말 여부 등의 변수를 가져왔지만 성능이 낮아짐. 실제로 
  
  * 과대적합 문제 해결


### 다양한 시도의 필요성

  * **CatBoost외에 LGBM / RandomForest / Neural Network 활용**
  
  * **Optuna**
  
  * **파생변수 생성**


### 상위권의 코드 공유를 통한 피드백



