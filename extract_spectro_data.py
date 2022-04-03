import numpy as np
from astropy.io import fits
from tqdm import tqdm
import multiprocessing


''' 
Read the data from seperated CROSS-ID fits files.
CROSS-ID url: 
	http://skyserver.sdss.org/dr12/en/tools/crossid/crossid.aspx
Data:
	- modelMag_u
	- modelMag_g
	- modelMag_r
	- modelMag_i
	- modelMag_z
	- specObjID
'''

absMagU=[]
absMagG=[]
absMagR=[]
absMagI=[]
absMagZ=[]
# specObjID_index=[]
Z=[]
RA=[]
DEC=[]
for i in range(10):
	filename='./cut_data/%d.fits' % i
	hdu=fits.open(filename, mmap=True)
	bossSpecObjID=hdu[1].data['bossSpecObjID']
	absMagU=np.append(absMagU,hdu[1].data['absMagU'][np.where((bossSpecObjID!=0))])
	absMagG=np.append(absMagG,hdu[1].data['absMagG'][np.where((bossSpecObjID!=0))])
	absMagR=np.append(absMagR,hdu[1].data['absMagR'][np.where((bossSpecObjID!=0))])
	absMagI=np.append(absMagI,hdu[1].data['absMagI'][np.where((bossSpecObjID!=0))])
	absMagZ=np.append(absMagZ,hdu[1].data['absMagZ'][np.where((bossSpecObjID!=0))])
	Z=np.append(Z,hdu[1].data['z'][np.where((bossSpecObjID!=0))])
	RA=np.append(RA,hdu[1].data['ra'][np.where((bossSpecObjID!=0))])
	DEC=np.append(DEC,hdu[1].data['dec'][np.where((bossSpecObjID!=0))])
	# specObjID_index=np.append(specObjID_index,hdu[1].data['specobjid'][np.where((bossSpecObjID!=0))])
# Find the data in range Z<0.99798
z_crit=0.99798
absMagU=absMagU[np.where((Z<z_crit))]
absMagG=absMagG[np.where((Z<z_crit))]
absMagR=absMagR[np.where((Z<z_crit))]
absMagI=absMagI[np.where((Z<z_crit))]
absMagZ=absMagZ[np.where((Z<z_crit))]
RA=RA[np.where((Z<z_crit))]
DEC=DEC[np.where((Z<z_crit))]
Z=Z[np.where((Z<z_crit))]

'''
Mag transform url:
	http://www.sdss3.org/dr8/algorithms/sdssUBVRITransform.php
'''

# Export the data.
Z_filename = './spectro_data/Z_Cross_ID.txt'
RA_filename = './spectro_data/RA_Cross_ID.txt'
DEC_filename = './spectro_data/DEC_Cross_ID.txt'
absMagU_filename = './spectro_data/absMagU_Cross_ID.txt'
absMagG_filename = './spectro_data/absMagG_Cross_ID.txt'
absMagR_filename = './spectro_data/absMagR_Cross_ID.txt'
absMagI_filename = './spectro_data/absMagI_Cross_ID.txt'
absMagZ_filename = './spectro_data/absMagZ_Cross_ID.txt'

np.savetxt(Z_filename,Z)
np.savetxt(RA_filename,RA)
np.savetxt(DEC_filename,DEC)
np.savetxt(absMagU_filename,absMagU)
np.savetxt(absMagG_filename,absMagG)
np.savetxt(absMagR_filename,absMagR)
np.savetxt(absMagI_filename,absMagI)
np.savetxt(absMagZ_filename,absMagZ)
