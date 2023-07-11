# Paraphrase-checker



## About The Project
Description: Paraphrase Checking Web App. <br>
Project submission to course Project I - 709162 - IT3910E<br>
Student: Nguyễn Việt Hoàng - SID: 20194434<br>

## Getting Started
_These are the instructions on setting up this project locally._
### Prerequisites
* [Python 3.9](https://www.python.org/downloads/release/python-390/)
### Installation

1. Download the [repo](https://github.com/HoangNV2001/Paraphrase-checker/archive/refs/heads/main.zip)
2. Unzip the downloaded package.
3. Open the Command Prompt (for Windows), navigate to the project folder _Paraphrase-checker_.
4. Install the libraries in `requirements.txt`
   ```sh
   pip install -r requirements.txt
   ```
5. To start the web application, in the command prompt that has been navigated to this project's directory, enter this command:
   ```sh
   python run.py
   ```
6. Leave the console open, and open this URL in the web browser: http://localhost:5000/

## Usage
* Below is the main page interface, which will appear when user open the web page:<br>

![Demo1](https://user-images.githubusercontent.com/72451372/155877871-61a834da-acd3-4e02-bbd5-5a107e38cf7c.png)

* User input the document that needs to be check by either enter the text into Section 1, or insert the document through the button in Section 2. 
<br><b>Note</b>: Section 1 and 2 cannot be both filled nor both empty.
* Next, the user enter the keyword that best summarize/ present the document content into Section 3. This keyword will be used to search for documents/webpages on Google search. <br> Section 3 cannot be empty.
* If the user want to only compare with PDF files (which mean to exclude websites from the search), tick the check box in Section 4.
* Downloading and comparing with 1 document on average takes 12 seconds. The number of default value for number of search results to download and compare is 6, with the maximum value is 20. This value can be changed by the user by using the slider in Section 5.
* When the form-filling is completed, press the “Start search” button in Section 6 to signal the system to start take in and process the input.
* Afterward, the waiting interface will appear.
* When the processing is completed, the webpage will be redirected to the result page. One example of the result page is as follow:<br>

![Demo2](https://user-images.githubusercontent.com/72451372/155877989-99350afb-e9e6-44a6-97d4-0e1fd7c63466.png)

There are 2 main sections in the result page:
* Section 1 show the percentage of input document that has high probability of paraphrasing from an online source.
* Section 2 is a table, in which each row is a sentence pair that has high chance of paraphrasing - the first column contains the sentence in the input document, the second column contains the sentence found from the search, in the third column is the link to the webpage/document that contains the source sentence, the fourth columns shows value of the probability of paraphrasing determined by the classification model.

## Contact
Nguyễn Việt Hoàng - hoang.nv194434@sis.hust.edu.vn - hoangnguyenviet1611@gmail.com </br>
Project Link: [https://github.com/HoangNV2001/Paraphrase-checker/](https://github.com/HoangNV2001/Paraphrase-checker/)

