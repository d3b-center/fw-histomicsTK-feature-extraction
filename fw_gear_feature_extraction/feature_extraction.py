import histomicstk as htk
import skimage
import os
import numpy as np

def get_path_features(path_to_mask, output_dir):
    out_file_path = os.path.join(output_dir, 'path_feats.csv')

    # load binary mask
    im_label = skimage.io.imread(path_to_mask)

    # if the input is binary
    if len(np.unique(im_label)) == 2:
        # assign unique ID to each object (nucleus)
        im_label = skimage.measure.label(im_label)

    # if the input is 3 channels, convert to 1 channel of IDs
    if im_label.shape[-1] == 3:
        red = im_label[:,:,0]
        green = im_label[:,:,1]
        blue = im_label[:,:,2]
        im_label = (red * 65536) + (green * 256) + blue 

    # load corresponding images
    path_to_image = os.path.join(output_dir, 'hematoxylin.png')
    im_nuclei = skimage.io.imread(path_to_image)
    path_to_image = os.path.join(output_dir, 'eosin.png')
    im_cytoplasm = skimage.io.imread(path_to_image)

    # feature extraction
    features = htk.features.compute_nuclei_features(im_label, im_nuclei=im_nuclei, im_cytoplasm=im_cytoplasm )
                                                    # morphometry_features_flag=False, \
                                                    # fsd_features_flag=True, \
                                                    # intensity_features_flag=True, \
                                                    # gradient_features_flag=True, \
                                                    # haralick_features_flag=True)
    # rprops = skimage.measure.regionprops( im_label )
    # htk.features.compute_morphometry_features(im_label, rprops=rprops)
    # features = features.drop(columns=['Label', 'Identifier.Xmin', 'Identifier.Ymin', 'Identifier.Xmax', 'Identifier.Ymax', \
    #                                 'Identifier.CentroidX', 'Identifier.CentroidY', \
    #                                 'Identifier.WeightedCentroidX', 'Identifier.WeightedCentroidY'])

    # save to disk
    features.to_csv(out_file_path, index=False)
