import csv

def write_csv(filename,new_line):
    with open(filename, "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))