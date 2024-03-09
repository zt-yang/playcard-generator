import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--background')
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output', default='output.pdf')
    parser.add_argument('-c', '--num_cols', type=int, default=2)
    parser.add_argument('-r', '--num_rows', type=int, default=5)
    parser.add_argument('-l', '--language', default='ch', choices=['ch', 'en'])
    args = parser.parse_args()

    args.output_name = args.output.replace('.pdf', '')
    return args
