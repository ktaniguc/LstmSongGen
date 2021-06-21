from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
 
import numpy as np
import random
import sys, os
import io
 
#テキストの生成
args = sys.argv  #1=input file name #result mid name #3=model name
inputText = args[1] + ".txt"
resultText = args[1] + "_result.txt"
f = open(inputText, 'r')
data = f.read()
text = data.split(",")

DS = os.sep
bs = os.path.dirname(__file__) + DS
model_weights_path = './' + args[2] + 'w.hdf5'
model_save_path = './'+ args[2] + '.hdf5'
make_model = False
#ここからLSTM
print('--------- start LSTM')
chars = text
count = 0
char_indices = {} #辞書
indices_char = {} #逆引き辞書

for word in chars:
  if not word in char_indices:
    char_indices[word] = count
    count +=1
    print(count, word) #登録した単語を表示

#==================
#逆引き辞書を辞書から作成する
indices_char = dict([(value, key) for (key, value) in char_indices.items()])

maxlen = 5
step = 1
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
  sentences.append(text[i: i + maxlen])
  next_chars.append(text[i + maxlen])

print('nb sequences:', len(sentences))

#モデルのファイルがある場合は読み取る
if(os.path.exists(model_save_path) and os.path.exists(model_weights_path)):
  print('-----------read Model')
  model=load_model(model_save_path)
  model.load_weights(model_weights_path)

else:
  make_model = True

  print('Vectorization...')
  x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
  y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
  for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
      x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

  #モデル生成
  print('Build model...')
  model = Sequential()
  model.add(LSTM(128,return_sequences=True,input_shape=(maxlen, len(chars))))
  model.add(LSTM(128,return_sequences=True))
  model.add(LSTM(128))
  model.add(Dense(len(chars), activation='softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

def sample(preds, temperature=1.0):
  preds = np.asarray(preds).astype('float64')
  preds = np.log(preds) / temperature
  exp_preds = np.exp(preds)
  preds = exp_preds / np.sum(exp_preds)
  probas = np.random.multinomial(1, preds, 1)
  while np.argmax(probas) >= count:
    probas = np.random.multinomial(1, preds, 1)

  return np.argmax(probas)


def on_epoch_end(epoch, _):
  print()
  print('------- Generating text after Epoch: %d' % epoch)
  start_index = random.randint(0, len(text) - maxlen - 1)
  start_index = 0 #テキストの最初からスタート
  for diversity in [0.2]: #ここは0.2のみ？
    print('--------diversity:', diversity)

    generated = ''
    sentence = text[start_index: start_index + maxlen]
    #sentenceはリストなので文字列へ変換
    generated += ','.join(sentence)
    print(sentence)

    print('--------- Generating with seed:"' + ",".join(sentence) + '"')
    sys.stdout.write(generated)

    for i in range(100):
      x_pred = np.zeros((1, maxlen, len(chars)))
      for t, char in enumerate(sentence):
        x_pred[0, t, char_indices[char]] = 1.

      preds = model.predict(x_pred, verbose=0)[0]
      next_index = sample(preds, diversity)
      print("next_index = ", next_index, "indices = ", indices_char[next_index])
      next_char = indices_char[next_index]

      generated += next_char+","
      sentence = sentence[1:]
      sentence.append(next_char)

      sys.stdout.write(next_char)
      sys.stdout.flush()
    print()


def on_train_end(logs):
  print('----- saving model...')
  model.save_weights(model_weights_path)
  model.save(model_save_path)


def make_melody(length=200):
  start_index = random.randint(0, len(text) - maxlen - 1)
  #start_index = 0 #テキストの最初からスタート

  print(start_index)
  for diversity in [0.2]: #ここは0.2のみ？
    print('--------diversity:', diversity)

    generated = ''
    #sentence = inputText[0: maxlen]
    sentence = text[start_index: start_index + maxlen]
    generated += ','.join(sentence)
    print(sentence)

    print('--------- Generating with seed:"' + ",".join(sentence) + '"')
    sys.stdout.write(generated)

    for i in range(length):
      x_pred = np.zeros((1, maxlen, len(chars)))
      for t, char in enumerate(sentence):
        x_pred[0, t, char_indices[char]] = 1.

      preds = model.predict(x_pred, verbose=0)[0]
      next_index = sample(preds, diversity)
      next_char = indices_char[next_index]

      generated += next_char+","
      sentence = sentence[1:]
      sentence.append(next_char)

      sys.stdout.write(next_char)
      sys.stdout.flush()
    print()

  return generated


if make_model:
  print_callbak = LambdaCallback(on_epoch_end=on_epoch_end, on_train_end=on_train_end)
  model.fit(x, y, batch_size=128, epochs=120, callbacks=[print_callbak])

print('-------print score')
melo_sentence = make_melody(700)
print(melo_sentence)
file = open(resultText,'w+',encoding='utf-8').write(melo_sentence)

