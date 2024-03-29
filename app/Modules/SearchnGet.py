from googlesearch import search as Search
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from app.Modules.PDFtoTxt import PdfConverter

# class GGSearch:
#     def __init__(self, query, num = 10, dir = 'app/Data/DownloadedPDFs'):
#         self.query = query
#         self.num = num
#         self.dir = dir
#         self.urls = []

def search(query, num = 10):
    '''
    Search Google using the query and get the URLs from search results
    :param: query: String, the keywords for searching
    :param: num: Int, number of search results to take into account
    :return: list of strings: URLs from search results
    '''
    urls = Search(query, num_results= num*2)
    #search for 2 times the designated number. The spared are used for backup,
    #in case one of the links are inaccessible
    return urls

def get_doc(url, processed_text_count):
    '''
    Open the URLs, and download its content.
    :param: url: string
    :param: processed_text_count: Int, the number of downloaded pages so far,
            used for naming/numbering purpose.
    :return: string: The directory to the downloaded content
    '''
    processed_text_dir = None

    print("Downloading:", url)
    req = Request(url, headers={'User-Agent' : "Magic Browser"})
    try:
        r = urlopen(req, timeout = 4).read()

        if url[-4:] =='.pdf':
            # filename = self.dir +'/file_'+ str(processed_text_count)+'.pdf'
            filename = str(processed_text_count)+'.pdf'
            text = r

        else:
            # filename = self.dir +'/file_'+ str(processed_text_count)+'.txt'
            filename = str(processed_text_count)+'.txt'
            soup = BeautifulSoup(r, features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk).encode('utf-8')

        with open(filename, 'wb') as f:
            f.write(text)
            print("Download successful, saved as:", filename)

        processed_text_dir = (filename, url)

    except Exception as e:
        print(e)

    return processed_text_dir

def search_n_get(query, num = 10):
    '''
    Search Google using the query and get the URLs from search results
    Download the contents in the URLs.
    :param: query: String, the keywords for searching
    :param: num: Int, number of contents to download.
    :return: string: The directories to the downloaded contents
    '''
    urls = search(query, num)
    processed_text_dirs = []
    processed_text_count = 0

    for url in urls:
        if processed_text_count == self.num:
            break
        try:
            processed_text_dir = get_doc(url, processed_text_count)
            processed_text_dirs.append(processed_text_dir)
            processed_text_count +=1
        except Exception:
            pass

    return processed_text_dirs
