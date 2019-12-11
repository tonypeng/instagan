import os
import glob
import argparse 
from PIL import Image
import shutil
import numpy as np
from scipy.io import loadmat
from time import time

data_directory = '/Users/michaelgump/Downloads/ADEChallengeData2016'

def code_to_class_index(code):
    if code == 0:
        return 0 # none
    # water, sky, rock, ground, tree, plant life, mountain, waterfall, hill, other
    if code == 22 or code == 27 or code == 61 or code == 129: # water; sea; river; lake
        return 1
    
    if code == 3:  # sky
        return 2  # sky
    
    if code == 35: # rock, stone
        return 3 # rock
    
    if code == 14 or code == 47 or code == 95 or code == 30: # earth, ground; sand; land, ground, soil; field
        return 4 # ground
    
    if code == 5: # tree
        return 5 # tree
    
    if code == 10 or code == 18: # grass; plant, flora, plant life
        return 6 # plants
    
    if code == 17: # mountain, mount
        return 7 # mountain
    
    if code == 114: # waterfall, falls
        return 8 # waterfall
    
    if code == 69:
        return 9 # hill
    
    return 10 # other

vec_code_to_class_index = np.vectorize(code_to_class_index)

number_processed = 0
all_files = sorted(glob.glob(os.path.join(data_directory, 'raw_annotations/validation/*.png')))
start_time = time()
for seg_filename in all_files:
    out_filename = seg_filename.split('/')[-1]
    out_file = os.path.join(data_directory, 'annotations/validation/{}'.format(out_filename))
    out_file_2 = os.path.join(data_directory, 'unfiltered_annotations/validation/{}'.format(out_filename))

    im = Image.open(seg_filename)
    seg =  np.array(im.getdata()).reshape((im.size[1], im.size[0]))
    class_seg = vec_code_to_class_index(seg).astype(np.uint8)

    contains_list = np.unique(class_seg)
    if len(contains_list) > 2 or (len(contains_list) == 2 and (0 not in contains_list or 10 not in contains_list)):
        Image.fromarray(class_seg, 'L').save(out_file) 
    Image.fromarray(class_seg, 'L').save(out_file_2) 
    
    number_processed += 1
    if (number_processed % 100) == 0:
        print('Processed {}, {}'.format(number_processed, time() - start_time))

