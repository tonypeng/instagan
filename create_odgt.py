import glob
import os
import json
from PIL import Image

root_dir = '/Users/michaelgump/Downloads/ADEChallengeData2016/'
image_dir = 'images'
annotation_dir = 'annotations'
splits = ['training', 'validation']

def get_odgt_json(img_file, seg_file):
    width, height = Image.open(img_file).size
    return json.dumps({
            'height': height,
            'width': width,
            'fpath_img': os.path.relpath(img_file, root_dir),
            'fpath_seg': os.path.relpath(seg_file, root_dir),
        })


for split in splits:
    odgt_file = open(os.path.join(root_dir, '{}.odgt'.format(split)), 'w')
    for seg_file in glob.glob(os.path.join(root_dir, annotation_dir, split, '*.png')):
        img_file = seg_file.replace('png', 'jpg').replace(annotation_dir, image_dir)
        line = get_odgt_json(img_file, seg_file)
        odgt_file.write(line + '\n')
