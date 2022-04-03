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

# absMagU=[]
# absMagG=[]
# absMagR=[]
# absMagI=[]
# absMagZ=[]
Z=[]
specObjID_index=[]
for i in range(10):
	filename='./cut_data/%d.fits' % i
	hdu=fits.open(filename, mmap=True)
	bossSpecObjID=hdu[1].data['bossSpecObjID']
	# absMagU=np.append(absMagU,hdu[1].data['absMagU'][np.where((bossSpecObjID!=0))])
	# absMagG=np.append(absMagG,hdu[1].data['absMagG'][np.where((bossSpecObjID!=0))])
	# absMagR=np.append(absMagR,hdu[1].data['absMagR'][np.where((bossSpecObjID!=0))])
	# absMagI=np.append(absMagI,hdu[1].data['absMagI'][np.where((bossSpecObjID!=0))])
	# absMagZ=np.append(absMagZ,hdu[1].data['absMagZ'][np.where((bossSpecObjID!=0))])
	Z=np.append(Z,hdu[1].data['z'][np.where((bossSpecObjID!=0))])
	specObjID_index=np.append(specObjID_index,hdu[1].data['specobjid'][np.where((bossSpecObjID!=0))])

# Find the data in range Z<0.99798
z_crit=0.99798
specObjID_index=specObjID_index[np.where((Z<z_crit))]

'''
Find the crossed stellar mass fraction.
Origin fits file url:
	https://data.sdss.org/sas/dr12/boss/spectro/redux/galaxy/v1_1/wisconsin_pca_bc03-DR12-boss.fits.gz
Official documentational table url（参考文献链接也在下面）:
	http://skyserver.sdss.org/dr12/en/help/browser/browser.aspx?cmd=description+stellarMassPCAWiscBC03+U#&&history=description+stellarMassPCAWiscBC03+U
Data:
	- MSTELLAR_MEDIAN.  in unit of dex (solar masses)
	- SPECOBJID
'''
filename = './fits/wisconsin_pca_bc03-DR12-boss.fits'
hdu = fits.open(filename,mmap=True)
specObjID_Mass=hdu[1].data['SPECOBJID']
stellar_Mass=hdu[1].data['MSTELLAR_MEDIAN']
RA_Mass=hdu[1].data['RA']
DEC_Mass=hdu[1].data['DEC']
Z_Mass=hdu[1].data['Z']

# Fine the Common specObjID:
specObjID_common=np.intersect1d(specObjID_index,specObjID_Mass)

# Get the Common Stellar Mass array: 
extracted_stellar_Mass=np.zeros(len(specObjID_common))
extracted_Z_Mass=np.zeros(len(specObjID_common))
extracted_RA_Mass=np.zeros(len(specObjID_common))
extracted_DEC_Mass=np.zeros(len(specObjID_common))

## Multi_part start:
extracted_stellar_Mass_shared=multiprocessing.RawArray('d',extracted_stellar_Mass)
extracted_Z_Mass_shared=multiprocessing.RawArray('d',extracted_Z_Mass)
extracted_RA_Mass_shared=multiprocessing.RawArray('d',extracted_RA_Mass)
extracted_DEC_Mass_shared=multiprocessing.RawArray('d',extracted_DEC_Mass)

def find_data(i):
    find_index=np.where(specObjID_Mass==specObjID_common[i])
    extracted_stellar_Mass_shared[i]=stellar_Mass[find_index]
    extracted_Z_Mass_shared[i]=Z_Mass[find_index]
    extracted_RA_Mass_shared[i]=RA_Mass[find_index]
    extracted_DEC_Mass_shared[i]=DEC_Mass[find_index]
    return
    #print(float(i)/float(len(specObjID_common))*100,"%")

n_core=10
# n_core=1
p = multiprocessing.Pool(processes=n_core)
mpi_array=np.arange(0,len(specObjID_common),1)
res = p.map(find_data,mpi_array)
p.close()
p.join()
print('Multiprocessing finished!')
extracted_stellar_Mass=np.frombuffer(extracted_stellar_Mass_shared,dtype=np.double)
extracted_Z_Mass=np.frombuffer(extracted_Z_Mass_shared,dtype=np.double)
extracted_RA_Mass=np.frombuffer(extracted_RA_Mass_shared,dtype=np.double)
extracted_DEC_Mass=np.frombuffer(extracted_DEC_Mass_shared,dtype=np.double)
## Multi_part end.

# Export the data.
mass_filename = './mass_data/stellar_Mass_bc03.txt'
Z_filename = './mass_data/Z_Mass_bc03.txt'
RA_filename = './mass_data/RA_Mass_bc03.txt'
DEC_filename = './mass_data/DEC_Mass_bc03.txt'
np.savetxt(mass_filename,extracted_stellar_Mass)
np.savetxt(Z_filename,extracted_Z_Mass)
np.savetxt(RA_filename,extracted_RA_Mass)
np.savetxt(DEC_filename,extracted_DEC_Mass)
