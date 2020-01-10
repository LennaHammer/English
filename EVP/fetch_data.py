import re
import json
import requests_html
s = requests_html.HTMLSession()
s.auth = ('englishprofile', 'vocabulary')

ALPHABETA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DOMAIN = "http://vocabulary.englishprofile.org"
assert len(ALPHABETA) == 26


def main1():
    xs = []
    for c in ALPHABETA[:]:
        url = f'http://vocabulary.englishprofile.org/dictionary/word-list/us/a1_c2/{c}'
        xs += [DOMAIN+x.attrs['href']
               for x in s.get(url).html.find('#groupResult li a')]
    # print(xs)
    print(len(xs))
    ys = []
    for x in xs[:]:
        ys += [DOMAIN+y.attrs['href']
               for y in s.get(x).html.find("#result li a")]
    print(len(ys))
    zs = {}
    for y in ys:
        zs[re.sub('#.*$', '', y)] = 1
    json.dump(list(zs.keys()), open("us_wordlist.json",
                                    'w', encoding='utf-8'), indent=" ")
    print(len(zs))
import os
import zipfile
def main2():
    urls = json.load(open("us_wordlist.json", 'r', encoding='utf-8'))
    print(len(urls))
    for i,url in enumerate(urls):
        print(f"[{i}/{len(urls)}]")
        name = re.sub('\?.*$','',os.path.basename(url))+".htm"
        with zipfile.ZipFile("us_words.zip",'a',compression=zipfile.ZIP_LZMA) as zf:
            if name in zf.namelist():
                continue
            doc = s.get(url).html
            html = doc.find('#dictionary_entry')[0].html
            #word = doc.find('#dictionary_entry .head h1')[0].text
            zf.writestr(name,html.encode('utf-8'))

main2()