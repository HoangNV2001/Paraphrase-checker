from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


class PdfConverter:
    '''
    Convert .pdf file to .txt file
    '''
    def __init__(self, file_path):
         self.file_path = file_path
# convert pdf file to a string which has space among words
    def convert_pdf_to_txt(self):
         rsrcmgr = PDFResourceManager()
         retstr = StringIO()
        #  codec = 'utf-8'
         laparams = LAParams()
         device = TextConverter(rsrcmgr, retstr, laparams=laparams)
         with open(self.file_path, 'rb') as fp:
             interpreter = PDFPageInterpreter(rsrcmgr, device)
             password = ""
             maxpages = 0
             caching = True
             pagenos = set()
             for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
                  interpreter.process_page(page)

         device.close()
         str = retstr.getvalue()
         retstr.close()
         return str
# convert pdf file text to string and save as a text_pdf.txt file
    def save_convert_pdf_to_txt(self):
         content = self.convert_pdf_to_txt()
         with open('text_pdf.txt', 'wb') as txt_pdf:
             txt_pdf.write(content.encode('utf-8'))

if __name__ == '__main__':
    import sys
    # append the path of the parent directory
    sys.path.append("..")
    pdfConverter = PdfConverter(file_path= 'app/Data/Paraphrase Identification in Vietnamese Documents.pdf')

    pdfConverter = PdfConverter(file_path= 'app/Data/DownloadedPDFs/Paper_91-Vietnamese_Sentence_Paraphrase_Identification.pdf')
    print(pdfConverter.convert_pdf_to_txt())
