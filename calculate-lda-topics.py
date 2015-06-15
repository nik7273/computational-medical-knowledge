from gensim import corpora, models, similarities
import json
import os

READ = 'r'
CORPUS_FILENAME = 'corpus.json'
data = json.load(open(CORPUS_FILENAME,READ))

sources = ['harrison','wikipedia','braunwald']
keywords = [word.replace(' ','_') for word in open('keywords').read().splitlines()]


for disease in keywords:
	if not os.path.isfile('./corpus-%s.mm'%disease):

		texts = [data[source][disease] for source in data]
		dictionary = corpora.Dictionary(texts)
		dictionary.save('./corpus-%s.dict'%disease)

		corpus = [dictionary.doc2bow(text) for text in texts]
		lsi = models.lsimodel.LsiModel(corpus, num_topics=10)
		lsi.show_topics(num_topics=10,num_words=10)

		corpora.MmCorpus.serialize('./combined-%s.mm'%disease,corpus)
	
	else:
		dictionary = corpora.Dictionary.load('./corpus-%s.dict'%disease)
		corpus = corpus.MmCorpus('./corpus-%s.mm'%disease)

	lda = models.ldamodel.LdaModel(corpus=corpus,id2word=dictionary, passes=20)
	with open('./topics-%s.txt'%disease,'wb') as outfile:
		for topic in lda.print_topics(num_topics=100,num_words=10):
			print>>outfile,topic