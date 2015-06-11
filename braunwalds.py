# -*- coding: utf-8 -*-
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

from awesome_print import ap

def pdfparser(data):
    fp = file(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'latin-1'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue() 
    return data

conditions = {'heart_attack':{'NSTEMIb.pdf','STEMI_diagnosis.pdf','STEMI_management.pdf'},
              'palpitations':['genetics_of_cardiac_arrhythmias.pdf','genesis_of_cardiac_arrhythmias.pdf','diagnosis_of_cardiac_arrhythmias.pdf',
                                'therapy_for_cardiac_arrhythmias.pdf']}
for condition in conditions:
    for pdf in conditions[condition]:
        with open(os.path.join('./data/braunwald',condition,pdf.replace('pdf','txt')),'wb') as outfile:
            print>>outfile,pdfparser(pdf)
