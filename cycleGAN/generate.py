import cv2
import argparse
import numpy as np

from pathlib import Path
from PIL import ImageFont, ImageDraw, Image

from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

def has_glyph(font, glyph):
    for table in font['cmap'].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False

def valid_char(font, dic_path):
    f =  open(dic_path, 'r')
    char_list = [l.strip() for l in f if has_glyph(font, l.strip())]
    return char_list

def generate(font_prefix, bg_folder, dataset_name, dic_path, suffix='', align='center', position=(0, 0)):

    colors = [(190, 84, 38), (0, 0, 0)]
    n_colors = len(colors)

    bg_paths = [f for f in Path(bg_folder).iterdir()]
    n_bg = len(bg_paths)

    if font_prefix in ('JasonHandwriting', 'TW-Kai'):
        fn = -1
        font_folder = Path(font_prefix)
    else:
        fn = 0
        font_folder = Path(font_prefix) / 'ttc'

    font_paths = [f for f in font_folder.iterdir()]
    n_fonts = len(font_paths)

    for i in range(n_fonts - 1, -1, -1):
        if len(font_paths[i].name.split('.')) < 2 or font_paths[i].name.split(
                '.')[1] not in ('ttf', 'ttc'):
            font_paths.pop(i)

    output_dir = Path(dataset_name)
    output_dir.mkdir(exist_ok=True)

    valid_char_list = [valid_char(TTFont(path, fontNumber=fn), dic_path) for path in font_paths]
    char_dic = [l.strip() for l in open(dic_path, 'r')]

    for char in char_dic:
        char_folder = output_dir / char
        char_folder.mkdir(exist_ok=True)
        for i, font_path in enumerate(font_paths):
            # check char exist
            if char in valid_char_list[i]:
                bg_img = cv2.imread(str(bg_paths[np.random.randint(0, n_bg)]))
                w, h, _ = bg_img.shape
                font = ImageFont.truetype(str(font_path), 50, encoding='unic')
                img_pil = Image.fromarray(bg_img)

                # drawing
                draw = ImageDraw.Draw(img_pil)
                w_t, h_t = draw.textsize(char, font=font)
                if align == 'center':
                    pos = ((w - w_t) / 2, (h - h_t) / 2)
                else:
                    pos = position

                draw.text(pos, char, font=font, fill=colors[np.random.randint(0, n_colors)])

                # save
                img = np.array(img_pil)
                font_name = font_path.name.split('.')[0]
                outfile = f'{char}_{font_prefix}_{font_name}{suffix}.jpg'
                out_path = char_folder / outfile
                cv2.imwrite(str(out_path), img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dic", required=True, help="text file containing characters to generate.One character per line")
    parser.add_argument("--background", required=True, help="path of the directory containing backgrounds for generated images.")
    args = vars(parser.parse_args())

    dic = args['dic']
    suffix = '_' + dic.split('.')[0]

    # generate
    for font in ('JasonHandwriting', 'genyo-font', 'genwan-font',
                 'genseki-font', 'gensen-font', 'TW-Kai'):
        print("Font: ", font)
        generate(font, args['background'], font + suffix, dic)
