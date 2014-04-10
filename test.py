import dstk
dstk = dstk.DSTK()

address = "9929 HARRY HINES BLVD, TX 75235"
geo = dstk.street2coordinates(address)[address]
lat = geo.get('latitude')
lon = geo.get('longitude')
street = geo.get('street_name')
conf = geo.get('confidence')
number = geo.get('street_number')

print lat,lon,street,conf,number

