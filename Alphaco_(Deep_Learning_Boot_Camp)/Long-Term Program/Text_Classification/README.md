# 뉴스 토픽 분류 모델 개선 방안
* 목표 : 데이콘 경진 대회 수상작 모델을 개선하여 더 나은 성능을 개시

### [Main]_StandardKFold_(5)_Ensemble_(3)
* 증식한 데이터를 Stratified K Fold (5)를 적용
* klue/roberta-base, bert-base-multilingual-uncased, xlm-roberta-base 모델을 사용하여 Soft Voting 적용
* 빠른 전이 학습을 위해 Colab의 TPU 사용

### Reference_1
* 데이콘 리더보드 : [Private 2nd] Huggingface를 사용한 베이스라인
* 참조한 내용 : KFold, 사용한 모델, Ensemble

### Reference_2
* 데이콘 리더보드: 최종 3th : [Private 5위 - 0.83705 / Back Translation]
* 참조한 내용 : Back Translation 및 Preprocessing

### original_data_visualization
* 기본적인 데이터 분석을 위해 시각화를 진행
* 라벨 별 데이터 분포 확인
* 라벨 별 문장 길이 확인 (최단/최장/최빈)
* 워드 클라우드를 통해 라벨 별 주요 단어 확인

### Comparing_Translation_Performence
* Back Translation 하기 위해 다양한 방법론을 비교 분석
* papago 및 bing을 이용하는 것이 성능 측면에서 가장 좋았다
* 그러나 일일 사용량 제한 및 서버 연결 안정성을 고려하여 M2M100 모델을 최종 선택

### [M2M100]Text_Data_Augmention
* M2M100 모델을 사용하여 원본 데이터를 한글 - 한글 번역하였다

### preprocessing_Aug_Data
* 증식한 데이터 셋에서 이상치가 다수 존재하여 정재함
* 그럼에도 극 소수의 이상치가 존재
* 뉴스에서 주로 사용하는 문제와 비슷하게 만들기 위해 일부 단어를 한자로 대체

### balanced_data
* topic_idx (label)별 데이터 개수가 불균형하기에 Over Samplig을 통해 해결

### revised_data_visualization
* 증식한 데이터 분석을 위해 시각화를 진행
* 라벨 별 데이터 분포 확인
* 라벨 별 문장 길이 확인 (최단/최장/최빈)
* 워드 클라우드를 통해 라벨 별 주요 단어 확인
