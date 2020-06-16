# -*- coding: utf-8 -*-
#/usr/bin/python2
'''
By kyubyong park. kbpark.linguist@gmail.com.
https://www.github.com/kyubyong/dc_tts
'''

from __future__ import print_function

from hyperparams import Hyperparams as hp
from utils import load_spectrograms
import os
from data_load import load_data
import numpy as np
import tqdm

# Load data
fpaths, _, _ = load_data() # list

for fpath in tqdm.tqdm(fpaths):
    fname, mel, mag = load_spectrograms(fpath)

    folder = "voces_procesadas/{}/".format(hp.voice)
    melsFolder = folder + "mels"
    magsFolder = folder + "mags"

    if not os.path.exists(melsFolder): os.mkdir(melsFolder)
    if not os.path.exists(magsFolder): os.mkdir(magsFolder)

    np.save(melsFolder+"/{}".format(fname.replace("wav", "npy")), mel)
    np.save(magsFolder+"/{}".format(fname.replace("wav", "npy")), mag)