from common import *
from astropy import wcs
from scipy.optimize import curve_fit
from scipy.ndimage.filters import convolve
from matplotlib.widgets import Slider, RadioButtons
import aplpy

# Settings
fits_dir = "/Users/Tom/HIPE/plots/SPIRE/"

# M74, NGC4151, M81
#obsid = 1342189427
#obsid = 1342188588
#obsid = 1342185538
obsid = 1342249237

band = 'PLW' #, 'PMW', 'PSW'

beam_sizes = {
    'PLW' : [20, 50, 80, 100, 150],
    'PMW' : [15, 35, 60, 80, 100],
    'PSW' : [10, 25, 40, 60, 80],
}

fig = figure()
plots = {}

styles = list(reversed(['-', '--', '-.', ':', '-.']))
render = plot

def update(_):
    for b in beam_sizes[band]:
        if b == 0:
            hdulist = fits.open(fits_dir + '{}_NOMINAL_REGRID_{}.fits'.format(obsid, band))
        else:
            hdulist = fits.open(fits_dir + '{}_HIRES_{}_BEAMHSIZE_{}.fits'.format(obsid, band, b))
        data = nan_to_num(hdulist[1].data)
        plots[b].set_ydata( (data[int(sfreq.val)])[:len(plots[b].get_ydata())] )

for i, b in enumerate(beam_sizes[band]):
    if b == 0:
        hdulist = fits.open(fits_dir + '{}_NOMINAL_REGRID_{}.fits'.format(obsid, band))
        print(hdulist[1].data.shape)
    else:
        hdulist = fits.open(fits_dir + '{}_HIRES_{}_BEAMHSIZE_{}.fits'.format(obsid, band, b))
    data = nan_to_num(hdulist[1].data)
    h = data.shape[1]
    plots[b],  = render(data[h // 2], label=b, linewidth=1, linestyle=styles[i])

xlim(h / 4, 3 * h / 4)
ylim(0, 70)
ylabel('Flux MJy/sr')
xlabel('Pixel')
legend(loc=1)

sfreq = Slider(axes([0.18, 0.85, 0.5, 0.02]), 'Y', 0, h, valinit=h // 2, valfmt='%d')
sfreq.on_changed(update)

show()
