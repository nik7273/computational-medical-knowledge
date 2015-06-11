# -*- coding: utf-8 -*-
#Search Wikipedia for Heart Attack
import wikipedia, codecs, itertools, os, time
from pprint import pprint

relevant_categories = {'medical','emergencies','disease'}

def findRelevantArticles(term,data_path='.'):
    articleList = []
    articles = wikipedia.search(term) #Setting suggestion = False (default value); No clear use for it now

    for article in articles:
        try: 
            article = wikipedia.page(article)
            category_keywords = set(list(itertools.chain.from_iterable([category.lower().split() for category in article.categories])))
            if len(category_keywords & relevant_categories) > 0:
                articlefilename = "content_"+str(article.title.lower())+".txt"
                if os.path.isfile(articlefilename):
                     articlefilename = "content_"+ str(article.title.lower())+'%s.txt' % str(term+time.strftime("%Y%m%d-%H%M%S"))
                with codecs.open(os.path.join(data_path,articlefilename),'wb', 'utf-8') as outfile:
                    content = wikipedia.page(article).content
                    print>>outfile,content
                articleList.append(str(article.title))
        except wikipedia.exceptions.PageError as e:
            pass
        except wikipedia.exceptions.DisambiguationError as e:
            for article in e.options:
                try:
                    article = wikipedia.page(article)
                    category_keywords = set(list(itertools.chain.from_iterable([category.lower().split() for category in article.categories])))
                    if len(category_keywords & relevant_categories) > 0:
                        articlefilename = "content_"+str(article.title.lower())+".txt"
                        if os.path.isfile(articlefilename):
                            articlefilename = "content_"+ str(article.title.lower())+'%s.txt' % str(term+time.strftime("%Y%m%d-%H%M%S"))
                        with codecs.open(os.path.join(data_path,articlefilename),'wb','utf-8') as outfile:
                            print>>outfile,article.content
                        articleList.append(str(article.title))
                except wikipedia.exceptions.DisambiguationError as f:
                    pass
        
conditions = ["heart attack","palpitations"] #Search all related pages?
make_filename = lambda aStr: aStr.replace(' ','_') 
for condition in conditions:
    findRelevantArticles(condition,data_path=os.path.join('./data/wikipedia',make_filename(condition)))
