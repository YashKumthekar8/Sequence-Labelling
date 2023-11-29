import torch.nn as nn
import torch
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from .wordrep import WordRep
from model.lstm_attention import LSTM_attention, multihead_attention


class WordSequence(nn.Module):
    def __init__(self, data):
        super(WordSequence, self).__init__()
        print("build word sequence feature extractor: %s..."%(data.word_feature_extractor))
        self.gpu = data.HP_gpu
        self.use_char = data.use_char
        # self.batch_size = data.HP_batch_size
        # self.hidden_dim = data.HP_hidden_dim
        self.droplstm = nn.Dropout(data.HP_dropout)
        self.bilstm_flag = data.HP_bilstm
        self.num_of_lstm_layer = data.HP_lstm_layer
        #word embedding
        self.wordrep = WordRep(data)

        self.input_size = data.word_emb_dim
        if self.use_char:
            self.input_size += data.HP_char_hidden_dim
            if data.char_feature_extractor == "ALL":
                self.input_size += data.HP_char_hidden_dim
        # for idx in range(data.feature_num):
        #     self.input_size += data.feature_emb_dims[idx]
        # The LSTM takes word embeddings as inputs, and outputs hidden states
        # with dimensionality hidden_dim.
        if self.bilstm_flag:
            lstm_hidden = data.HP_hidden_dim // 2
        else:
            lstm_hidden = data.HP_hidden_dim

        self.word_feature_extractor = data.word_feature_extractor

        self.lstm_first = nn.LSTM(self.input_size, lstm_hidden, num_layers=1, batch_first=True,
                            bidirectional=self.bilstm_flag)
        self.lstm_layer = nn.LSTM(lstm_hidden * 4, lstm_hidden, num_layers=1, batch_first=True,
                                  bidirectional=self.bilstm_flag)
        self.self_attention_first = multihead_attention(data.HP_hidden_dim,num_heads=data.num_attention_head, dropout_rate=data.HP_dropout, gpu=self.gpu)
        # DO NOT Add dropout at last layer
        self.self_attention_last = multihead_attention(data.HP_hidden_dim,num_heads=1, dropout_rate=0, gpu=self.gpu)
        self.lstm_attention_stack =  nn.ModuleList([LSTM_attention(lstm_hidden,self.bilstm_flag,data) for _ in range(int(self.num_of_lstm_layer)-2)])
        #highway encoding
        #self.highway_encoding = HighwayEncoding(data,data.HP_hidden_dim,activation_function=F.relu)



    def forward(self, word_inputs, word_seq_lengths, char_inputs, char_seq_lengths, char_seq_recover, input_label_seq_tensor):
        """
            input:
                word_inputs: (batch_size, sent_len)
                word_seq_lengths: list of batch_size, (batch_size,1)
                char_inputs: (batch_size*sent_len, word_length)
                char_seq_lengths: list of whole batch_size for char, (batch_size*sent_len, 1)
                char_seq_recover: variable which records the char order information, used to recover char order
                label_size: nubmer of label
            output:
                Variable(batch_size, sent_len, hidden_dim)
        """
        word_represent, label_embs = self.wordrep(word_inputs, word_seq_lengths, char_inputs, char_seq_lengths, char_seq_recover,input_label_seq_tensor)
        #word_represent shape [batch_size, seq_length, word_embedding_dim+char_hidden_dim]
        # word_embs (batch_size, seq_len, embed_size)
        # label_embs = self.highway_encoding(label_embs)
        """
        First LSTM layer (input word only)
        """
        lstm_out = word_represent
        lstm_out = pack_padded_sequence(input=lstm_out, lengths=word_seq_lengths.cpu().numpy(), batch_first=True)
        hidden = None
        lstm_out, hidden = self.lstm_first(lstm_out, hidden)
        lstm_out, _ = pad_packed_sequence(lstm_out)
        # shape [seq_len, batch, hidden_size]
        lstm_out = self.droplstm(lstm_out.transpose(1, 0))
        attention_label = self.self_attention_first(lstm_out, label_embs, label_embs)
        # shape [batch_size, seq_length, embedding_dim]
        lstm_out = torch.cat([lstm_out, attention_label], -1)
        #shape [batch_size, seq_length, embedding_dim + label_embeeding_dim]

        # LAN layer
        for layer in self.lstm_attention_stack:
            lstm_out = layer(lstm_out, label_embs, word_seq_lengths, hidden)
        """
        Last Layer 
        Attention weight calculate loss
        """
        lstm_out = pack_padded_sequence(input=lstm_out, lengths=word_seq_lengths.cpu().numpy(), batch_first=True)
        lstm_out, hidden = self.lstm_layer(lstm_out, hidden)
        lstm_out, _ = pad_packed_sequence(lstm_out)
        lstm_out = self.droplstm(lstm_out.transpose(1, 0))
        lstm_out = self.self_attention_last(lstm_out, label_embs, label_embs, True)
        return lstm_out

