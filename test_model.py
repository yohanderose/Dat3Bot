import pickle
from preprocess import img_to_feature_vec

test = img_to_feature_vec('./dataset/not/AF1003.jpg', 'hot')
if test is not None:
    test = test[:-1]
    # print(test)

clf = pickle.load(open('./models/lr.sav', 'rb'))
res = clf.predict([test])[0]
print(res)
