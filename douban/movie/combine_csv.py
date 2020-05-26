#! -*- coding: utf-8 -*-
#/usr/bin/env python
import os
import sys
import pandas as pd
'''
合并每个类的interval csv文件到一个文件里
example:
合并前：
  1-10_0.csv
  1-20_10.csv
  1-30_20.csv
  ...
  1-100_90.csv
合并后：
  1-纪录片.csv

'''
def main():
    typefile = "douban_movie_types.txt"
    csvdir = "data"
    movietypes = pd.read_csv(typefile, sep='\s+', names=['name', 'id']).values
    interval_ids = [
        (100,90),(90,80),(80,70),(70,60),(60, 50),
        (50,40),(40,30),(30,20),(20,10),(10,0)
    ]
    for typename, typeid in movietypes:
        csvdf = None
        for interval_id in interval_ids:
            fname = os.path.join(csvdir, "%d-%d_%d.csv"%(typeid, *interval_id))
            if os.path.exists(fname)==0:
                print(fname, "not exists!")
                continue
            df = pd.read_csv(fname)
            if csvdf is None:
                csvdf = df
            else:
                csvdf = pd.concat([csvdf, df])
        outf = '%d-%s.csv'%(typeid, typename)
        csvdf.to_csv(outf, index=False)

if __name__ == "__main__":
    main()