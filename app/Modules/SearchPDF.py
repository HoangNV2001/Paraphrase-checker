from googlesearch import search as Search
import urllib.request

class GetPDF:
    def __init__(self, query, num = 10, dir = 'app/app/Data/DownloadedPDFs'):
    # to search
        self.query = query+" filetype:pdf"
        self.num = num
        self.dir = dir
        self.urls = []

    def search(self):
        result = Search(self.query, tld="co.in", num= self.num*2, stop= self.num*2, pause=1)
        for j in result:
            if j[-4:] =='.pdf' and j[-4:] not in self.urls:
              self.urls.append(j)
        return self.urls

    def download(self):
        urls = self.search()
        downloaded = []
        download_count = 0
        for url in urls:
            if download_count == self.num:
                break
            filename = self.dir +'/'+ url.split("/")[-1]

            print("Downloading:", url)
            try:
                request = urllib.request.urlopen(url, timeout=6)
                with open(filename, 'wb') as f:
                    f.write(request.read())
                    print("Download successful, saved as:", filename)
                    downloaded.append((filename, url))
                    download_count +=1
            except:
                print("Download", url,"unsuccessful")
        return downloaded

if __name__ == '__main__':
    search = GetPDF(query = 'nlp',dir = '../app/Data/DownloadedPDFs')
    download = search.download()
    print(download)
