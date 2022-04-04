# SDSS_Homework for Evo of Galaxy formation. (2022.4)

This repository is used to reduce the data from SDSS/dr12.
- format_inquired_data.py was used to tansform the raw SDSS fits to fisible SQL format.
- extract_mass_daya.py was used to find the stellar mass according to the specobjID and redshift.
- extract_spectro_data was used to find the spectrum parameters according to the BossobjID and redshift.
- print_header.py was used to get the fits header for convenient.

All the fits files are coming from: https://www.sdss.org/dr12/
