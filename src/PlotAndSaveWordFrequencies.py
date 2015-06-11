# -*- coding: utf-8 -*-
from plotSave import plot_and_save
from listFreqs import fromPDFtoText, getAndListFreqs

plot_and_save(getAndListFreqs(fromPDFtoText("../Harrison's/STEMI.pdf","STEMITxtFromPDF.txt"), 'STEMI_words', 'listedSTEMIData.txt')["freqs"], getAndListFreqs(fromPDFtoText("../Harrison's/STEMI.pdf","STEMITxtFromPDF.txt"), 'STEMI_words', 'listedSTEMIData.txt')["words"], "Word Count", "Harrisons-STEMI-word-frequencies.png")
plot_and_save(getAndListFreqs(fromPDFtoText("../Harrison's/NSTEMI.pdf","NSTEMITxtFromPDF.txt"), 'NSTEMI_words', 'listedNSTEMIData.txt')["freqs"], getAndListFreqs(fromPDFtoText("../Harrison's/NSTEMI.pdf","NSTEMITxtFromPDF.txt"), 'NSTEMI_words', 'listedNSTEMIData.txt')["words"], "Word Count", "Harrisons-NSTEMI-word-frequencies.png")
plot_and_save(getAndListFreqs(fromPDFtoText("../data.txt","anything.txt"), 'WIKI_words', 'listedWikiData.txt')["freqs"], getAndListFreqs(fromPDFtoText("../data.txt","anything.txt"), 'WIKI_words', 'listedWikiData.txt')["words"], "Word Count", "wikipedia-word-frequencies.png")