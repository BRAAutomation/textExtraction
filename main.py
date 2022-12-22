from PIL import Image
import pyocr
import pyocr.builders

import os
import numpy as np
import argparse
import glob

INPUT_DIR = "./input"
OUTPUT_DIR = "./output"
MARGIN_LEN = 50

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default = INPUT_DIR)
parser.add_argument('--output1', type=str, default = OUTPUT_DIR)
parser.add_argument('--output2', type=str, default = OUTPUT_DIR)
args = parser.parse_args()

def main(args):
    #take from all pdf files
    tools = pyocr.get_available_tools()
    tool = tools[0]
    for imgName, img_fl in enumerate( glob.glob(args.input+ "/*") ):
        #Opening Image
        im = Image.open(img_fl)
        H, W = im.size

        #OCR
        box_builder = pyocr.builders.LineBoxBuilder(tesseract_layout = 6)
        text_position = tool.image_to_string(im,lang = "eng",builder = box_builder)

        #FOR ANNOTATION
        with open(args.output1 + "/" + os.path.splitext(os.path.basename(img_fl))[0] + ".txt" , 'w') as f:
            for listdata in text_position:
                (x1,y1),(x2,y2) = listdata.position
                xmin = int(x1); xmax = int(x2); ymin = int(y1); ymax = int(y2)
                x_center = (xmin + xmax)/2 ; y_center = (ymin + ymax)/2
                width = xmax - xmin ; height = ymax - ymin
                #Standerlize
                x_center /= W ; width /= W
                y_center /= H ; height /= H
                content = '{} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(1, x_center, y_center, width, height)
                f.write( content )

        #FOR RECOGNITION
        with open(args.output2 + "/" + os.path.splitext(os.path.basename(img_fl))[0] + ".txt" , 'w') as f:
            for listdata in text_position:
                #print(listdata)
                f.write( str( listdata) + "\n")

if __name__ == '__main__':
    main(args)
