import sys
import vw

filename = sys.argv[1]
outfile = sys.argv[2]
vw.sigmoid_file(filename,outfile)
