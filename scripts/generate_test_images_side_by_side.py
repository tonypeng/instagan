import os
from glob import glob
from PIL import Image

RESULTS_DIR = "pix2pix/results"

subdirs = [dir for dir in glob(RESULTS_DIR + "/*/")]

for file in glob(subdirs[0] + "*_B.png"):
    file_basename = os.path.basename(file)
    image_filenames = []
    for subdir in subdirs:
        example_filename = subdir + file_basename
        image_filenames.append(example_filename)
    images = [Image.open(x) for x in image_filenames]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save('results_combined/' + file_basename)