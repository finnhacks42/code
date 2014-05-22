import sys
import vw
filein = sys.argv[1]
fileout = sys.argv[2]
vw.featureMask([1845],filein,fileout)
