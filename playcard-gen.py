#!/usr/bin/env python
from subprocess import call
from tempfile import mktemp
import os
from utils import get_parser


def get_text(input_file):
    ## read in .txt or .csv file
    with open(input_file) as f:
        names = f.readlines()

    ## process the text to remove ordered lists
    is_long_text = False
    line_max = 12
    new_names = []
    for name in names:
        if '.' in name:
            name = name.split('.')[1].strip()
        if len(name) > 6:
            is_long_text = True
            line = ''
            for i, c in enumerate(name):
                line += c
                if i % line_max == line_max - 1:
                    line += '\\newline '
            name = line
        new_names.append(name)
    names = new_names
    return names, is_long_text


def generate_playcard(args):

    num_cols = args.num_cols
    num_rows = args.num_rows
    output_name = args.output_name
    names, is_long_text = get_text(args.input)

    margin_top = 0.5 * 254
    margin_left = 0.75 * 254
    margin_bottom = 0.5 * 254
    margin_right = 0.75 * 254

    page_width = int(8.5 * 254 + 0.5)
    page_height = int(11 * 254 + 0.5)

    label_width = 3.5 * 272
    label_height = 2 * 272
    label_bleed = 0  # -.1*272

    if args.language == 'en':
        text_top = int(0.325 * label_height)
        label_left_ratio = 0.03
    else:
        if is_long_text:
            text_top = int(0.3 * label_height)
            label_left_ratio = 0
        else:
            text_top = int(0.27 * label_height)
            label_left_ratio = 0.06

    latex = ""
    if args.language == 'en':
        latex += "\\documentclass[12pt]{article}"
        latex += "\\usepackage{fontspec}"
        latex += "\\setmainfont[Ligatures=TeX,Scale=3]{chunkfive.otf}"
        latex += "\\setstretch{2.0}"
    else:
        if is_long_text:
            latex += "\\documentclass[12pt]{extarticle}"
        else:
            latex += "\\documentclass[17pt]{extarticle}"
        latex += "\\usepackage{xeCJK}"
        latex += "\\usepackage[T1]{fontenc}"
    latex += "\\pagestyle{empty}"
    latex += "\\usepackage{xunicode}"
    latex += "\\usepackage{setspace}"
    latex += "\\usepackage{graphics}"
    latex += "\\usepackage{graphicx}"
    latex += "\\usepackage{color}"
    latex += "\\usepackage[left=0cm,top=0cm,right=0cm,bottom=0cm,nohead,nofoot]{geometry}"
    latex += "\\usepackage[absolute]{textpos}"
    latex += "\\setlength\\parindent{0cm}"
    latex += "\\setlength\\parskip{0cm}"
    latex += "\\TPGrid[0.1mm,0.1mm]{%d}{%d}" % (page_width, page_height)
    latex += "\\begin{document}"

    for i in range(0, len(names)):

        i_mod = i % (num_rows * num_cols)
        if i_mod == 0:
            latex += "\\newpage\\tiny ."

        label_left = float(0.5 + margin_left +
                           (page_width - margin_left - margin_right) / num_cols * (i_mod % 2) - label_bleed)
        label_top = float(0.5 + margin_top +
                          ((page_height - margin_top - margin_bottom) / num_rows) * int(i_mod / 2) - label_bleed)

        latex += "\\begin{textblock}{%d}(%d,%d)" % (label_width, label_left, label_top)
        if args.background is not None:
            latex += "\\includegraphics[width=3.5in]{%s}" % args.background
        latex += "\\end{textblock}"

        label_left -= label_width * label_left_ratio

        ## some names are too long
        pos_top = label_top + text_top
        if '\\' in names[i]:
            pos_top -= text_top * 0.17
        if args.num_rows >= 5:
            pos_top -= text_top * 0.3

        latex += "\\begin{textblock}{%d}(%d,%d)" % (label_width, label_left, pos_top)
        latex += "\\begin{center}\\textcolor[rgb]{0,0,0}{\\textbf{"
        if args.language == 'ch':
            if len(names[i]) <= 6:
                latex += "\\Huge"
            else:
                latex += "\\large"
        latex += "{ %d. %s }\\\\" % (i+1, names[i])
        # latex += "{ %s }\\\\" % names[i]
        latex += "}}"
        latex += "\\end{center}"
        latex += "\\end{textblock}"

    latex += "\\end{document}"

    filename_latex = mktemp('tex')

    file_latex = open(filename_latex, "w")
    file_latex.write(latex)
    file_latex.close()

    call(["xelatex", "-jobname", output_name, "-output-directory", ".", filename_latex])
    os.remove(output_name + '.log')
    os.remove(output_name + '.aux')


if __name__ == '__main__':
    args = get_parser()
    generate_playcard(args)
