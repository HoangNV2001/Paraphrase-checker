from re import compile


class TextWrapper:
    '''
    Wrap a document, which is in String type, in an Object.
    Provide some attributes and methods for later uses in Compare
    '''
    def __init__(self, text):
        self.text = text
        self.list_sentence_vectors = self._split_sentence_word()
        self.sentence_count = len(self.list_sentence_vectors)
        self.inverted_index = self._inverted_index()

    def _split_sentence_word(self):
        '''
        Split the text into list of sentences.
        Each sentence is splited into list of words.
        Sentences which have less than 5 words would be removed
                                        (not used for comparison).
        :return: list of lists of strings.
        '''
        sentence_list = self.text.split('.')
        to_pop = []

        for i in range(len(sentence_list)):
            splited = [w.lower() for w in compile(r"\w+").findall(sentence_list[i])]
            if len(splited) <5:
                if not_first_single_word_sentence:
                    to_pop.append(i)

        for ind in to_pop[::-1]:
            sentence_list.pop(ind)

        return sentence_list

    def _inverted_index(self):
        '''
        return: inverted_index: Dictionary,
                Keys are words that appear in the document,
                Values are the indexes of the sentences that contain the word.
        '''
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
