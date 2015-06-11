# -*- coding: utf-8 -*-
#FILE USED FOR TESTING AND DEBUGGING JACCARD/WIKIPEDIA ACCESS CODE

import wikipedia, itertools

articleList = []
articles = wikipedia.search("Heart Attack")
relevant_categories = {'medical','emergencies','disease'}
article = articles[0]
article = wikipedia.page(article)
category_keywords = set(list(itertools.chain.from_iterable([category.lower().split() for category in article.categories])))
if len(category_keywords & relevant_categories) > 0:
    articleList.append(str(article.title))
print articleList
