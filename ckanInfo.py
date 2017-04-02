#!/usr/bin/env python3

from ckan import *

ckan = CkanClient()
print ("\nNumber of published datasets:%d" % len(ckan.Datasets))
print ("Number of internal resources:%d" % ckan.NIntRsrc)
print ("Number of external resources:%d" % ckan.NExtRsrc)
