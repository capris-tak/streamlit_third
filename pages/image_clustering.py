import os
import cv2
from google.colab.patches import cv2_imshow
import glob
import pandas as pd
import numpy as np
from sklearn import svm
import pickle

cs = sorted([x.split('/')[-1] for x in glob.glob('images/*')])

labels = []
images = []

for c in cs:
  c_path = os.getcwd() + '/images/'+ c +'/'
  for k in glob.glob(c_path + "*.jpg"):
    img = cv2.imread(k)
    #print(c,img.shape)
    img = cv2.resize(img, dsize=(64, 64))
    img = img.flatten()
    labels.append(c)
    images.append(img)

# 学習モデルを作成する
model = svm.SVC(decision_function_shape='ovr')
# モデルを学習させる
model.fit(images, labels)
# 相関を表示
print(model.score(images, labels))
# 学習データをファイルに保存
pickle.dump(model, open("model.sav", "wb"))


#学習モデルの読み込み
model = pickle.load(open("model.sav", 'rb'))
#フォルダ内の画像ファイルを取り出す
for file in glob.glob("*.jpg"):
    img = cv2.imread(file)
    #画像を学習しやすいように加工する
    img = cv2.resize(img, (64, 64))
    cv2_imshow(img)
    img = img.flatten()
    print(file,"判定結果　　"+str(model.predict([img])))