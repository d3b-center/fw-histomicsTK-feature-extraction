import histomicstk as htk
from glob import glob
import skimage
import os
import numpy as np

import matplotlib.pyplot as plt

# create stain to color map
stain_color_map = htk.preprocessing.color_deconvolution.stain_color_map
print('stain_color_map:', stain_color_map, sep='\n')
# specify stains of input image
stains = ['hematoxylin',  # nuclei stain
          'eosin',        # cytoplasm stain
          'null']         # set to null if input contains only two stains

# create stain matrix
W = np.array([stain_color_map[st] for st in stains]).T

def HandE_deconvolve(path_to_image, output_dir):
# perform standard color deconvolution
    # load image
    im_nuclei = skimage.io.imread(path_to_image)
    # deconvolve color
    im_stains = htk.preprocessing.color_deconvolution.color_deconvolution(im_nuclei, W)
    # get nuclei/hematoxylin channel
    im_nuclei_stain = im_stains[0][:, :, 0]
    im_eosin_stain = im_stains[0][:, :, 1]
    # save to disk
    skimage.io.imsave(os.path.join(output_dir, 'hematoxylin.png'), im_nuclei_stain)
    skimage.io.imsave(os.path.join(output_dir, 'eosin.png'), im_eosin_stain)
