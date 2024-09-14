import time

import requests
import os
from fpdf import FPDF
from search_document import data_loading,single_file_loading
# print(key)
# url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}"
# a = requests.get(url).json()
# print(a)
from sentence_transformers import SentenceTransformer

from threading import Thread
class Scraper(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.count = 3
        self.key = os.environ.get("NEWSAPIKEY")
        self.url =  f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.key}"
        self.dir = "E:/21bce7985_ML/document_pdf/"
    def run(self):
        while True:
            self.scrape_articles()
            time.sleep(60)

    def scrape_articles(self):
        response = requests.get(self.url).json()
        articles = response.get("articles",[])
        news = []
        for article in articles:
            source = article.get("source",{})
            title = article.get("title","")
            description = article.get("description","")
            news.append([source,title,description])

        self.make_pdf(news,self.dir)
        return news

    def clean_text(self,text):
        try:
            return text.encode("latin-1", "ignore").decode("latin-1")
        except UnicodeEncodeError:
            return text.encode("ascii", "ignore").decode("ascii")
    def make_pdf(self,news,output_file):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial",size = 15)
        pdf.cell(200,10,txt = "News",ln = True,align = "C")
        for new in news:
            source,title,desc = new
            # print(source)
            # print(title)
            # print(desc)
            source = self.clean_text(source.get("name",""))
            if title:
                title =self.clean_text(title)
            else:
                title = ""
            if desc:
                desc = self.clean_text(desc)
            else:
                desc = ""
            pdf.ln(10)
            pdf.set_font("Arial",style="B",size=12)
            pdf.multi_cell(0,10,f"Title:{title}")
            pdf.set_font("Arial",size = 12)
            pdf.multi_cell(0,10,f"source:{source}")
            pdf.multi_cell(0,10,f"Description:{desc}")
        file_name = f"news{self.count}.pdf"
        output_path = os.path.join(output_file,file_name)
        pdf.output(output_path)
        self.count+=1
        single_file_loading(output_file,self.count)

# pdf_maker = Scraper()
# pdf_maker.scrape_articles()