import sys
print(sys.version)

from pylab import *
from astropy.io import fits
from matplotlib.widgets import Slider, RadioButtons
import glob
import re

# Settings
fits_dir = "/Users/Tom/HIPE/plots/iter_test/"

band = 'PLW' #, 'PMW', 'PSW'

fig = figure()
plots = {}

styles = list(reversed(['-', '--', '-.', ':']))
render = plot

def update(_):
    for n in files:
        hdulist = fits.open(files[n])
        data = nan_to_num(hdulist[1].data)
        plots[n].set_ydata( (data[int(sfreq.val)])[:len(plots[n].get_ydata())] )

files_orig = {}
for fname in glob.glob(fits_dir + band + '*.fits'):
    n = int(re.findall('\d+', fname)[0])
    files_orig[n] = fname

plot_iters = [5, 10, 15, 20]
files = {k: v for k, v in files_orig.items() if k in plot_iters}

for i, n in enumerate(sort([k for k, v in files.items()])):
    hdulist = fits.open(files[n])
    data = nan_to_num(hdulist[1].data)
    h = data.shape[1]
    plots[n],  = render(data[h // 2], label=n, linewidth=1, linestyle=styles[i % len(styles)])

xlim(h / 4, 3 * h / 4)
ylim(0, 150)
ylabel('Flux MJy/sr')
xlabel('Pixel')
legend(loc=1)

sfreq = Slider(axes([0.18, 0.85, 0.5, 0.02]), 'Y', 0, h, valinit=h // 2, valfmt='%d')
sfreq.on_changed(update)

figure()
n = sort([k for k, v in files_orig.items()])

hdulist = fits.open(files_orig[n[0]])
max_image = nan_to_num(hdulist[1].data)
h,w = max_image.shape
#max_image = max_image[w//4:h//4,3*w//4:3*h//4 ]

diffs = zeros_like(n)

for i in n:
    hdulist = fits.open(files_orig[i])
    data = nan_to_num(hdulist[1].data)
    diffs[i-1] = sqrt(((max_image - data)**2).mean())

ylabel('RMS Pixel Difference from 1 Iteration')
xlabel('Number of Iterations')

plot(n, diffs)
plot(n, diffs, 'kx')
savefig('doc/iter-rms.pdf')

# Plot Thumbs
figure()
k, fs = files.items()

for i, k in enumerate(k):
    subplot(4,1,i+1)
    

show()
