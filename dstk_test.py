# this script geo locates a single address using DSTK and prints the result to screen for debugging.
import sys
import dstk
dstk = dstk.DSTK({'apiBase':'http://localhost:8080'})

address = "7401 SAMUELL BLVD, DALLAS, TX 75227"
geo = dstk.street2coordinates(address)[address]
if geo:
    for i in geo.items():
        print i
else:
    print 'not found'


