import re
import pandas as pd

from transformers import TextClassificationPipeline
from transformers import BertTokenizerFast, BertModel

loaded_tokenizer = BertTokenizerFast.from_pretrained('klue/bert-base')


START_TOKEN, END_TOKEN = [loaded_tokenizer.vocab_size], [loaded_tokenizer.vocab_size + 1]


def preprocess_sentence(sentence):
  sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
  sentence = sentence.strip()
  return sentence

def evaluate(sentence):
  sentence = preprocess_sentence(sentence)

  sentence = tf.expand_dims(
      START_TOKEN + loaded_tokenizer.encode(sentence) + END_TOKEN, axis=0)

  output = tf.expand_dims(START_TOKEN, 0)

  # 디코더의 예측 시작
  for i in range(50):
    predictions = q_a_model(inputs=[sentence, output], training=False)

    # 현재(마지막) 시점의 예측 단어를 받아온다.
    predictions = predictions[:, -1:, :]
    predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

    # 만약 마지막 시점의 예측 단어가 종료 토큰이라면 예측을 중단
    if tf.equal(predicted_id, END_TOKEN[0]):
      break

    # 마지막 시점의 예측 단어를 출력에 연결한다.
    # 이는 for문을 통해서 디코더의 입력으로 사용될 예정이다.
    output = tf.concat([output, predicted_id], axis=-1)

  return tf.squeeze(output, axis=0)

def predict(sentence):
  prediction = evaluate(sentence)

  predicted_sentence = loaded_tokenizer.decode(
      [i for i in prediction if i < loaded_tokenizer.vocab_size])

  return predicted_sentence


def for_company_chat_bot_result(emotion_model, q_a_model):

  text_classifier = TextClassificationPipeline(
    tokenizer=loaded_tokenizer, 
    model=emotion_model, 
    framework='tf',
    return_all_scores=True)

  list_customer_id = []
  customer_question = []
  customer_answer = []
  customer_emotion = []

  while True:

    customer_id = str(input('고객님의 아이디를 입력해주세요 : '))
    print()

    print(f'고객님의 아이디가 {customer_id} 맞습니까?')

    print()
    confirmation = str(input('고객님의 아이디가 맞으면 yes / 아니면 no를 입력해주세요 : '))

    if confirmation == 'yes':
      list_customer_id.append(customer_id)
      break

    else:
      pass


  print()
  print('\n--------------------------------------------\n')
  print()
  print('Q & A 챗봇을 그만두고 싶을 경우 end를 입력해주세요!')
  print()

  while True:
    
    text = str(input('50자 내의 질문 사항을 입력해주세요. : '))
    print()

    if len(text) > 50:
      continue

    if text == 'end':
      print()
      print(f'{customer_id}님 챗봇 서비스를 이용해주셔서 감사합니다')
      break
    
    answer = predict(text)
    customer_answer.append(answer)
    print(f'답변 : {answer}')

    customer_question.append(text)
    
    d = text_classifier(text)[0][0]
    p = text_classifier(text)[0][1]

    max_emotion = max(p['score'], d['score'])


    if max_emotion == p['score']:
      customer_emotion.append('positive')

    else: 
      customer_emotion.append('negative')

  list_customer_id = list_customer_id * len(customer_question)

  result_Q_A = pd.DataFrame(zip(list_customer_id, customer_question, customer_answer, customer_emotion))
  result_Q_A.columns = ['Customer_ID', 'Question', 'Answer', 'Coustomer_Emotion']

  return result_Q_A