from app.Modules.SimilarityMeasures import vectorize_pair
from app.Modules.PDFtoTxt import PdfConverter
import numpy as np
from app.Modules.text_wrapper import TextWrapper
from os.path import getsize

def compare(match, text_wrapper1 , processed_text_dir, pkl_model):
    '''
    Compare the input document with another downloaded document sentence-by-sentence.

    :param: match: Dictionary with keys are the sentences in the input document
                    that has high probability of paraphrasing, the values consists
                    of the sentence found in another source that has high
                    paraphrasing chance, its URL, and the probability value.
    :param: text_wrapper1: TextWrapper object of the input document.
    :param: processed_text_dir: String, directory to the downloaded content.
    :pkl_model: pkl file, the SVM model used for classification.
    :return: match: Dictionary (as described above)
    '''
    text_dir = processed_text_dir[0]
    url = processed_text_dir[1]
    # url = "<a href=\""+url+"\">"+url.split('/')[-1]+"</a>"
    url = "<a href=\""+url+"\">"+url+"</a>"
    try:
        print("\n\n Comparing with", text_dir)
        if getsize(text_dir) > 500000:
            raise Exception("The file is too big")

        if text_dir[-4:]=='.pdf':
            text2 = PdfConverter(file_path= text_dir).convert_pdf_to_txt()
        else:
            with open(text_dir, 'r', encoding = "utf-8") as f:
                text2 = f.read()


        sentence_list1 = text_wrapper1.list_sentence_vectors
        inverted_index1 = text_wrapper1.inverted_index
        '''
        inverted_index: Dictionary,
                Keys are words that appear in the document,
                Values are the indexes of the sentences that contain the word.
        '''

        text_wrapper2 = TextWrapper(text2)
        sentence_list2 = text_wrapper2.list_sentence_vectors

        '''
        Only compare compare sentence pairs that share more that 4 common words.
        '''
        for sentence_vec in sentence_list2:

            to_compare = {}
            '''
            Keys are indexes of the sentences in the input sentence.
            Values are number of words that sentence_vec and the indexed sentence
                share in common.
            '''
            for word in sentence_vec:
                if word in inverted_index1.keys():
                    for sentence_index in inverted_index1[word]:
                        if sentence_index not in to_compare.keys():
                            to_compare[sentence_index] =1
                        else:
                            to_compare[sentence_index] += 1

            for sentence_index in to_compare.keys():
                if to_compare[sentence_index] >4:

                    v1 = sentence_list1[sentence_index]
                    v2 = sentence_vec

                    x = np.array([vectorize_pair(v1, v2)])
                    prob = pkl_model.predict_proba(x)[0][1]

                    if prob > 0.5:
                        s1 = ' '.join(v1)
                        s2 = ' '.join(v2)
                        if s1 not in match.keys():
                            match[s1] = [s2, url, round(prob,2)]
                        else:
                            if prob > match[s1][2]:
                                match[s1] = [s2, url, round(prob,2)]


    except Exception as e:
        print("Exception with", text_dir)
        print(e)

    return match

def match_proportion(match, sentence_count):
        '''
        Create a report of the comparing process, based on the "match" dictionary.

        :param: match: Dictionary with keys are the sentences in the input document
                        that has high probability of paraphrasing, the values consists
                        of the sentence found in another source that has high
                        paraphrasing chance, its URL, and the probability value.
        :param: sentence_count: number of sentences in the input document.
        :return: proportion: Dictionary, the levels of similarity and number
                            of sentence pairs that belong to those levels.
        '''
        similar_95_count = 0
        similar_80_count = 0
        similar_65_count = 0
        similar_50_count = 0
        for key, item in match.items():
            prob = item[2]
            if  prob > 0.95:
                similar_95_count += 1
                match[key][2] = "<p style=\"color:maroon;\">"+str(prob)+"</p>"
            elif prob > 0.8:
                similar_80_count += 1
                match[key][2] = "<p style=\"color:red;\">"+str(prob)+"</p>"
            elif prob > 0.65:
                similar_65_count += 1
                match[key][2] = "<p style=\"color:orange;\">"+str(prob)+"</p>"
            elif prob > 0.5:
                similar_50_count += 1
                match[key][2] = "<p style=\"color:darkblue;\">"+str(prob)+"</p>"
        not_similar = sentence_count - similar_95_count - similar_80_count - similar_65_count - similar_50_count

        proportion = {
                        "Similarity level": "proportion",
                        "Very high (Sentence with possibility of paraphrasing higher than 95%)": similar_95_count,
                        "High (80% to 95%)": similar_80_count,
                        "Noticible (65% to 80%)": similar_65_count,
                        "Low (50% to 65%)": similar_50_count,
                        "Not a paraphrase (less than 50% probability)": not_similar
                        }
        return proportion
