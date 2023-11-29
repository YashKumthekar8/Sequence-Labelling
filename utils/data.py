# -*- coding: utf-8 -*-
# @Author: Jie
# @Date:   2017-06-14 17:34:32
# @Last Modified by:   Jie Yang,     Contact: jieynlp@gmail.com
# @Last Modified time: 2018-06-22 00:01:47
from __future__ import print_function
from __future__ import absolute_import
import sys
from .alphabet import Alphabet
from .functions import *

try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle


START = "</s>"
UNKNOWN = "</unk>"
PADDING = "</pad>"

class Data:
    def __init__(self):
        self.MAX_SENTENCE_LENGTH = 250
        self.MAX_WORD_LENGTH = -1
        self.number_normalized = True
        self.norm_word_emb = False
        self.norm_char_emb = False
        self.word_alphabet = Alphabet('word')
        self.char_alphabet = Alphabet('character')

        # self.feature_name = []
        # self.feature_alphabets = []
        # self.feature_num = len(self.feature_alphabets)
        # self.feat_config = None


        self.label_alphabet = Alphabet('label',True)
        self.tagScheme = "NoSeg" ## BMES/BIO

        self.seg = True

        ### I/O
        self.train_dir = None
        self.dev_dir = None
        self.test_dir = None
        self.raw_dir = None

        self.decode_dir = None
        self.dset_dir = None ## data vocabulary related file
        self.model_dir = None ## model save  file
        self.load_model_dir = None ## model load file

        self.word_emb_dir = None
        self.char_emb_dir = None
        # self.feature_emb_dirs = []

        self.train_texts = []
        self.dev_texts = []
        self.test_texts = []
        self.raw_texts = []

        self.train_Ids = []
        self.dev_Ids = []
        self.test_Ids = []
        self.raw_Ids = []

        self.pretrain_word_embedding = None
        self.pretrain_char_embedding = None
        # self.pretrain_feature_embeddings = []

        self.label_size = 0
        self.word_alphabet_size = 0
        self.char_alphabet_size = 0
        self.label_alphabet_size = 0
        # self.feature_alphabet_sizes = []
        # self.feature_emb_dims = []
        # self.norm_feature_embs = []
        self.word_emb_dim = 50
        self.char_emb_dim = 30

        ###Networks
        self.word_feature_extractor = "LSTM" ## "LSTM"/"CNN"/"GRU"/
        self.use_char = True
        self.char_feature_extractor = "CNN" ## "LSTM"/"CNN"/"GRU"/None
        self.use_crf = True
        self.nbest = None

        ## Training
        self.average_batch_loss = False
        self.optimizer = "SGD" ## "SGD"/"AdaGrad"/"AdaDelta"/"RMSProp"/"Adam"
        self.status = "train"
        ### Hyperparameters
        self.HP_cnn_layer = 4
        self.HP_iteration = 100
        self.HP_batch_size = 10
        self.HP_char_hidden_dim = 50
        self.HP_hidden_dim = 200
        self.HP_dropout = 0.5
        self.HP_lstm_layer = 1
        self.HP_bilstm = True

        self.HP_gpu = False
        self.HP_lr = 0.015
        self.HP_lr_decay = 0.05
        self.HP_clip = None
        self.HP_momentum = 0
        self.HP_l2 = 1e-8

    def show_data_summary(self):
        print("++"*50)
        print("DATA SUMMARY START:")
        print(" I/O:")
        print("     Tag          scheme: %s"%(self.tagScheme))
        print("     MAX SENTENCE LENGTH: %s"%(self.MAX_SENTENCE_LENGTH))
        print("     MAX   WORD   LENGTH: %s"%(self.MAX_WORD_LENGTH))
        print("     Number   normalized: %s"%(self.number_normalized))
        print("     Word  alphabet size: %s"%(self.word_alphabet_size))
        print("     Char  alphabet size: %s"%(self.char_alphabet_size))
        print("     Label alphabet size: %s"%(self.label_alphabet_size))
        print("     Word embedding  dir: %s"%(self.word_emb_dir))
        print("     Char embedding  dir: %s"%(self.char_emb_dir))
        print("     Word embedding size: %s"%(self.word_emb_dim))
        print("     Char embedding size: %s"%(self.char_emb_dim))
        print("     Norm   word     emb: %s"%(self.norm_word_emb))
        print("     Norm   char     emb: %s"%(self.norm_char_emb))
        print("     Train  file directory: %s"%(self.train_dir))
        print("     Dev    file directory: %s"%(self.dev_dir))
        print("     Test   file directory: %s"%(self.test_dir))
        print("     Raw    file directory: %s"%(self.raw_dir))
        print("     Dset   file directory: %s"%(self.dset_dir))
        print("     Model  file directory: %s"%(self.model_dir))
        print("     Loadmodel   directory: %s"%(self.load_model_dir))
        print("     Decode file directory: %s"%(self.decode_dir))
        print("     Train instance number: %s"%(len(self.train_texts)))
        print("     Dev   instance number: %s"%(len(self.dev_texts)))
        print("     Test  instance number: %s"%(len(self.test_texts)))
        print("     Raw   instance number: %s"%(len(self.raw_texts)))
        # print("     FEATURE num: %s"%(self.feature_num))
        # for idx in range(self.feature_num):
        #     print("         Fe: %s  alphabet  size: %s"%(self.feature_alphabets[idx].name, self.feature_alphabet_sizes[idx]))
        #     print("         Fe: %s  embedding  dir: %s"%(self.feature_alphabets[idx].name, self.feature_emb_dirs[idx]))
        #     print("         Fe: %s  embedding size: %s"%(self.feature_alphabets[idx].name, self.feature_emb_dims[idx]))
        #     print("         Fe: %s  norm       emb: %s"%(self.feature_alphabets[idx].name, self.norm_feature_embs[idx]))
        print(" "+"++"*20)
        print(" Model Network:")
        print("     Model        use_crf: %s"%(self.use_crf))
        print("     Model word extractor: %s"%(self.word_feature_extractor))
        print("     Model       use_char: %s"%(self.use_char))
        if self.use_char:
            print("     Model char extractor: %s"%(self.char_feature_extractor))
            print("     Model char_hidden_dim: %s"%(self.HP_char_hidden_dim))
        print(" "+"++"*20)
        print(" Training:")
        print("     Optimizer: %s"%(self.optimizer))
        print("     Iteration: %s"%(self.HP_iteration))
        print("     BatchSize: %s"%(self.HP_batch_size))
        print("     Average  batch   loss: %s"%(self.average_batch_loss))

        print(" "+"++"*20)
        print(" Hyperparameters:")

        print("     Hyper              lr: %s"%(self.HP_lr))
        print("     Hyper        lr_decay: %s"%(self.HP_lr_decay))
        print("     Hyper         HP_clip: %s"%(self.HP_clip))
        print("     Hyper        momentum: %s"%(self.HP_momentum))
        print("     Hyper              l2: %s"%(self.HP_l2))
        print("     Hyper      hidden_dim: %s"%(self.HP_hidden_dim))
        print("     Hyper         dropout: %s"%(self.HP_dropout))
        print("     Hyper      lstm_layer: %s"%(self.HP_lstm_layer))
        print("     Hyper          bilstm: %s"%(self.HP_bilstm))
        print("     Hyper             GPU: %s"%(self.HP_gpu))
        print("DATA SUMMARY END.")
        print("++"*50)
        sys.stdout.flush()


    # def initial_feature_alphabets(self):
    #     items = open(self.train_dir,'r').readline().strip('\n').split()
    #     total_column = len(items)
    #     print(items)
    #     if total_column > 2:
    #         for idx in range(1, total_column-1):
    #             feature_prefix = items[idx].split(']',1)[0]+"]"
    #             self.feature_alphabets.append(Alphabet(feature_prefix))
    #             self.feature_name.append(feature_prefix)
    #             print("Find feature: ", feature_prefix)
    #     self.feature_num = len(self.feature_alphabets)
    #     self.pretrain_feature_embeddings = [None]*self.feature_num
    #     self.feature_emb_dims = [20]*self.feature_num
    #     self.feature_emb_dirs = [None]*self.feature_num
    #     self.norm_feature_embs = [False]*self.feature_num
    #     self.feature_alphabet_sizes = [0]*self.feature_num
    #     if self.feat_config:
    #         for idx in range(self.feature_num):
    #             if self.feature_name[idx] in self.feat_config:
    #                 self.feature_emb_dims[idx] = self.feat_config[self.feature_name[idx]]['emb_size']
    #                 self.feature_emb_dirs[idx] = self.feat_config[self.feature_name[idx]]['emb_dir']
    #                 self.norm_feature_embs[idx] = self.feat_config[self.feature_name[idx]]['emb_norm']
        # exit(0)
        


    def build_alphabet(self, input_file):
        in_lines = open(input_file,'r', encoding='utf8').readlines()
        for line in in_lines:
            pairs = line.strip().split()
            if len(line) < 5:
                continue
            word = pairs[0]
            if sys.version_info[0] < 3:
                word = word.decode('utf-8')
            if self.number_normalized:
                word = normalize_word(word)
            label = pairs[-1]
            self.label_alphabet.add(label)
            self.word_alphabet.add(word)
            for char in word:
                self.char_alphabet.add(char)
            
                
        self.word_alphabet_size = self.word_alphabet.size()
        self.char_alphabet_size = self.char_alphabet.size()
        self.label_alphabet_size = self.label_alphabet.size()
        startS = False
        startB = False
        for label,_ in self.label_alphabet.iteritems():
            if "S-" in label.upper():
                startS = True
            elif "B-" in label.upper():
                startB = True
        if startB:
            if startS:
                self.tagScheme = "BMES"
            else:
                self.tagScheme = "BIO"
        # print(startB, startS)
        # print(self.tagScheme)
        


    def fix_alphabet(self):
        self.word_alphabet.close()
        self.char_alphabet.close()
        self.label_alphabet.close()
        # for idx in range(self.feature_num):
        #     self.feature_alphabets[idx].close()


    def build_pretrain_emb(self):
        if self.word_emb_dir:
            print("Load pretrained word embedding, norm: %s, dir: %s"%(self.norm_word_emb, self.word_emb_dir))
            self.pretrain_word_embedding, self.word_emb_dim = build_pretrain_embedding(self.word_emb_dir, self.word_alphabet, self.word_emb_dim, self.norm_word_emb)
        if self.char_emb_dir:
            print("Load pretrained char embedding, norm: %s, dir: %s"%(self.norm_char_emb, self.char_emb_dir))
            self.pretrain_char_embedding, self.char_emb_dim = build_pretrain_embedding(self.char_emb_dir, self.char_alphabet, self.char_emb_dim, self.norm_char_emb)
        # for idx in range(self.feature_num):
        #     if self.feature_emb_dirs[idx]:
        #         print("Load pretrained feature %s embedding:, norm: %s, dir: %s"%(self.feature_name[idx], self.norm_feature_embs[idx], self.feature_emb_dirs[idx]))
        #         self.pretrain_feature_embeddings[idx], self.feature_emb_dims[idx] = build_pretrain_embedding(self.feature_emb_dirs[idx], self.feature_alphabets[idx], self.feature_emb_dims[idx], self.norm_feature_embs[idx])


    def generate_instance(self, name):
        self.fix_alphabet()
        if name == "train":
            self.train_texts, self.train_Ids = read_instance(self.train_dir, self.word_alphabet, self.char_alphabet, self.label_alphabet, self.number_normalized, self.MAX_SENTENCE_LENGTH)
            # print(self.train_texts, self.train_Ids)
        elif name == "dev":
            self.dev_texts, self.dev_Ids = read_instance(self.dev_dir, self.word_alphabet, self.char_alphabet, self.label_alphabet, self.number_normalized, self.MAX_SENTENCE_LENGTH)
        elif name == "test":
            self.test_texts, self.test_Ids = read_instance(self.test_dir, self.word_alphabet, self.char_alphabet, self.label_alphabet, self.number_normalized, self.MAX_SENTENCE_LENGTH)
        elif name == "raw":
            self.raw_texts, self.raw_Ids = read_instance(self.raw_dir, self.word_alphabet, self.char_alphabet, self.label_alphabet, self.number_normalized, self.MAX_SENTENCE_LENGTH)
        else:
            print("Error: you can only generate train/dev/test instance! Illegal input:%s"%(name))


    def write_decoded_results(self, predict_results, name):
        fout = open(self.decode_dir,'w')
        sent_num = len(predict_results)
        content_list = []
        if name == 'raw':
           content_list = self.raw_texts
        elif name == 'test':
            content_list = self.test_texts
        elif name == 'dev':
            content_list = self.dev_texts
        elif name == 'train':
            content_list = self.train_texts
        else:
            print("Error: illegal name during writing predict result, name should be within train/dev/test/raw !")
        assert(sent_num == len(content_list))
        for idx in range(sent_num):
            sent_length = len(predict_results[idx])
            for idy in range(sent_length):
                ## content_list[idx] is a list with [word, char, label]
                fout.write(content_list[idx][0][idy].encode('utf-8') + " " + predict_results[idx][idy] + '\n')
            fout.write('\n')
        fout.close()
        print("Predict %s result has been written into file. %s"%(name, self.decode_dir))


    def load(self,data_file):
        f = open(data_file, 'rb')
        tmp_dict = pickle.load(f)
        f.close()
        self.__dict__.update(tmp_dict)

    def save(self,save_file):
        f = open(save_file, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()



    def write_nbest_decoded_results(self, predict_results, pred_scores, name):
        ## predict_results : [whole_sent_num, nbest, each_sent_length]
        ## pred_scores: [whole_sent_num, nbest]
        fout = open(self.decode_dir,'w')
        sent_num = len(predict_results)
        content_list = []
        if name == 'raw':
           content_list = self.raw_texts
        elif name == 'test':
            content_list = self.test_texts
        elif name == 'dev':
            content_list = self.dev_texts
        elif name == 'train':
            content_list = self.train_texts
        else:
            print("Error: illegal name during writing predict result, name should be within train/dev/test/raw !")
        assert(sent_num == len(content_list))
        assert(sent_num == len(pred_scores))
        for idx in range(sent_num):
            sent_length = len(predict_results[idx][0])
            nbest = len(predict_results[idx])
            score_string = "# "
            for idz in range(nbest):
                score_string += format(pred_scores[idx][idz], '.4f')+" "
            fout.write(score_string.strip() + "\n")

            for idy in range(sent_length):
                try:  # Will fail with python3
                    label_string = content_list[idx][0][idy].encode('utf-8') + " "
                except:
                    label_string = content_list[idx][0][idy] + " "
                for idz in range(nbest):
                    label_string += predict_results[idx][idz][idy]+" "
                label_string = label_string.strip() + "\n"
                fout.write(label_string)
            fout.write('\n')
        fout.close()
        print("Predict %s %s-best result has been written into file. %s"%(name,nbest, self.decode_dir))


    def read_config(self,args):

        ## read data:


        self.train_dir = args.train_dir

        self.dev_dir = args.dev_dir

        self.test_dir = args.test_dir

        self.model_dir = args.model_dir

        self.word_emb_dir = args.word_emb_dir

        self.norm_word_emb = str2bool(args.norm_word_emb)

        self.norm_char_emb = str2bool(args.norm_char_emb)

        self.number_normalized = str2bool(args.number_normalized)

        self.seg = args.seg

        self.word_emb_dim = int(args.word_emb_dim)

        self.char_emb_dim = int(args.char_emb_dim)

        self.use_crf = args.use_crf

        self.use_char = args.use_char

        self.word_feature_extractor = args.word_seq_feature

        self.char_feature_extractor = args.char_seq_feature

        ## read training setting:

        self.optimizer = args.optimizer

        self.average_batch_loss = args.ave_batch_loss

        self.status = args.status

        self.HP_cnn_layer = int(args.cnn_layer)

        self.HP_iteration = int(args.iteration)

        self.HP_batch_size = int(args.batch_size)

        self.HP_char_hidden_dim = int(args.char_hidden_dim)

        self.HP_hidden_dim = int(args.hidden_dim)

        self.HP_dropout = float(args.dropout)

        self.HP_lstm_layer = int(args.lstm_layer)

        self.HP_bilstm = args.bilstm

        self.HP_gpu = args.gpu

        self.HP_lr = float(args.learning_rate)

        self.HP_lr_decay = float(args.lr_decay)

        self.HP_momentum = float(args.momentum)

        self.HP_l2 = float(args.l2)

        self.clip_grad = float(args.clip_grad)

        self.label_embedding_scale = float(args.label_embedding_scale)

        self.num_attention_head = int(args.num_attention_head)

        self.whether_clip_grad = str2bool(args.whether_clip_grad)

        ##
        # self.MAX_SENTENCE_LENGTH = int(args.MAX_SENTENCE_LENGTH)
        #
        # self.MAX_WORD_LENGTH = int(args.MAX_WORD_LENGTH )



# def config_file_to_dict(input_file):
#     config = {}
#     fins = open(input_file,'r').readlines()
#     for line in fins:
#         if len(line) > 0 and line[0] == "#":
#             continue
#         if "=" in line:
#             pair = line.strip().split('#',1)[0].split('=',1)
#             item = pair[0]
#             if item=="feature":
#                 if item not in config:
#                     feat_dict = {}
#                     config[item]= feat_dict
#                 feat_dict = config[item]
#                 new_pair = pair[-1].split()
#                 feat_name = new_pair[0]
#                 one_dict = {}
#                 one_dict["emb_dir"] = None
#                 one_dict["emb_size"] = 10
#                 one_dict["emb_norm"] = False
#                 if len(new_pair) > 1:
#                     for idx in range(1,len(new_pair)):
#                         conf_pair = new_pair[idx].split('=')
#                         if conf_pair[0] == "emb_dir":
#                             one_dict["emb_dir"]=conf_pair[-1]
#                         elif conf_pair[0] == "emb_size":
#                             one_dict["emb_size"]=int(conf_pair[-1])
#                         elif conf_pair[0] == "emb_norm":
#                             one_dict["emb_norm"]=str2bool(conf_pair[-1])
#                 feat_dict[feat_name] = one_dict
#                 # print "feat",feat_dict
#             else:
#                 if item in config:
#                     print("Warning: duplicated config item found: %s, updated."%(pair[0]))
#                 config[item] = pair[-1]
#     return config


def str2bool(string):
    if string == "True" or string == "true" or string == "TRUE":
        return True
    else:
        return False