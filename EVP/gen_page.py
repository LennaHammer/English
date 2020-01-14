import zipfile
import pyquery
import re
import json
import os
import pandas as pd
import requests_html
items = []
with zipfile.ZipFile('us_words.zip','r') as zf:
    for name in zf.namelist()[:]:
        html = zf.open(name,'r').read().decode('utf-8')
        html = re.sub(r'<b\s+class="b".*?>(.+?)</b>',r'`\1`',html,flags=re.DOTALL)
        doc = requests_html.HTML(html=html)
        #doc = pyquery.PyQuery(html)
        #print(repr(doc.find('.head h1')))
        word = doc.find('.head h1')[0].text
        pron = ' '.join(list(x.text for x in doc.find('.head .pron')))
        #assert '!!' not in pron, word
        #print(word)
        item = {'word':word}
        print(word)
        for posblock in doc.find('.posblock'):
            poses = [x.text for x in posblock.find('.posblock > .posgram')] # phrasal verb
            pos = ' '.join({x:1 for x in poses}.keys())
            pos = re.sub(r"\s+",' ',pos)
            #pos ='!!!'.join(x.text for x in posblock.find('.posgram'))
            #if len(poses)>1:
            #    print([x.text for x in poses])
            #assert len(posblock.find('.posgram'))>=1, [word, pos]
            #pos = posblock.find('.posgram')[0].text if poses else '' 
            #print(pos)
            for gwblock in posblock.find('.posblock > .gwblock, .phrasal_verb > .gwblock'):
                if 'class="phraserec"' in gwblock.html:
                    # inclined to do sth http://vocabulary.englishprofile.org/dictionary/show/us/US3375947
                    pass
                gw = '!!'.join([x.text for x in gwblock.find('h3')])
                assert '!!' not in gw, word
                #print(gwblock.text)
                for sense in gwblock.find('.sense'):
                    gwblock = None
                    assert len(sense.find('.def'))==1,word+" "+name+sense.text
                    freq = sense.find('[class|=freq]')
                    assert len(freq)==1
                    freq = freq[0].text
                    define = sense.find('.def')[0].text
                    examples = '|'.join(x.text.strip() for x in sense.find('.examp'))
                    items.append({'word':word,'pos':pos,'pron':pron, 'gw':gw,'freq':freq,'def':define,'example':examples})
        #items.append(item)

df = pd.DataFrame(items)
df=df.sort_values(by=['freq','word'],kind='heapsort')
df.to_csv('words.tsv',sep="\t",index=False,quoting=3)