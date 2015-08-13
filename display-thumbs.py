from pylab import *
from astropy.io import fits
import aplpy
import glob

#files = glob.glob('/Users/Tom/HIPE/plots/obs_thumbs/above_lowsnr/*PLW.fits')[:16]
files = glob.glob('/Users/Tom/HIPE/plots/obs_thumbs/below_highsnr/*PLW.fits')[:16]

for f in files:
    print(f)

fmain = figure(figsize=(12,8))
for i, f in enumerate(files):
    print(i, f)
    fig = aplpy.FITSFigure(f, figure=fmain, subplot=(4,4,i+1))
    fig.show_colorscale(cmap='gist_heat')
    fig.axis_labels.hide()
    fig.tick_labels.hide()
    fig.add_colorbar()
    #fig.colorbar.show()


tight_layout()
subplots_adjust(hspace=0.2, wspace=0)

#savefig('doc/above_lowsnr.pdf')
savefig('doc/below_highsnr.pdf')
show()
