from common import *
from astropy import wcs
from scipy.optimize import curve_fit
import aplpy

beams = [25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 125, 150, 200, 250]
bands = ['PLW', 'PMW', 'PSW']

mask_radii = {
    'PLW' : 50,
    'PMW' : 100,
    'PSW' : 200
}

minima_locks = {
    'PLW' : [],
    'PMW' : [],
    'PSW' : []
}

for band in bands:
    truth_hdulist = fits.open('/Users/Tom/HIPE/plots/TRUTH_m74_{}.fits'.format(band))

    truth_image = truth_hdulist[1].data
    truth_wcs = wcs.WCS(truth_hdulist[1].header)

    mask_image = truth_image.copy()
    w, h = mask_image.shape
    cx, cy = w // 2 - w // 20, h//2 + h // 20
    r_max = mask_radii[band]

    for i in range(w):
        for j in range(h):
            r = sqrt((cx - j)**2 + (cy - i)**2)
            if r < r_max:
                mask_image[i][j] = 1
            else:
                mask_image[i][j] = 0

    truth_image = nan_to_num(truth_image)
    truth_image *= mask_image
    truth_peak = truth_image.max()

    # imshow(truth_image)
    figure()
    render = plot
    hires_differences = []
    hires_diff_maps = []

    for b in beams:
        hdulist = fits.open('/Users/Tom/HIPE/plots/HIRES_{}_BEAMHSIZE_{}.fits'.format(band, b))
        hires_image = hdulist[1].data

        hires_image *= mask_image
        hires_image *= (nansum(truth_image) / nansum(hires_image))

        im_diff = truth_image - hires_image
        hires_diff_maps.append(im_diff)
        hires_differences.append(sqrt(nanfilter(truth_image - hires_image)**2).sum() / mask_image.sum())

    exp_decay = lambda x, A, t, y0: A * np.exp(x-50 * t) + y0
    params, cov = curve_fit(exp_decay, beams, hires_differences, p0=[0.0001, -150, 0.00001])
    print(params)

    # if band == 'PMW':
    #     render(beams[:-1], hires_differences[:-1], label=band)
    # else:
    render(beams, hires_differences, label=band)

    print('\t'.join([str(x) for x in beams]))
    print('\t'.join([str(x) for x in hires_differences]))
    legend(loc='best')
    xlabel('Beam Half Pixel Size')
    ylabel('RMS Image Pixel Difference')
    grid()

    x = linspace(*xlim(), num=200)
    y = exp_decay(x+50, *params)

    #plot(x, y)

    tight_layout()
    savefig('doc/beam-size-{}.pdf'.format(band))
show()
