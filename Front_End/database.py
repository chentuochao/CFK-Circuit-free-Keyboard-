import nltk
import random
import numpy as np 
from nltk.corpus import inaugural

#英文单词中较少出现的字母包括 j k q v x z (低于1%) 

def get_sentences():
    '''获得语料库中的句子，输出成sectence'''
    '''需要调用这个函数'''
    articles = inaugural.fileids()
    sentences = []
    for i in articles:
        article = inaugural.sents(i)
        sentences = sentences + list(article)
    return sentences

def random_give_sentence(sentences):
    '''随机给出一个语料库中的句子'''
    index = int(random.random()*5050)
    sentence = sentences[index]
    sentence = " ".join(sentence)
    return sentence

def adaptive_give_sentence(rare_dict,alphabet):
    '''给出比较稀有字母对应的句子'''
    sentences = rare_dict[alphabet]
    index = int(random.random()*len(sentences))
    sentence = sentences[index]
    sentence = " ".join(sentence)
    return sentence

def generate_rare_dict(sentences):
    '''给出稀有字母的列表'''
    '''需要调用这个函数'''
    zlist = []
    jlist = []
    klist = []
    qlist = []
    vlist = []
    xlist = []
    for sentence in sentences:
        for words in sentence:
            for letter in words:
                if letter == 'z':
                    zlist.append(sentence)
                if letter == 'j':
                    jlist.append(sentence)
                if letter == 'k':
                    klist.append(sentence)
                if letter == 'q':
                    qlist.append(sentence)
                if letter == 'v':
                    vlist.append(sentence)
                if letter == 'x':
                    xlist.append(sentence)
    rare_dict = {'z':zlist,'j':jlist,'k':klist,'q':qlist,'v':vlist,'x':xlist}
    return rare_dict

def package_give_sentence(sentences,rare_dict):
    '''规划给出的句子，尽量多给出稀有字节的句子，可以后期再调整'''
    '''需要调用这个函数'''
    miaomiao = int(random.random()/0.001)
    if miaomiao == 1:
        return 'susu budiubudiude' #彩蛋
    flag = int(random.random()/0.1)
    if flag == 1:
        return adaptive_give_sentence(rare_dict,'j')
    elif flag == 2:
        return adaptive_give_sentence(rare_dict,'z')
    elif flag == 3:
        return adaptive_give_sentence(rare_dict,'k')
    elif flag == 4:
        return adaptive_give_sentence(rare_dict,'q')
    elif flag == 5:
        return adaptive_give_sentence(rare_dict,'v')
    elif flag == 6:
        return adaptive_give_sentence(rare_dict,'x')
    else:
        return random_give_sentence(sentences)


