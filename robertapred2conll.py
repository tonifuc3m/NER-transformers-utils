#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 10:43:52 2021

@author: antonio
"""
import argparse
import codecs

def argparser():
    parser = argparse.ArgumentParser(description='process user given parameters')
    parser.add_argument("-p", "--predictions", required = True, dest = "predictions_path", 
                        help = "Path to predictions file")
    parser.add_argument("-i", "--input", required=True, dest="input_path",
                        help = "Path to input file")
    parser.add_argument("-o", "-outpout", required=True, dest="out_path",
                        help="Path to output file")
    args = parser.parse_args()
    return args.predictions_path, args.input_path, args.out_path

def robertaformat_to_conll(roberta_predictions_path, roberta_input_path, out_path):
    roberta_file = codecs.open(roberta_predictions_path, 'r', 'UTF-8')
    input_file = codecs.open(roberta_input_path, 'r', 'UTF-8')

    fout = open(out_path,'w')
    for line_roberta, line_input in zip(roberta_file, input_file):
        if line_roberta == line_input == '\n':
            fout.write('\n')
            continue
        
        token_roberta = line_roberta.split(' ')[0]
        token_input = line_input.split('\t')[0]
        if token_roberta == token_input:
            filename = line_input.split('\t')[1]
            pos0 = line_input.split('\t')[2].split('_')[0]
            pos1 = line_input.split('\t')[2].split('_')[1]
            tag = line_roberta.split(' ')[1]
            fout.write(f"{token_input} {filename} {pos0} {pos1} {tag}")
            continue
        
        # Assume all mismatches are because the roberta predictions are cropped
        # when too long lines
        filename = line_input.split('\t')[1]
        pos0 = line_input.split('\t')[2].split('_')[0]
        pos1 = line_input.split('\t')[2].split('_')[1]
        tag = line_input.split('\t')[-1]
        fout.write(f"{token_input} {filename} {pos0} {pos1} {tag}")
        for line_input in input_file:
            if line_roberta == line_input == '\n':
                fout.write('\n')
                break
            token_input = line_input.split('\t')[0]
            if token_roberta == token_input:
                filename = line_input.split('\t')[1]
                pos0 = line_input.split('\t')[2].split('_')[0]
                pos1 = line_input.split('\t')[2].split('_')[1]
                tag = line_roberta.split(' ')[1]
                fout.write(f"{token_input} {filename} {pos0} {pos1} {tag}")
                break
            filename = line_input.split('\t')[1]
            pos0 = line_input.split('\t')[2].split('_')[0]
            pos1 = line_input.split('\t')[2].split('_')[1]
            #tag = line_input.split('\t')[-1]
            tag='O'
            fout.write(f"{token_input} {filename} {pos0} {pos1} {tag}")    
    fout.close()
if __name__ == '__main__':
    roberta_predictions_path, roberta_input_path, out_path = argparser()
    robertaformat_to_conll(roberta_predictions_path, roberta_input_path, out_path)