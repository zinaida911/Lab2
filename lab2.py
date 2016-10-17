#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import zipfile
import json

import nltk

import pymorphy2

from bs4 import BeautifulStoneSoup

import os
import errno


def main (  ): #{
    morph = pymorphy2.MorphAnalyzer()

    while True:
        fileDir = input("Enter dir:")
        try:
            text = get_text(fileDir)
            break
        except IOError as e:
            if e.errno == errno.ENOENT:
                print(e.strerror)
            continue

    #fileDir = 'inputText/1.odt'
    #fileDir = 'inputText/Повести покойного Ивана Петровича Белкина.odt'
    #fileDir = 'inputText/hard.odt'
    #fileDir = 'inputText/EOs.odt'

    text = get_text(fileDir)
    print('Текст файла: ' + text)

    nameAndExt = os.path.basename(fileDir)
    name, ext = os.path.splitext(nameAndExt)

    tokens = nltk.word_tokenize(text)

    tagTokens = []
    for item in tokens:
        tagTokens.append(morph.parse(item)[0])

    print('Количество элементов в исходном тексте: ' + str(len(tagTokens)))

    prepCount = 0
    conjCount = 0
    newTokens = []
    for i in range (0, len(tagTokens),1):
        if 'PREP' in tagTokens[i].tag or 'CONJ' in tagTokens[i].tag:
            if 'PREP' in tagTokens[i].tag:
                prepCount += 1
            if 'CONJ' in tagTokens[i].tag:
                conjCount += 1
    print('Найдено предлогов: ' + str(prepCount) + '   Найдено союзов: ' + str(conjCount))

    for i in range(0, len(tagTokens), 1):
        if not('PREP' in tagTokens[i].tag) and not('CONJ' in tagTokens[i].tag):
            newTokens.append(tokens[i])
    print('Количество элементов в результате: ' + str(len(newTokens)))

    outText = ' '.join(newTokens)

    punctuation =['!', '?', ';', ':', ',', '.', '...']
    for item in punctuation:
        outText = outText.replace(' ' + item, item)
    print('Результат: ' + outText)

    print('Вывод в JSON:')
    outJSON = JObject()
    outJSON.file_name = name
    outJSON.text = outText

    print(outJSON.toJSON())
    outFile = 'outputText/' + name + '.json'

    file = open(outFile, 'w')
    file.write(outJSON.toJSON())
    file.close()
#}

def get_text(fileDir):
    document = zipfile.ZipFile(fileDir)
    textSoup = BeautifulStoneSoup(document.read('content.xml'))
    document.close()
    return textSoup.get_text()

class JObject:
    def toJSON(self):
        return json.dumps(self, default=lambda  o: o.__dict__, ensure_ascii=False, sort_keys=True, indent=4)

main();
