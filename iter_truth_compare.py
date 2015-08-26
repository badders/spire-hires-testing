from common import *

fitsDir = '/Users/Tom/HIPE/plots/iter_truth/'
obsid = 1342185538
band = 'PLW'

truth_data = fits.open(fitsDir + str(obsid) + '_TRUTH_' + band + '.fits')[1].data

mask = zeros_like(truth_data)
w, h = truth_data.shape
cx, cy = w // 2, h // 2
r = 70

for i in range(w):
    for j in range(h):
        if (i - cx)**2 + (j-cy)**2 < r**2:
            mask[i][j] = 1

iters = range(0, 81)
diffs = []
truth_data = nan_to_num(truth_data) * mask

for i in iters:
    if i == 0:
        image_data = fits.open(fitsDir + str(obsid) + '_NOMINAL_' + band + '.fits')[1].data
    else:
        image_data = fits.open(fitsDir + str(obsid) + '_HIRES_' + band + '_' + str(i) + '.fits')[1].data

    image_data = nan_to_num(image_data) * mask
    normal_image_data = image_data * (truth_data.sum() / image_data.sum())

    diff_data = truth_data - normal_image_data
    diff_data = diff_data * mask

    diff = (diff_data**2).sum() / mask.sum()
    diffs.append(sqrt(diff))

plot(iters, diffs, label='Truth - Hires')
xlabel('Number of Iterations')
ylabel('RMS Pixel Differnce')
legend()

show()
