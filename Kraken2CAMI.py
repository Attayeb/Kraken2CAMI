import argparse







def printset(li, level):
    subset = [x for x in li if x[1] == level]
    subset.sort(key=lambda x: float(x[4]), reverse=True)
    total = sum([float(x[4]) for x in subset])
    for x in subset:
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
    for x in report:
        x = x.split("\t")
        g = x[3]
        if g != "-":
            #print(x.strip())
            dic.append({'percent': x[0],
                 'number1': x[1],
                 'number2': x[2],
                 'tax': x[3],
                 'taxid':x[4],
                 'taxonomy':x[5].strip()})


    result = list()
    taxidlist=list()
    taxlist=list()
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
                       "|".join([str(x) for x in taxidlist]),
                       "|".join(taxlist),
                       str(x['percent'])])

    f.close()
    return (result)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert Kraken to CAMI')
    parser.add_argument('-i', dest='input', type=str,
                        help='Kraken-report file name', required=True)
    parser.add_argument('-o', dest='output', type=str,
                         help='CAMI file')

    parser.add_argument('-l', dest='level', type=str, help='taxonomy_level comma separated', default="species,genus,phylum")
    parser.add_argument('--sampleid', dest='sampleid', type=str, help='Sample ID', default='')
    parser.add_argument('--ncbitaxid', dest='taxonomyid', type=str, help='NCBI Taxonomy date', default='')
    args = parser.parse_args()
    filename = args.input
    sampleid=args.sampleid
    taxonomyid=args.taxonomyid
    level = args.level
    result = main(filename=filename)
    levels = level.split(",")
    print('''# Taxonomic Profiling Output
@SampleID:%s
@Version:0.9.1
@Ranks:superkingdom|phylum|class|order|family|genus|species
@TaxonomyID:%s
@@TAXID	RANK	TAXPATH	TAXPATHSN	PERCENTAGE'''%(sampleid, taxonomyid))
    for x in levels:
        printset(result, x)


