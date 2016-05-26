#!/usr/bin/env python

import csv
from lib.convert import util as converterUtils
from lib.util import io as ioUtilities

def process(infile, extension, hyb2tcga, outdir, annotationInfo):
    if len(hyb2tcga) != 1:
        raise Exception("multiple samples found for one tsv file")
    
    tcga_id = hyb2tcga.itervalues().next()
    hdr1, hdr2 = generate_headers(infile, tcga_id, annotationInfo)
    
    filepath = converterUtils.constructPath(outdir, tcga_id, extension)
    
    rawfile = open(infile, 'rb')
    csvfile = csv.reader(rawfile, dialect='excel-tab')
    
    csvfile_with_hdr = converterUtils.change_header__generator(csvfile, hdr1, hdr2)
    csvfile_with_NAs = converterUtils.map_blank_to_na(csvfile_with_hdr)
    
    ioUtilities.safeMakeDirs(outdir)
    converterUtils.writeCsvFile(filepath, csvfile_with_NAs)
    
    rawfile.close()

def generate_headers(infile, tcga_id, annotationInfo):
    old_hdr = ioUtilities.getTabFileHeader(infile)
    
    num_header_columns =  annotationInfo.getNumHeaderCols()
    num_info_cols = num_header_columns - 1
    num_data_cols = len(old_hdr) - num_header_columns
    
    new_hdr = ['Hybridization REF'] + [''] * num_info_cols + [tcga_id] * num_data_cols
    
    return new_hdr, old_hdr