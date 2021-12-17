import numpy as np
np.random.seed(42)
from Modules.SimilarityMeasures import vectorize_pair
import re

def read_data_file(dir):
    text_set =[]
    with open(dir, 'r', encoding ='utf-8') as text:
        for line in text.readlines():
            text_set.append(line.strip())
    return text_set

def remove_special_chars(sentence, keep_under_score):
    sentence = sentence.lower()
    sentence = re.sub(r'(v\s\.\sv\s.)', '', sentence, re.UNICODE)
    if keep_under_score:
        sub_string = ''.join(ch for ch in sentence if (ch.isalnum() or ch == ' ' or ch == '_'))
    else:
        sub_string = ''.join(ch for ch in sentence if (ch.isalnum() or ch == ' '))
    sub_string_2 = re.sub('\s{2,}', ' ', sub_string, re.UNICODE)
    return sub_string_2

def create_list_pair(sentences1, sentences2, keep_under_score = True):
    number_sentences = len(sentences1)
    list_sentences = []
    for i in range(number_sentences):
        s1 = remove_special_chars(sentences1[i], keep_under_score)
        s2 = remove_special_chars(sentences2[i], keep_under_score)
        s = {'s1': s1, 's2': s2}
        list_sentences.append(s)
    return list_sentences

# def write_to_file(file_name_1, file_name_2, pairs):
#     fout1 = open(file_name_1, 'w')
#     fout2 = open(file_name_2, 'w')
#     for pair in pairs:
#         s1 = pair['s1'] + '\n'
#         s2 = pair['s2'] + '\n'
#         fout1.write(s1.encode('utf8'))
#         fout2.write(s2.encode('utf8'))
#     fout1.close()
#     fout2.close()


if __name__ == '__main__':

    train_labels = read_data_file('app//Data//vnPara//Labels.txt')
    for i in range (len(train_labels)):
        if train_labels[i] == '1,':
            train_labels[i] = 1
        else:
            train_labels[i] = int(train_labels[i])

    train_data = []

    list_sentence_1 = []
    list_sentence_2 = []
    with open("app//Data//vnPara//Sentences1.txt", encoding ='utf-8') as fin:
        for line in fin:
            list_sentence_1.append(line)

    with open("app//Data//vnPara//Sentences2.txt", encoding ='utf-8') as fin:
        for line in fin:
            list_sentence_2.append(line)

    pairs = create_list_pair(list_sentence_1, list_sentence_2, False)

    num_samples = len(train_labels)
    for i in range(num_samples):
        s1 = pairs[i]['s1'].split()
        s2 = pairs[i]['s2'].split()
        train_data.append(vectorize_pair(s1,s2))

    X = np.array(train_data)
    y = np.array(train_labels)

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

    from sklearn.svm import SVC
    svm_clf2= SVC(kernel = 'rbf', probability = True)
    svm_clf2.fit(X_train, y_train)

    from sklearn.metrics import f1_score
    print('f1 = ',f1_score(y_test, svm_clf2.predict(X_test)))


    import pickle

    filename = 'app//Models//SVM//svm_paraphrase_identification_model.sav'
    pickle.dump(svm_clf2, open(filename, 'wb'))
