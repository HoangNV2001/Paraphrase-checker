from app.Modules.SimilarityMeasures import vectorize_pair
from app.Modules.PDFtoTxt import PdfConverter
from app.Modules.SearchnGet import search, get_doc
from app.Modules.Compare import compare, match_propotion
import pickle
import numpy as np
from app.Modules.text_wrapper import TextWrapper, process_input_file
from os.path import getsize


def search_download_compare(file_path, type, query, num):
    '''
    Process the input document,
    search Google using the query and number of search,
    scrape the contents found in the URLs returned from search result,
    compare the input document and the downloaded contents,
    return the comparison report.

    :param: file_path: String, directory to the input document.
    :param: type: String, extension of the input document ('.txt', '.pdf')
    :param: query: String, keywords used for searching
    :param: num: int, number of search results to take account into.
    :return: match: Dictionary with keys are the sentences in the input document
                    that has high probability of paraphrasing, the values consists
                    of the sentence found in another source that has high
                    paraphrasing chance, its URL, and the probability value.
    :return: proportion: Dictionary, the levels of similarity and number
                        of sentence pairs that belong to those levels.
    '''
    text_wrapper1 = process_input_file(file_path, type)

    urls = search(query = query, num = num)

    processed_text_dirs = []
    processed_text_count = 0
    for url in urls:
        if processed_text_count == num:
            break
        try:
            processed_text_dir = get_doc(url, processed_text_count)
            processed_text_dirs.append(processed_text_dir)

            processed_text_count +=1
        except Exception:
            pass

    pkl_file = 'app/Models/SVM/svm_paraphrase_identification_model.sav'
    with open(pkl_file, 'rb') as file:
        pkl_model = pickle.load(file)

    match = {}
    for text_dir, url in processed_text_dirs:
        match = compare(text_wrapper1 , processed_text_dir, match, pkl_model)

    print("Finished comparing!")

    proportion = match_propotion(match)

    return match, proportion


if __name__ == '__main__':
    pdf_file = 'app//Data//Paraphrase Identification in Vietnamese Documents.pdf'
    query = "Paraphrase Identification in Vietnamese Documents"
    search_download_compare(pdf_file, query, 2)
