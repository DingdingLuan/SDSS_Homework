import numpy as np
from astropy.io import fits
from tqdm import tqdm


fitsename='./galaxy_DR12v5_LOWZ_South.fits'
hdu=fits.open(fitsename, mmap=True)
# print(repr(hdu[1].header))

data_plate=hdu[1].data['PLATE']
data_mjd=hdu[1].data['MJD']
data_fiber=hdu[1].data['FIBERID']

data_raw=np.concatenate([[np.array(data_plate), np.array(data_mjd), np.array(data_fiber)]], axis=1)
Header=' plate  mjd fiber'
data_output=np.transpose(data_raw)

cut=10
bin=np.size(data_output,0)//cut
for i in np.arange(cut):
	if i!=cut-1:
		np.savetxt('./cut_data/lowZ_South_'+str(i)+".txt", data_output[i*bin:(i+1)*bin,:], fmt="%s",header=Header,delimiter=' ')
	else:
		np.savetxt('./cut_data/lowZ_South_'+str(i)+".txt", data_output[i*bin:np.size(data_output,0),:], fmt="%s",header=Header,delimiter=' ')