#!/usr/bin/python3
import argparse
import pandas as pd
import matplotlib.pyplot as plt
def plotCAMI(filename, taxlevel, imgfile):
    f = open(filename)
    data = f.readlines()
    sdata = [x.strip().split("\t")for x in data[6:]]
    df = pd.DataFrame([[x[3], float(x[4])] for x in sdata if x[1]==taxlevel])
    df.columns = ['tax', 'perc']
    df = df[df['perc']>=1]
    total = sum(df.perc)
    df = df.sort_values(by=['tax'])
    df = df.append({'tax':'Others less than 1\%', 'perc':100-total}, ignore_index=True)
    labels = df.tax
    values = df.perc
    exps = [0.2 if (x < 2) else 0 for x in values]
    plt.figure(figsize=(20,20))
    plt.axis('equal')
    plt.pie(values, labels=labels, startangle=-90, autopct='%1.1f%%', explode=exps)
    plt.savefig(imgfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PLOT CAMI\n')
    parser.add_argument('-i', dest='input', type=str,
                        help='CAMI file', required=True)
    parser.add_argument('-l', dest='level', type=str, help='taxonomy_level',
                        default="phylum")
    parser.add_argument('-o', dest='imgfile', type=str, help='Image file name', default="plot.pdf")
    args = parser.parse_args()
    filename = args.input
    taxlevel = args.level
    imgfile = args.imgfile
    plotCAMI(filename=filename, taxlevel=taxlevel, imgfile=imgfile)