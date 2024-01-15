# Printable Name Plate & Play Card PDF Generator

![](media/example.jpg)

## Usage 
```
python playcard-gen.py -i 2020.csv -b 2020.pdf
python nameplate-gen.py -i data/240113-EI/input.csv -b data/240113-EI/EI-background.png
```

*  `-i | --input` can be `.csv` or `.txt`
* `-b | --background` can be `.png`, `.jpg` or `.pdf`.

## Set up

Should be able to run without virtual env. Install `texlive` on MacOS by following [instructions](https://www.tug.org/texlive/) and on `Ubuntu` by running:

```
apt-get install texlive-xetex texlive-latex-recommended texlive-latex-extra
```