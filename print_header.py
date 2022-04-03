import numpy as np
from astropy.io import fits
from tqdm import tqdm


# filename='./cut_data/0.fits'
# filename = '../data/wisconsin_pca_bc03-DR12-boss.fits'
filename='../galaxy_DR12v5_LOWZ_South.fits'
hdu=fits.open(filename, mmap=True)
# print(repr(hdu[1].header))
Z=hdu[1].data['Z']
print(np.max(Z))
print(len(Z))
# bossSpecObjID=hdu[1].data['bossSpecObjID']
# print(len(bossSpecObjID[np.where((bossSpecObjID!=0))]))