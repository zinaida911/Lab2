#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import zipfile
from xml.dom.minidom import *
import json

import nltk
from nltk import word_tokenize

import pymorphy2

from bs4 import BeautifulStoneSoup

import os
import errno


def main (  ): #{
    morph = pymorphy2.MorphAnalyzer()

    #fileDir = 'inputText/1.odt'
    #fileDir = 'inputText/Повести покойного Ивана Петровича Белкина.odt'
    #fileDir = 'inputText/hard.odt'
    fileDir = 'inputText/EOs.odt'

    text = get_text(fileDir)
    print(text)

    nameAndExt = os.path.basename(fileDir)
    name, ext = os.path.splitext(nameAndExt)


    tokens = nltk.word_tokenize(text)
    print(tokens)

    #tagTokens = nltk.pos_tag(tokens)

    tagTokens = []
    for item in tokens:
        tagTokens.append(morph.parse(item)[0])

    #print(tagTokens)
    print(len(tagTokens))

    #for item in tagTokens:
    #   print(item.word +'  ' + morph.lat2cyr(item.tag))
    prepCount = 0
    conjCount = 0
    newTokens = []
    for i in range (0, len(tagTokens),1):
        if 'PREP' in tagTokens[i].tag or 'CONJ' in tagTokens[i].tag:
            if 'PREP' in tagTokens[i].tag:
                prepCount += 1
            if 'CONJ' in tagTokens[i].tag:
                conjCount += 1
    print('Найдено предогов: ' + str(prepCount) + '   Найдено союзов: ' + str(conjCount))

    for i in range(0, len(tagTokens), 1):
        if not('PREP' in tagTokens[i].tag) and not('CONJ' in tagTokens[i].tag):
            newTokens.append(tokens[i])

    outText = ' '.join(newTokens)

    punctuation =['!', '?', ';', ':', ',', '.', '...']
    for item in punctuation:
        outText = outText.replace(' ' + item, item)
    print(outText)
    #for item in newTokens:
    #    print(item)

    #print(len(newTokens))
    #print(newTokens)


    #print(tagTokens)

    #print (len(tokens))




    #JSON OUT!!!
    outJSON = JObject()
    outJSON.file_name = name
    outJSON.text = outText

    #for i in range (0, len(text), 1):
     #   outJSON.paragraph = text[i]

    print(outJSON.toJSON())
    #print(outJSON.toJSON().encode('utf8'))

    #print(json.dumps(createJSONstring(text, name), sort_keys=True, indent=4))
    #print(json.dumps({'4':5,'6':7}, sort_keys=True, indent=4))
    #print(json.dumps(createJSONstring(text,name),  sort_keys=True, indent=4))

#}

def get_text(fileDir):
    document = zipfile.ZipFile(fileDir)
    #xml_content = document.read('content.xml')
    #document.close()


    #xml = parse(document.)
    #xml = parse('inputText/content.xml')
    #print(document.filelist)
    #print(document.open('content.xml'))
    xml = parse(document.open('content.xml'))

    textSoup = BeautifulStoneSoup(document.read('content.xml'))
    #print(textSoup.prettify())
    #print(textSoup.get_text())

    document.close()
    """
    officeText = xml.getElementsByTagName('office:text')

    textFromDoc = []

    if len((officeText[0].childNodes)) != 0:
        for officeNode in officeText[0].childNodes:
            if len(officeNode.childNodes) != 0:
                for nextNode1 in officeNode.childNodes:
                    if len(nextNode1.childNodes) == 0:
                        if nextNode1.nodeValue == None:
                            textFromDoc.append(' ')
                        else:
                            textFromDoc.append(nextNode1.nodeValue)
                    else:
                        for nextNode2 in  nextNode1.childNodes:
                            if len(nextNode2.childNodes) == 0:
                                textFromDoc.append(nextNode2.nodeValue)
    """

    #for node in text:
        #textFromDoc.append(getTextFromTag(node))
        #print(getTextFromTag(node))

    return textSoup.get_text()

def getTextFromTag(node):
    if len(node.childNodes) != 0:
        if node.childNodes[0].nodeValue == None:
            return getTextFromTag(node.childNodes[0])
        else:
            return node.childNodes[0].nodeValue
    else:
        return '\n'

"""
def createJSONstring(text, fileName):
    string = '{ \'file_name\':  \'' + fileName + '\', \'paragraph\': {'
    for i in range (0, len(text), 1):
        if i == len(text)-1:
            string += ' \'' + str(i+1) + '\': \'' + text[i] + '\''
        else:
            string += ' \'' + str(i+1) + '\': \'' + text[i] + '\','
    string += '}, }'
    print(string)
    return string
"""

class JObject:
    def toJSON(self):
        return json.dumps(self, default=lambda  o: o.__dict__, ensure_ascii=False, sort_keys=True, indent=4)

main();
