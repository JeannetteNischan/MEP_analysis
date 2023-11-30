import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import glob
from scipy import stats
import pandas as pd
import itertools
from scipy import io
import scipy
import keyboard
import math


# %% Load data
from scipy.io import loadmat
testdata = loadmat('/home/jeanettenischan/Data/data_INTENS_TMS/data/001/post1/IO_ipsilesional.mat')

# %% Plot one trial
testdata.keys()
# %%

