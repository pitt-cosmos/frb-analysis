import moby2
import math

ardata = moby2.scripting.get_array_data({'season':'2016', 'array_name':'AR3'})
n_tes=0
n_noc=0
n_dark=0
for t in ardata['det_type']:
    if t == 'tes':
        n_tes += 1
    elif t == 'dark_squid':
        n_dark += 1
    else:
        n_noc += 1
print "number of tes: %d" % n_tes
print "number of dark_squid: %d" % n_dark
print "number of no_conn: %d" % n_noc

pixel_indexes = [index for index in range(1056) if math.floor(index / 32)%4 ==0 and math.floor(index/32)<32]

dts = ardata['det_type']
n_full = 0
for p in pixel_indexes:
    if dts[p] == 'tes' and dts[p+32] == 'tes' and dts[p+64]=='tes' and dts[p+96]=='tes':
        n_full += 1
print "number of total pixels: %d" % len(pixel_indexes)
print "number of full range pixels: %d" % n_full
