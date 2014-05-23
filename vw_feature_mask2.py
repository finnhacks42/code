# this creats a feature mask file that can be used with the --feature_mask flag 
import vw
import sys

infile = sys.argv[1]
masked = infile+"masked"
maskfile = "mask"

features = sys.argv[2:]
features = [int(x) for x in features]

# create a file with only that subset
ns_features = vw.featureMask(features,infile,masked)


# create a file that masks everything except the specified subset

vw.create_mask_file(ns_features,maskfile)
