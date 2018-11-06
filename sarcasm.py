from nltk.tokenize import word_tokenize
from nltk import pos_tag
from textblob import TextBlob
from sklearn.model_selection import cross_val_score
from sklearn import svm
import csv
import pickle
from features import detect_yeah
from features import detect_prop
from features import get_uni
from features import uni_feature

train_label = []
train_first = []
train_second = []
test_first = []
test_second = []

uni = {}

def extract_feature(first, second, file):
	with open(file, 'w') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		features = []
		for i in range(len(first)):
			feature = []
			detect_yeah(first[i], feature)
			uni_feature(first[i], uni, feature)
			# feature.append(detect_prop(first[i]))
			# testimonial_f = TextBlob(first[i])
			# testimonial_s = TextBlob(second[i])
			# feature.append(testimonial_f.sentiment.polarity)
			# feature.append(testimonial_f.sentiment.subjectivity)
			# feature.append(testimonial_f.sentiment.polarity)
			# feature.append(testimonial_f.sentiment.subjectivity)
			wr.writerow(feature)
			# tokens = word_tokenize(line)
			# print(pos_tag(tokens))
			# print(word_tokenize(line))
			features.append(feature)
	return features


def read_train():
	f = open("train.tsv","r")
	line = f.readline()
	while line:
		line = f.readline()
		if(len(line) > 0):
			train_label.append(line.strip().split("\t")[0])
			train_first.append(line.strip().split("\t")[1])
			train_second.append(line.strip().split("\t")[2])
			# print(line.strip().split("\t")[1].split(' ', 1)[0])
	f.close()

def read_test():
	f = open("test.tsv","r")
	line = f.readline()
	while line:
		line = f.readline()
		if(len(line) > 0):
			test_first.append(line.strip().split("\t")[1])
			test_second.append(line.strip().split("\t")[2])
	f.close()

def read_features(file):
	features = []
	with open(file, 'r') as myfile:
		reader = csv.reader(myfile)
		for row in reader:
			features.append(row)
	return features

def train_features(features):
	print("Training now!")
	clf = svm.SVC(kernel='linear')
	scores = cross_val_score(clf, features, train_label, cv=3)
	# clf.fit(features, train_label) 
	# print(clf.coef_)
	print(scores)

	
	return clf

def test(clf, features_test):
	with open("eevee_submission.csv", 'w') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		line = []
		line.append("Id")
		line.append("Category")
		wr.writerow(line)

		Id = 0
		for feature in features_test:
			wrap = []
			wrap.append(feature)
			line = []
			line.append(Id)
			line.append(int(clf.predict(wrap)))
			wr.writerow(line)
			Id += 1

def save_model(clf):
	filename = 'model.sav'
	pickle.dump(clf, open(filename, 'wb'))

def load_model():
	filename = 'model.sav'
	clf = pickle.load(open(filename, 'rb'))
	return clf

def main():
	read_train()
	read_test()
	get_uni(train_first, train_second, uni)
	# features_train = extract_feature(train_first, train_second, "feature.csv")
	# features_test = extract_feature(test_first, test_second, "feature_test.csv")
	# features_train = read_features("feature.csv")
	# features_test = read_features("feature_test.csv")
	# clf = train_features(features_train)
	# save_model(clf)
	# clf = load_model()
	# test(clf, features_test)
	


if __name__ == "__main__":
	main()