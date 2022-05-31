!pip install konlpy
!apt-get update -qq
!apt-get install fonts-nanum* -qq


from konlpy.tag import Okt
import seaborn as sns
from tqdm.notebook import tqdm
import re
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import cv2
from google.colab.patches import cv2_imshow

!gdown --id 1MYIvNImqYe7WVM4N05mZBkZj_UsQ7kJw

file_path = '/content/불용어.txt'
with open(file_path) as f:
    lines = f.readlines()

stop_words = [line.rstrip('\n') for line in lines]

okt=Okt()

def display_result(DataFrame):
  count = sns.countplot(data=DataFrame, x='Coustomer_Emotion', palette='Set3')
  plt.savefig('savefig_default.png')

  texts = DataFrame['Question']

  lst_clean = []

  for text in tqdm(texts):
    lst_clean.append(re.sub("[^가-힣\\s]", "", text))

  text_token = []

  for text in tqdm(lst_clean):
    text_token.append(okt.morphs(text, stem=True))

  word_cloud = []

  for token_text in tqdm(text_token):
    word_cloud.extend([clean for clean in token_text if not clean in stop_words])

  word_count = Counter(word_cloud)

  wc=WordCloud(font_path='/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf',
              background_color='white', width=200, height=200, max_words=10, max_font_size=200)
  wc.generate_from_frequencies(dict(word_count))
  wc.to_file("고객_질문_키워드.png")

  img = cv2.imread('고객_질문_키워드.png', cv2.IMREAD_UNCHANGED)
  display(count)
  cv2_imshow(img)