# -*- coding:utf-8 -*-

"""
 gensim使用方法以及例子: http://blog.csdn.net/u014595019/article/details/52218249
 Gensim官方教程翻译: http://blog.csdn.net/questionfish/article/details/46739207
"""

from __future__ import division
import math
import os
import jieba
import jieba.analyse
from gensim import corpora, models, similarities
import sys
sys.path.append("..")
sys.path.append("../..")
# import script
from script.alm_read_write import Almread
import datetime

class BugMatch(object):
    def __init__(self, work_dir, model, fname, mname):
        self.work_dir = work_dir
        self.model = model
        self.fname = fname
        self.mname = mname
        self.origial = []

    def pre_process(self, low_freq_filter=False, label_flag=False):
        if not os.path.exists(self.work_dir + '/deerwester.dict'):
            stopwords_fname = self.work_dir + '/smartstoplist.txt'
            jieba.analyse.set_stop_words(stopwords_fname)
            texts_tokenized = []
            with open(self.fname, 'rb') as fn:
                lines = fn.readlines()
                for tmp in lines:
                    self.origial.append(tmp)
                    tmp = tmp.split('\t')[2].strip()
                    tmp = jieba.analyse.extract_tags(tmp, 10)
                    texts_tokenized.append(tmp)
            texts_filtered = texts_tokenized
            dictionary = corpora.Dictionary(texts_filtered)
            dict_name = self.work_dir + '/deerwester.dict'
            dictionary.save(dict_name)
            corpus = [dictionary.doc2bow(text) for text in texts_filtered]
            #result:[[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)], [(1, 1), (7, 1), (8, 1), (9, 1), (10, 1)]...] <== (id, time)
            # 存入硬盘，以备后需              print one.split('\t')[2].strip()
            corpus_fname = self.work_dir + '/fr_summarys_corpus.mm'
            corpora.MmCorpus.serialize(corpus_fname, corpus)
            tfidf = models.TfidfModel(corpus)#目前只是生成了一个模型，但这是类似于生成器，并不是将对应的corpus转化后的结果
            tfidf.save(self.work_dir + '/tfidfmodel.mm')
        else:
            with open(self.fname, 'rb') as fn:
                lines = fn.readlines()
                for tmp in lines:
                    self.origial.append(tmp)
            dictionary = corpora.Dictionary.load(self.work_dir + '/deerwester.dict')
            corpus = corpora.MmCorpus(self.work_dir + '/fr_summarys_corpus.mm')
            tfidf = models.TfidfModel.load(self.work_dir + '/tfidfmodel.mm')
        # tfidf = models.TfidfModel(corpus)#目前只是生成了一个模型，但这是类似于生成器，并不是将对应的corpus转化后的结果
        # print tfidf
        # tfidf.save(self.work_dir + '/tfidfmodel.mm')

        corpus_tfidf = tfidf[corpus]

        if self.model == "lsi":
            lsi_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
            corpus_tfidf = lsi_model[corpus_tfidf]

        if self.model == "lda":
            lda_model = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=10)
            corpus_tfidf = lda_model[corpus_tfidf]

        # for t in dictionary.token2id.keys():
        #     print t, dictionary.token2id[t] # result:(display 141) <== (word , id)

        # # 余弦相似度查询bug匹配数据
        corpus_simi_matrix = similarities.MatrixSimilarity(corpus_tfidf)
        # test_text = "[SWD_TEST]Project clone for Pixi3-3.5 3G VF".split()
        # summary = "[camera]low memory into the camera settings sd card store click on the photo,camera flash back"
        # test_text = jieba.analyse.extract_tags(summary, 10)
        # # print test_text
        # test_bow = dictionary.doc2bow(test_text)
        # test_tfidf = tfidf[test_bow]
        # test_simi = corpus_simi_matrix[test_tfidf]
        # simi = sorted(enumerate(test_simi), key=lambda x: x[1], reverse=True)
        # # print(list(enumerate(test_simi)))
        # # print simi
        # # print origial
        return dictionary, tfidf, corpus_simi_matrix

    def similar_search(self, data, dictionary, tfidf, corpus_simi_matrix):
        data = data.split('\t')
        bug_id = data[0]
        summary = data[2].strip()
        test_text = jieba.analyse.extract_tags(summary, 10)
        test_bow = dictionary.doc2bow(test_text)
        test_tfidf = tfidf[test_bow]
        test_simi = corpus_simi_matrix[test_tfidf]
        simi = sorted(enumerate(test_simi), key=lambda x: x[1], reverse=True)
        # print(list(enumerate(test_simi)))
        # print simi
        return simi, bug_id

    def match_result(self, simi, fobj = None):
        comment = "<pre>There are some similar bugs below, you can make a reference !\nsimilarity    bug_id    project    summary\n"
        for i in range(len(simi)):
            if i == 1 and float(simi[i][1]) < 0.5:
                if fobj:
                    fobj.write(str(simi[i][1]) + "        " + self.origial[simi[i][0]])
                    fobj.write(str(simi[i+1][1]) + "        " + self.origial[simi[i+1][0]])
                temp = self.origial[simi[i][0]].split('\t', 1)
                temp2 = self.origial[simi[i+1][0]].split('\t', 1)
                comment += str(simi[i][1]) + "    "
                comment += "<a href='https://alm.tclcom.com:7003/im/issues?selection=%s'  target='_Blank'>%s</a>" % (temp[0], temp[0])
                comment += "    " + temp[1]
                comment += str(simi[i+1][1]) + "    "
                comment += "<a href='https://alm.tclcom.com:7003/im/issues?selection=%s'  target='_Blank'>%s</a>" % (temp2[0], temp2[0])
                comment += "    " + temp2[1]
                break
            elif float(simi[i][1]) < 0.5:
                break
            if fobj:
                fobj.write(str(simi[i][1]) + "        " + self.origial[simi[i][0]])
            if i > 0:
                temp = self.origial[simi[i][0]].split('\t', 1)
                comment += str(simi[i][1]) + "    "
                comment += "<a href='https://alm.tclcom.com:7003/im/issues?selection=%s' target='_Blank'>%s</a>" % (temp[0], temp[0])
                comment += "    " + temp[1]
        comment += "</pre>"
        return comment

    def match_process(self):
        match_data = []
        path = self.work_dir + "/match_result.txt"
        fobj=open(path, 'a+')
        with open(self.mname, 'rb') as fn:
            lines = fn.readlines()
            for tmp in lines:
                match_data.append(tmp)
        if match_data == []:
            print "There is no new bug today!"
            fobj.write("\n********************************************************************\n")
            fobj.write("There is no new bug at " + datetime.date.today().strftime("%Y-%m-%d"))
            fobj.write("\n********************************************************************\n")
            fobj.close()
            return
        fobj.write("\n====================================================================\n")
        fobj.write("There are some new bugs' match result below at " + datetime.date.today().strftime("%Y-%m-%d"))
        fobj.write("\n====================================================================\n\n")
        dictionary, tfidf, corpus_simi_matrix = self.pre_process()
        for data in match_data:
            simi, bug_id = self.similar_search(data, dictionary, tfidf, corpus_simi_matrix)
            comment = self.match_result(simi, fobj)
            fobj.write("\n--------------------------------------------------------------------\n")
            # print "******************************"
            # print comment
            self.deliver_comments_to_alm(bug_id, comment)
        fobj.close()
        # For test
        # print comment
        # self.deliver_comments_to_alm(3655095, comment)

    def deliver_comments_to_alm(self, bug_id, add_comment):
        alm = Almread().alm
        arg = {
                'Additional Comments': add_comment,
                }
        resp = alm.editItem(item_id=bug_id, **arg)
        print "Add comment**********************SUCCESS!"

    def web_result_display(self, bug_id):
        alm = Almread(bug_id)
        try:
            bug = alm.read_defect()
        except:
            print "Please input a right number!"
            return "Error"
        data = str(bug_id) + "\t" + bug["project"] + "\t" + bug["summary"]
        dictionary, tfidf, corpus_simi_matrix = self.pre_process()
        simi, bug_id = self.similar_search(data, dictionary, tfidf, corpus_simi_matrix)
        comment = self.match_result(simi)
        return comment


if __name__ == "__main__":
    work_dir = os.getcwd()
    default_fname = work_dir + '/all_bugs_RC.txt'
    match_fname = work_dir + '/new_add_bugs_RC.txt'
    model = "tfidf"
    match = BugMatch(work_dir, model, default_fname, match_fname)
    data = match.match_process()
    # n = "<pre>There are some similar bugs below, you can make a reference !\nsimilarity    bug_id    project    summary\n0.501931   <a href='https://alm.tclcom.com:7003/im/issues?selection=4433947'>4433947</a>   simba6_na   [idol5s simba6 na]</pre>"
    # print n
    # match.deliver_comments_to_alm(3655095, n)
    # print match.web_result_display("3655095")
    print "Done!"
