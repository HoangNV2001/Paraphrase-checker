from re import compile

def sentence_to_vec(s):
    s = [w.lower() for w in compile(r"\w+").findall(s)]
    cur = 0
    to_pop =[]
    not_first_single_char = False
    for i in range(len(s)):
        if len(s[i]) <2 and i>0:
            if not_first_single_char:
                s[cur] += s[i]
                to_pop.append(i)
            else:
                cur = i
                not_first_single_char = True
        else:
            cur = i
            not_first_single_char = False

    for ind in to_pop[::-1]:
        s.pop(ind)
    return s

class TextWrapper:
    def __init__(self, text):
        self.text = text
        self.list_sentence_vectors = self._split_sentence_word()
        self.inverted_index = self._inverted_index()
        self.sentence_count = len(self.list_sentence_vectors)

    def _split_sentence_word(self):
        sentence_list = self.text.split('.')
        to_pop = []
        cur = 0
        not_first_single_word_sentence = False
        for i in range(len(sentence_list)):
            splited = sentence_to_vec(sentence_list[i])
            if len(splited) <2 and i>0:
                if not_first_single_word_sentence:
                    sentence_list[cur].extend(splited)
                    to_pop.append(i)
                else:
                    sentence_list[i] = splited
                    cur = i
                    not_first_single_word_sentence = True
            else:
                sentence_list[i] = splited
                cur = i
                not_first_single_word_sentence = False

        for ind in to_pop[::-1]:
            sentence_list.pop(ind)
        return sentence_list

    def _inverted_index(self):
        inverted_index = {}
        for i in range(len(self.list_sentence_vectors)):
            for word in self.list_sentence_vectors[i]:
                if word not in inverted_index.keys():
                    inverted_index[word] = [i]
                else:
                    inverted_index[word].append(i)
        return inverted_index


def process_input_file(file_path, type):
    from app.Modules.PDFtoTxt import PdfConverter
    if type == 'pdf':
        text = PdfConverter(file_path= file_path).convert_pdf_to_txt()
    elif type == 'txt':
        with open(file_path, 'r', encoding = "utf-8") as f:
            text = f.read()
    else:
        raise Exception("Unknown file type!")

    text_wrapper = TextWrapper(text)
    return text_wrapper

if __name__ =='__main__':
    from PDFtoTxt import PdfConverter
    w = TextWrapper(PdfConverter(file_path= 'app/Data/DownloadedPDFs/Paper_91-Vietnamese_Sentence_Paraphrase_Identification.pdf').convert_pdf_to_txt())
