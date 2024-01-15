#!/usr/bin/env python
from subprocess import call
from tempfile import mktemp
import os
from utils import get_parser


filter_by_professors = [
    'agrawal', 'hadfield-menell', 'isola', 'jda', 'lpk', 'tlp', 'nickroy', 'sitzmann', 'torralba', 'yoonkim'
]


def get_text(input_file, max_length=24):
    """ read .csv file downloaded from
    https://docs.google.com/spreadsheets/d/1fAzchmLE3CbeVa36rqg7YMPf5J4GdDNHQFr0iFAr7RQ/edit#gid=0
    """
    with open(input_file) as f:
        lines = f.readlines()

    names = []
    for line in lines:
        fields = line.split(',')
        if fields[3] in filter_by_professors:
            name = fields[0] + ' ' + fields[1]
            spacing = '\\,' * int((max_length - len(name)))
            name = spacing + name + spacing
            names.append(name)
    print('\n\n\nfound {} names\n\n\n'.format(len(names)))
    return names


def generate_nameplate(args):
    output_name = args.output_name
    names = get_text(args.input)

    latex = "\\documentclass[20pt]{extarticle}"
    latex += "\\usepackage{moresize}"
    latex += "\\usepackage{overpic}"
    latex += "\\usepackage[absolute]{textpos}"
    latex += "\\usepackage{graphicx}"
    latex += "\\usepackage{rotating}"
    latex += "\\usepackage{nopageno}"
    latex += "\\usepackage[top=0mm,bottom=0mm,left=0mm,right=0mm]{geometry}"
    latex += "\\begin{document}"
    latex += "\\bfseries\Huge"

    for name in names:
        latex += "\\begin{center}"
        latex += "\\hspace*{-0pt}"
        latex += "\\begin{overpic}[width=0.86\columnwidth]{" + args.background + "}"
        latex += "\\begin{turn}{-90}"
        latex += "\\put(-80,7){" + name + "}"
        latex += "\\end{turn}"
        latex += "\\begin{turn}{90}"
        latex += "\\put(20,-47){" + name + "}"
        latex += "\\end{turn}"
        latex += "\\end{overpic}"
        latex += "\\end{center}"

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
    generate_nameplate(args)
