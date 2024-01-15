import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--background')
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output', default='output.pdf')
    parser.add_argument('-l', '--language', default='ch', choices=['ch', 'en'])
    args = parser.parse_args()

    args.output_name = args.output.replace('.pdf', '')
    return args
