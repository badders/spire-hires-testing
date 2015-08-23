# spire-hires-testing

/doc/ contains output figures and the presentation document given in the telecon.

/stats/ contains the data analysis of the entire set of observations in the archive
    -   {band}.csv contains the full set of statistics calculated
    -   Results.csv is set of information used as the threshold tests including pass/fail

/obs-lists/ contains dataset output from some scripts, and data classifying the various observations by proposal type

/obs-to-hires/ contain lists of the observation ids that pass the final agreed tests

Some scripts are designed to be run in hipe, denoted as (HIPS), others are pure python and use the standard scipy stack with astropy and aplpy where appropriate.

 beam-size-profiles-SPIRE.py - Take a set of fits of files, named by hires beam size and create an interactive plot of a cut through the image - uses files output by beam-size-SPIRE.py and regird.py

 beam-size-SPIRE.py (HIPE) - Perform a hires mapping using beams cropped to various sizes, and output these to fits files

 regrid.py (HIPE) - Regrid nominal maps from beam-size-SPIRE.py to match the pixel grid of the HiRes maps

 beam-size-profiles.py - Similar to beam-size-profiles-spire.py but using
