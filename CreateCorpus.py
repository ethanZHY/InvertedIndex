import os
from bs4 import BeautifulSoup
import re

# This is the file directory where the corpus is
directory = r'pages/'

def corpusHelper(directory):
    filelist = os.listdir(directory)
    for file in filelist:
        inpath = directory + file
        page = open(inpath,'r')
        source_code = page.read()
        page.close()
        soup = BeautifulSoup(source_code, "html.parser")
        head1 = soup.find('h1').get_text()
        fx = open(r'raw/' + file, 'w')
        fx.write(head1.lower() + ' ')

        content = soup.find('div', {'id': 'mw-content-text'})
        for paragraph in content.findAll('p'):
            for sup in paragraph.findAll('sup'):
                sup.replace_with(r' ')
            for ea in paragraph.findAll('a',{'class':'external autonumber'}):
                ea.replace_with(r' ')
            for span in paragraph.findAll('span',{'class':'mwe-math-element'}):
                span.replace_with(r' ')
            paragraph = paragraph.get_text() + ' '
            paragraph = paragraph.lower()
            paragraph = re.sub('[;\\\\\'\"/\n_&)\[\]+=!(`~><]', "", paragraph)
            paragraph = re.sub(',\s', ' ', paragraph)
            paragraph = re.sub('\.\s', ' ', paragraph)
            paragraph = re.sub(':\s', ' ', paragraph)


        # deal with, such as U.S
            matchObj = re.search('\D\.\D',paragraph)
            if matchObj:
                tmp = re.sub('\.', '', matchObj.group())
                paragraph = re.sub('\D\.\D', tmp, paragraph)

            matchObj = re.search('\.[a-z]', paragraph)
            if matchObj:
                tmp = re.sub('\.', ' ', matchObj.group())
                paragraph = re.sub('\.[a-z]', tmp, paragraph)

            # print(paragraph)
            fx.write(paragraph)
        fx.close()
        print(head1)



corpusHelper(directory)