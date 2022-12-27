# Kaggle Scrabble Player Rating [(Link)](https://www.kaggle.com/c/scrabble-player-rating)

## Scrabble Game Rule

[You Tube : 공식 게임 규칙 소개 영샹](https://www.youtube.com/watch?v=RYeXv1vmLGM)<br>
[WIKIPEDIA : 위키백과 설명 글](https://en.wikipedia.org/wiki/Scrabble)<br>
[온라인 게임 체험](https://playscrabble.com/)

* 원하는 만큼 타일을 사용하여 단어 하나를 중앙에 배치

* 각 타일에는 점수가 적혀있음 + 보너스 칸을 통과하여 단어를 배치한 경우 배로 점수를 얻음

* 단어를 만드는 방법

  - 이미 있는 단어의 앞이나 뒤, 양쪽 모두
  - 이미 있는 단어와 직각이 되도록
  - 이미 있는 단어와 평행하게
  - 새 단어가 이미 있는 단어에 글자를 추가
  
* 타일을 통해 단어를 만들기 어려울 경우, 원하는 만큼 타일을 버리고 (주머니에 다시 넣음) 새로 뽑을 수 있음

* 주머니에 글자 타일이 다 떨어지면 이후에는 타일을 보충하지 않고 진행

* 게임 종료

  - 주머니 빈 상태에서 타일을 다 사용한 사람이 생김
  - 더 이상 아무도 단어를 놓을 수 없음
  - 두바뀌 연속 모두 패스 시

* 각자의 점수에 남은 타일 수 만큼 감점 / 총 감점 만큼 게임 끝낸 사람은 추가 점수를 얻음

---

## 대회 소개
---

### 목표

* 플레이어의 Scrabble Game 데이터를 활용하여 랭킹 예측
* RMSE가 가장 적은 회귀 예측 알고리즘 개발

### 참여 기간

### 참여자

* 권남우 [(Git Hub)](https://github.com/namwootree)
  - 대회 총괄 
  - 데이터 전처리 및 시각화
  - 모델링

### 사용한 Tool

* Python
* Pandas / Numpy / Scikit - Learn / XGBoost / LigthGBM / Catboost / Matplotlib / Optuna / Seaborn
* Colab

### 결과

* PRIVATE 100.34660 (RMSE)
* 총 301개의 팀 중 20등 

---

## [데이터 소개](https://www.kaggle.com/competitions/scrabble-player-rating/data)

### Train

* 각각의 플레이어의 최종 점수와 게임하기 이전의 순위에관 학습 데이터 셋

### Games

* 게임에 관한 데이터

* game_id / first / time_control_name / winner / created_at / lexicon / initial_time_seconds / increment_seconds / rating_mode / max_overtime_minutes / game_duration_seconds

### Turns

* 게임의 시작과 끝까지 동안 발생한 턴 내에서 발생한 내용들

* game_id / turn_number / nickname / rack / location / move / points / score / turn_type


### Test

* 각각의 플레이어의 최종 점수와 게임하기 이전의 순위에관 추론 데이터 셋

---

## 프로세스

### Reference

* [Full Walkthrough (EDA + FE + Model Tuning)](https://www.kaggle.com/code/ijcrook/full-walkthrough-eda-fe-model-tuning) 

1. [DDA & EDA](https://github.com/namwootree/Portfolio/blob/main/Competition/Kaggle/Scrabble%20Player%20Rating/DDA_%26_EDA.ipynb)
   -  Target (rating)에 관한 분포를 히스토그램으로 확인한 결과 1500등한 데이터 갯수가 유독 많은 것을 확인함
   
   -  사용자의 닉네임을 검토한 결과, 닉네임 뒤에 Bot이라고 끝난 실제 유저가 아닌 Bot이 4명 있음을 확인함
   
   - 사용자별로 게임을 플레이한 횟수를 확인한 결과, 가장 많이 한 게임 횟수는 6576번 이었으며 평균 게임 횟수는 약 49번, 중위값은 8이였다. 
   
   - Bot이 플레이한 게임의 데이터와 실제 사람이 플레이한 게임을 'game_id'를 기준으로 Merge한 결과 각각의 휴면 플레이어들은 Bot과 대결하였음을 알 수 있었다.
   
   - 그리고 'Master Bot'은 실제 휴면과 게임을 하지않고 Bot끼리 게임한 것을 알 수 있었다.
   
   - 일부 휴먼 플레이어를 샘플로 뽑아 상대한 Bot별로 점수를 확인한 결과, 상대한 Bot별로 점수 편차가 차이가 남을 확인할 수 있었다
   
   - 그리고 플레이한 시간에 따라 상대할 Bot이 달라짐을 확인할 수 있었다
   
   - 유저별 점수 및 우승 비율별 랭킹이 유의미한 상관관계가 있음을 확인할 수 있었다
   
   
2. Preprocessing
  
  * #### Turn
  
    - 점수에 영향을 줄 수 있는 남은 타일 개수를 파생변수로 생성
    - 남은 타일의 개수가 7개 미만 여부를 파생변수로 생성
    - 배치한 타일 개수를 파생변수로 생성
    - Dale–Chall readability formula 기준으로 어려운 단어 여부를 파생변수로 생성
    - 타일을 배치한 위치 정보를 X 및 Y축 기준으로 숫자로 변환
    - 'move' 칼럼에서 타일의 위치를 정보를 나타내지 않은 것의 개수를 파생변수로 생성
    - 여러 변수들의 통계값 (평균, 합계, 최대값)을 구하여 파생변수로 생성
    
  * #### Train & Test
  
    - Train과 Test 셋을 'game_id'와 'nickname'을 기준으로 병합
    - 유저와 상대한 Bot를 구분하고 'game_id'와 'nickname'을 기준으로 병합
    - 랭킹이 15000등인 데이터는 제외
  
  * #### create cumm player features_overall
  
    - 닉네임 별로 플레이 평균 점수, 우승 횟수, 우승 비율, 평균 경기 사간을 파생변수로 생성
    
  * #### create cumm player features bot
  
    - 닉네임과 상대한 Bot 별로 '플레이어'의 평균 점수, 우승 횟수, 우승 비율, 평균 경기 사간을 파생변수로 생성
    
  * #### create cumm player features lexicon
  
    - 사용한 어휘 사전 별로 평균 점수, 우승 횟수, 우승 비율, 평균 경기 사간을 파생변수로 생성
    
  * #### create cumm player game features
  
    - game 데이터 셋의 "bot_name", "rating_mode", "lexicon", "game_end_reason" 칼럼을 One Hot Encoding 한 후, 변수별 합계를 구함
    
  * #### create cumm bot features
  
    - 닉네임과 상대한 Bot 별로 Bot의 평균 점수와 평균 랭킹을 구함
    
  * #### create cumm turns features
  
    - turn 데이터 셋에서 파생된 변수들의 유저별 평균값을 생성
  
3. Modeling

  * Optuna를 활용하여 하이퍼파라미터 설정
  * Repeated KFold를 사용하여 일반화의 성능을 높이고자 함
  * LightGBM을 활용하여 추론

---

## 느낀 점

 ### 1. 데이터 셋 이해의 어려움
 
    - Sca
