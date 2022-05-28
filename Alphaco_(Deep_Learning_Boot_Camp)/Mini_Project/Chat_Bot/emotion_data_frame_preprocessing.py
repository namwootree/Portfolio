def emotion_data_frame_preprocessing1(DataFrame):

  import pandas as pd

  DataFrame = DataFrame[['감정_대분류', '감정_소분류', '사람문장1', '사람문장2']]

  p_cond = ['신이 난', '안도', '기쁨', '만족스러운', '자신하는', '편안한', '감사하는', '신뢰하는', '느긋']
  d_cond = ['스트레스 받는', '당황', '분노', '회의적인', '혼란스러운', '흥분', '걱정스러운', '충격 받은', '불안', '짜증내는', '실망한', '슬픔', '툴툴대는', '악의적인']

  cond = p_cond + d_cond

  DataFrame = DataFrame[DataFrame['감정_소분류'].isin(cond)]

  for i in p_cond:
    cond = (DataFrame['감정_소분류']== i)
    DataFrame.loc[cond, '감정'] = '긍정'

  for i in d_cond:
    cond = (DataFrame['감정_소분류']== i)
    DataFrame.loc[cond, '감정'] = '부정'

  sen1 = DataFrame['사람문장1']
  sen2 = DataFrame['사람문장2']
  emo = DataFrame['감정']

  d1 = {'사람문장':list(sen1), '감정':list(emo)}

  d2 = {'사람문장':list(sen2), '감정':list(emo)}

  df1 = pd.DataFrame(data=d1)
  df2 = pd.DataFrame(data=d2)

  DataFrame = pd.concat([df1, df2], axis=0)

  return DataFrame

def emotion_data_frame_preprocessing2(DataFrame, data_size):
  cond = (DataFrame['감성'] == 'm') & (DataFrame['발화자']== 'c') & (DataFrame['QA여부']== 'q')

  DataFrame = DataFrame.loc[cond]

  DataFrame = DataFrame[['발화문', '감성']]

  DataFrame.columns = ['사람문장', '감정']

  cond1 = (DataFrame['감정'] == 'm')

  DataFrame.loc[cond1, '감정'] = '중립'

  mdf = DataFrame[:data_size]

  return mdf