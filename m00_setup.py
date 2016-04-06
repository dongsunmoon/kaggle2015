import dicom, lmdb, cv2, re, sys
import os, fnmatch, shutil, subprocess
from IPython.utils import io
import numpy as np
np.random.seed(1234)
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore') # we ignore a RuntimeWarning produced from dividing by zero

CAFFE_ROOT = "/home/moon/caffe/"
caffe_path = os.path.join(CAFFE_ROOT, "python")
if caffe_path not in sys.path:
    sys.path.insert(0, caffe_path)

import caffe

print("\nSuccessfully imported packages, hooray!\n")

from skimage import transform


def diff_images(images):
    images = np.array(images)
    diff = np.zeros([29,128,128])
    for i in range(29):
        diff[i] = np.absolute(images[i] - images[i+1])
    return diff
