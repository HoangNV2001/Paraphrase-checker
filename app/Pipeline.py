from app.Modules.SimilarityMeasures import vectorize_pair
from app.Modules.PDFtoTxt import PdfConverter
from app.Modules.SearchnGet import search, get_doc
from app.Modules.Compare import compare, match_propotion
import pickle
import numpy as np
from app.Modules.text_wrapper import TextWrapper, process_input_file
from os.path import getsize


def search_download_compare(file_path, type, query, num):
    text_wrapper1 = process_input_file(file_path, type)
    yield True

    urls = search(query = query, num = num)
    yield True

    processed_text_dirs = []
    processed_text_count = 0
    for url in urls:
        if processed_text_count == num:
            break
        try:
            processed_text_dir = get_doc(url, processed_text_count)
            processed_text_dirs.append(processed_text_dir)
            yield True
            processed_text_count +=1
        except Exception:
            pass
    # compare_pdfs = ['Data\\Paraphrase Identification in Vietnamese Documents.pdf']

    pkl_file = 'app/Models/SVM/svm_paraphrase_identification_model.sav'
    with open(pkl_file, 'rb') as file:
        pkl_model = pickle.load(file)
    yield True

    match = {}
    for text_dir, url in processed_text_dirs:
        match = compare(text_wrapper1 , processed_text_dir, match, pkl_model)
        yield True
    print("Finished comparing!")

    proportion = match_propotion(match)
    yield True
    return match, proportion


if __name__ == '__main__':
    pdf_file = 'app//Data//Paraphrase Identification in Vietnamese Documents.pdf'
    query = "Paraphrase Identification in Vietnamese Documents"
    search_download_compare(pdf_file, query, 2)
