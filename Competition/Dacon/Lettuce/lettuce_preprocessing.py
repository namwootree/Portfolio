import pandas as pd
import numpy as np

import os
import glob
from tqdm.auto import tqdm

import warnings
warnings.filterwarnings(action='ignore') 

class lettuce_train_set_preprocessing():

  def merge_X_y(self,
                path_train_input,
                path_train_target,
                path_save
                ):
                
    all_input_list = sorted(glob.glob(path_train_input + '*.csv'))
    all_target_list = sorted(glob.glob(path_train_target + '*.csv'))

    for path_X, path_y in tqdm(zip(all_input_list, all_target_list)):

      df_X = pd.read_csv(path_X)
      df_y = pd.read_csv(path_y)

      df_y['DAT'] = df_y['DAT'].apply(lambda x : x-1)

      df_merge = pd.merge(df_X, df_y, how='left', on='DAT')

      CASE_FILE_NAME = path_y.split('/')[-1]
      CASE_NUM = CASE_FILE_NAME.split('.')[0]

      df_merge['CASE_NUM'] = CASE_NUM

      col1 = df_merge.columns[-1:].to_list()
      col2 = df_merge.columns[:-1].to_list()

      df_merge = df_merge[col1 + col2]
      df_merge.to_csv(path_save+ '/' +CASE_FILE_NAME)

    print('DONE')

  
  def concat_case_data(self,
                       path_save):

    list_Data = os.listdir(path_save)
    list_Data = sorted(list_Data)

    df_total = pd.DataFrame(columns=['CASE_NUM', 'DAT', 'obs_time', '내부온도관측치', '내부습도관측치', 'co2관측치', 'ec관측치',
       '시간당분무량', '일간누적분무량', '시간당백색광량', '일간누적백색광량', '시간당적색광량', '일간누적적색광량',
       '시간당청색광량', '일간누적청색광량', '시간당총광량', '일간누적총광량', 'predicted_weight_g'])

    for case in list_Data:

      df = pd.read_csv(path_save + '/' + case)
      df.drop(['Unnamed: 0'],axis=1, inplace =True)
      
      df_total = pd.concat([df_total, df], axis=0)
    
    df_total.to_csv('/content/total_case_train.csv')

    print('DONE')
