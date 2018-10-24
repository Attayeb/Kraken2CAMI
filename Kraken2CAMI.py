#!/usr/bin/python3
import argparse
def printset(li, level, ranks, precision):
    taxlevels = ['superkingdum', 'phylum', 'class', 'order', 'family','genus','species']
    inc = [i for i, j in enumerate(taxlevels) if j in ranks]
    subset = [x for x in li if x[1] == level]
    subset.sort(key=lambda x: float(x[4]), reverse=True)
    total = sum([float(x[4]) for x in subset])

    for x in subset:
        if len(x[2]) <= max(inc):
            #print(max(inc))
            #print(x[2])
            continue
        if x[4] == '0.'+'0'*precision:
            continue
        x[2] = "|".join([x[2][i] for i in inc])
        x[3] = "|".join([x[3][i] for i in inc])
        print("\t".join(x))
    return subset, total

def main(filename):
    f = open(filename)

    report = f.readlines()

    levels = ['D', 'P', 'C', 'O', 'F', 'G', 'S']
    levelsdic = {'D':'superkingdum',
                 'P':'phylum',
                 'C':'class',
                 'O':'order',
                 'F':'family',
                 'G':'genus',
                 'S':'species'}

    dic = list()
    total = 0.
    for x in report:
        x = x.split("\t")
        g = x[3]
        g2 = x[4]
        if g2=='0':
            total= total + int(x[1])
        if g2=='1':
            total= total + int(x[1])
        if g not in ["-", "U"]:
            #print(x.strip())
            dic.append(
                {
                 'percent': x[0],
                 'cpercent':float(x[1])/total*100,
                 'number1': x[1],
                 'number2': x[2],
                 'tax': x[3],
                 'taxid':x[4],
                 'taxonomy':x[5].strip()
                }
            )


    result = list()
    taxidlist=list()
    taxlist=list()
    formatstring='{:.%df}'%precision
    for x in dic:
        if x['tax']=='U':
            continue
        taxlevel = levels.index(x['tax'])
        taxidlist = taxidlist[:taxlevel]
        taxlist = taxlist[:taxlevel]
        if taxlevel == 0:
            taxidlist=[]
            taxidlist.append(int(x['taxid']))
            taxlist.append(x['taxonomy'])
        else:
            if taxlevel+1 > len(taxidlist):
                taxidlist.append(int(x['taxid']))
                taxlist.append(x['taxonomy'])
            else:
                taxidlist[taxlevel] = int(x['taxid'])
                taxlist[taxlevel] = x['taxonomy']
        result.append([x['taxid'],
                       levelsdic[x['tax']],
                       [str(x) for x in taxidlist],
                       taxlist,
                       formatstring.format(x['cpercent'])])

    f.close()
    return (result)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert Kraken to CAMI\n'
                                                 'If you want to save to a file you can pipe the result using ">"\n'
                                                 'example: Kraken2CAMI.py -i report.text > report.CAMI')
    parser.add_argument('-i', dest='input', type=str,
                        help='Kraken-report file name', required=True)
    parser.add_argument('-l', dest='level', type=str, help='taxonomy_level comma separated', default="species,genus,phylum")
    parser.add_argument('--sampleid', dest='sampleid', type=str, help='Sample ID', default='')
    parser.add_argument('--ncbitaxid', dest='taxonomyid', type=str, help='NCBI Taxonomy date', default='')
    parser.add_argument('--ranks', dest='ranks', type=str, help='Ranks comma separated', default="superkingdom,phylum,class,order,family,genus,species")
    parser.add_argument('--precision', dest='precision', type=int, help='precision of precentage', default=5)
    args = parser.parse_args()
    filename = args.input
    sampleid=args.sampleid
    taxonomyid=args.taxonomyid
    level = args.level
    precision = args.precision
    ranks = args.ranks.split(",")
    result = main(filename=filename)
    levels = level.split(",")
    print('''# Taxonomic Profiling Output
@SampleID:%s
@Version:0.9.1
@Ranks:%s
@TaxonomyID:%s
@@TAXID	RANK	TAXPATH	TAXPATHSN	PERCENTAGE'''%(sampleid, "|".join(ranks), taxonomyid))
    for x in levels:
        #print(x)
        #print(result)
        printset(result, level=x, ranks=ranks[:ranks.index(x)+1], precision=precision)


