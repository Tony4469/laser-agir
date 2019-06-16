#!/usr/bin/python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# LASER  Language-Agnostic SEntence Representations
# is a toolkit to calculate multilingual sentence embeddings
# and to use them for document classification, bitext filtering
# and mining
#
# --------------------------------------------------------
#
# Quora Q&A paraphrase detection

import os
import sys
import numpy as np

# get environment
LASER = os.getenv('LASER_AGIR', "/Users/tonyparker/Documents/Python/laser-agir/")

sys.path.append(LASER + '/source')
sys.path.append(LASER + '/source/lib')
from embed import SentenceEncoder, EncodeLoad, EncodeFile
from text_processing import Token, BPEfastApply
from indexing import IndexCreate, IndexSearchMultiple, IndexPrintConfusionMatrix

###############################################################################

print('LASER: similarity search')

print('\nProcessing:')
all_texts = []

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
class Similarity:
    def __init__(self, p_path):
        self.args = Namespace(
                base_dir=os.path.normpath(os.path.join(p_path, './tasks/similarity') ), 
                bpe_codes=os.path.normpath(os.path.join(p_path, './models/93langs.fcodes') ), 
                buffer_size=100, 
                cpu=False, 
                data= os.path.normpath(os.path.join(p_path, './tasks/similarity/dev/input') ), 
                encoder= os.path.normpath(os.path.join(p_path, './models/bilstm.93langs.2018-12-26.pt') ), 
                max_sentences=None, 
                max_tokens=12000, 
                output= os.path.normpath(os.path.join(p_path, './tasks/similarity/embed/output') ), 
                textual=False, 
                verbose=True)
        self.enc = EncodeLoad(self.args)
        out_dir = os.path.dirname(self.args.output)
        if not os.path.exists(out_dir):
            print(' - creating directory {}'.format(out_dir))
            os.mkdir(out_dir)
    
    def launch(self, lang):
        self.args.lang= lang
        
        all_data = []
        all_index = []
        for l in self.args.lang:
            Token(os.path.join(self.args.base_dir, self.args.data + '.' + l),
                  os.path.join(self.args.base_dir, self.args.output + '.tok.' + l),
                  lang=l,
                  romanize=True if l == 'el' else False,
                  lower_case=True,
                  verbose=self.args.verbose, over_write=False)
            BPEfastApply(os.path.join(self.args.base_dir, self.args.output + '.tok.' + l),
                         os.path.join(self.args.base_dir, self.args.output + '.bpe.' + l),
                         self.args.bpe_codes,
                         verbose=self.args.verbose, over_write=False)
            EncodeFile(self.enc,
                       os.path.join(self.args.base_dir, self.args.output + '.bpe.' + l),
                       os.path.join(self.args.base_dir, self.args.output + '.enc.' + l),
                       verbose=self.args.verbose, over_write=False)
            d, idx = IndexCreate(os.path.join(self.args.base_dir, self.args.output + '.enc.' + l),
                                 'FlatL2',
                                 verbose=self.args.verbose, save_index=False)
            all_data.append(d)
            all_index.append(idx)
        
        
        distances, indexes, cosine = IndexSearchMultiple(all_data, all_index, texts=all_texts,
                                  verbose=True, print_errors=False)
        
        print('D', distances)
        print('I', indexes)
        print('cosine', cosine)
        
        return distances, indexes, cosine

