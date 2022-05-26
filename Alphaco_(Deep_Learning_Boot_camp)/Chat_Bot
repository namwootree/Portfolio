class ai_hub_data_frame_preprocessing():

  def list_seperate_for_Q_and_A(self, list_talker=None, list_sentence=None):

    import pandas as pd
    from tqdm.notebook import tqdm

    new_list_s = [] # 대화 주제 별 seller의 말뭉치의 집합
    new_list_c = [] # 대화 주제 별 consumer의 말뭉치의 집합

    new_c = [] # 대화 주제 별 임시 구매자 말뭉치
    new_s = [] # 대호 주제 별 임시 판매자 말뭉치

    for i, t in enumerate(tqdm(list_talker)): # t : 화자 (seller, consumer), i : 문장 리스트 위치


      if t == 'c': # 화자 : customer

        new_c.append(list_sentence[i]) # 구매자의 말을 구매자 말뭉치에 넣음
        new_list_s.append(' '.join(new_s)) # # 화자가 구매자로 바뀌었기에 모아둔 판매자 말뭉치를 new_list_s 넣는다
        new_s = [] # 판매자 말뭉치 초기화

      
      if t == 's': # 화자 : seller

        new_s.append(list_sentence[i])
        new_list_c.append(' '.join(new_c)) # 화자가 판매자로 바뀌었기에 모아둔 구매자 말뭉치를 new_list_c 넣는다
        new_c = [] # 구매자 말뭉치 초기화
    
    new_list_s.append(new_s[:][0]) # 맨 마지막 seller의 말까지 포함시킨다

    new_list_s = [x for x in new_list_s if x != ''] # 리스트 내에 '' 제거
    new_list_c = [x for x in new_list_c if x != '']

    return new_list_s, new_list_c

  def dataframe_handling_for_Q_and_A(self, DataFrame, list_seperate_for_Q_and_A):

    import pandas as pd
    
    df_need_col = DataFrame[['발화자', '발화문',
                             'QA번호', 'QA여부',
                             '상담번호', '상담내순번',
                             '인텐트']] # 필요한 columns만 추출

    df_sorted = df_need_col.sort_values(['상담번호', 'QA번호']) # 대화 주제별 및 순서 정렬

    cond_customer_question= (df_sorted['발화자'] == 'c') &  (df_sorted['QA여부'] == 'q') # consumer의 질문만 추출
    cond_seller_answer = (df_sorted['발화자'] == 's') &  (df_sorted['QA여부'] == 'a') # seller의 답변만 추출

    df_filtered = df_sorted.loc[cond_seller_answer|cond_customer_question]

    list_talker = list(df_filtered['발화자'])
    list_sentence = list(df_filtered['발화문'])

    new_list_s, new_list_c = list_seperate_for_Q_and_A(list_talker, list_sentence)

    df_customer = pd.DataFrame(new_list_c)
    df_seller = pd.DataFrame(new_list_s)

    df_Q_A = pd.concat([df_customer ,df_seller], axis=1)
    df_Q_A.columns = ['Question', 'Answer']

    print(f'총 데이터 개수 : {df_Q_A.shape[0]}')

    return  df_Q_A
