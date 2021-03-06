#!/usr/bin/env python

import numpy as np
import os
from halotools import sim_manager



catman = sim_manager.CatalogManager()

#############################################################################
####### CHECK THAT WE CAN LOCATE AVAILABLE AND CLOSEST HALO CATALOGS #######

"""
supported_halocats = catman.available_halocats
simname, halo_finder = supported_halocats[0]
catalog_type = 'raw_halos'
desired_redshift = 1


location = 'web'
closest_cat_on_web = catman.closest_halocat(location, catalog_type, simname, halo_finder, desired_redshift)
print("\n Closest matching catalog on the web = \n%s\n " % closest_cat_on_web[0])

location = 'cache'
closest_cat_in_cache = catman.closest_halocat(location, catalog_type, simname, halo_finder, desired_redshift)
print("\n Closest matching catalog in cache = \n%s\n " % closest_cat_in_cache[0])

location='/Volumes/NbodyDisk1/raw_halos/bolshoi/rockstar'
closest_cat_in_cache = catman.closest_halocat(location, catalog_type, simname, halo_finder, desired_redshift)
print("\n Closest matching catalog on external disk = \n%s\n " % closest_cat_in_cache[0])


"""
#############################################################################
# CHECK THE CONVENIENCE FUNCTION ALL_HALOCATS_IN_CACHE
print("\n")
all_cached_files = catman.all_halocats_in_cache('halos')
#for f in all_cached_files: print(f)


#############################################################################
####### CHECK THAT RAW HALO CATALOG DOWNLOADS GO TO CACHE #######
catalog_type = 'raw_halos'
desired_redshift = 12.083
simname = 'bolshoi'
halo_finder = 'rockstar'
disk_location = os.path.join(os.path.join('/Volumes/NbodyDisk1/raw_halos', simname), halo_finder)

catlist = catman.available_snapshots(disk_location, catalog_type, simname, halo_finder)
print("\n All catalogs on external disk:\n")
for f in catlist:
	print f

### Check the web
closest_cat_on_web = catman.closest_halocat('web', catalog_type, simname, halo_finder, desired_redshift)
print("\nFor simname = %s and redshift = %.2f, " % (simname, desired_redshift))
print("Closest halocat available for download: \n%s\n" % closest_cat_on_web[0])

### Check the cache
is_in_cache = catman.check_for_existing_halocat('cache', catalog_type, 
	simname, halo_finder, fname=closest_cat_on_web[0])
print("Is the file already in cache?\n %r \n" % is_in_cache)

### Check the external disk
is_on_disk = catman.check_for_existing_halocat(disk_location, catalog_type, 
	simname, halo_finder, 
	fname=closest_cat_on_web[0])

print("Is the file stored on disk?\n %r \n" % is_on_disk)
if is_on_disk == False:
	output_fname = catman.download_raw_halocat(simname, halo_finder, closest_cat_on_web[1], 
		overwrite = False, download_loc = disk_location)
	print("\n The following fname was just downloaded: \n%s\n" % output_fname)
	print("\n This fname should agree with: \n%s\n" % closest_cat_on_web[0])
	print("Can we detect this newly downloaded file on disk?\n")
	is_on_disk = catman.check_for_existing_halocat(
		disk_location, catalog_type, simname, halo_finder, 
		fname=closest_cat_on_web[0])
	print is_on_disk
	print ("\n")


if is_in_cache == False:
	print("\n... downloading file...\n")
	catman.download_raw_halocat(simname, halo_finder, closest_cat_on_web[1], overwrite = False)
	is_in_cache = catman.check_for_existing_halocat('cache', catalog_type, 
		simname, halo_finder, fname=closest_cat_on_web[0])
	print("Is the file now in cache? %r " % is_in_cache)

closest_cat_in_cache = catman.closest_halocat('cache', catalog_type, simname, halo_finder, desired_redshift)
if closest_cat_in_cache[0] != is_in_cache:
	print("closest_halocat method failed to detect the following catalog: \n%s\n" % is_in_cache)


#############################################################################
####### CHECK THAT WE CAN PROCESS AND STORE ANY RAW HALO CATALOG INTO AN ARRAY #######
print("\n\n Processing raw halo catalog found in cache\n\n")
halocat_fname = is_in_cache

def some_other_cut(x):
	return x['mpeak'] > 5.e5

arr, reader = catman.process_raw_halocat(halocat_fname, simname, halo_finder)

### Store the catalog
version_name = 'mpeak.gt.2e9'
notes = {'cuts_description': 'I passed no cuts_funcobj argument, so I just used whatever the defaults were. '}
output_full_fname = catman.store_processed_halocat(arr, reader, version_name, 
	notes = notes, overwrite=True)

import h5py
f = h5py.File(output_full_fname)
print f.attrs.keys()
ps = f.attrs['halocat_exact_cuts']
import pickle
cutting_function = pickle.loads(f.attrs['halocat_exact_cuts'])


f.close()


#############################################################################

dummylist = catman.available_snapshots('cache', 'halos', simname, halo_finder)
print("\n")
for f in dummylist:
	print os.path.basename(f)
print("\n")

halocat_obj = sim_manager.read_nbody.get_halocat_obj(simname, halo_finder)
print("Closest halocat = \n")
print(halocat_obj.closest_halocat(dummylist, 11.77, version_name='mpeak.gt.2e9'))
print("\n")




















#############################################################################
####### CHECK THE HALOCAT_OBJ PROPERTIES #######
#halocat_obj = sim_manager.read_nbody.get_halocat_obj(simname, halo_finder)
#original_loc = halocat_obj.original_data_source
#print("Original data source for %s %s = \n%s\n" % (simname, halo_finder, original_loc))



#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
print("\n\n\n\n")
