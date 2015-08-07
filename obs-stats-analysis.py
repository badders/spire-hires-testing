from pylab import *

data = loadtxt('obs-lists/obs-stats.csv', delimiter=',', skiprows=1, unpack=True)
types = loadtxt('obs-lists/obs-types.csv', delimiter=',', skiprows=1, unpack=True)

# Extra Galactic
# GAL = 1
# COS = 2

# Glactic
# STA = 3
# ISM = 4
# SOL = 5

# Everything else/unknown
# TOO = 6
# DDT = 7

# Obs Modes
# Small = Type 1
# Large = Type 2
# Parallel = Type 3

exgal_test = logical_or(types[2] == 1, types[2] == 2)
gal_test = logical_or(types[2] == 3, types[2] == 4, types[2] == 5)
other_test = logical_not(logical_or(exgal_test, gal_test))

gal_ids = types[0][gal_test]
exgal_ids = types[0][exgal_test]
other_ids = types[0][other_test]
msize = 2

gal_filter = np.in1d(data[0], gal_ids)
exgal_filter = np.in1d(data[0], exgal_ids)
other_filter = np.in1d(data[0], other_ids)

def run_filters():
    # > threshold buts less than 5 SNR:
    filt = logical_and(data[1] < 5, data[2] > 279)
    obs_ids = data[0][filt]
    savetxt('obs-lists/ids-abovethresh-lowsnr.csv', obs_ids, fmt='%d')

    filt = logical_and(data[1] > 17, data[2] < 100)
    obs_ids = data[0][filt]
    savetxt('obs-lists/ids-belowthresh-highsnr.csv', obs_ids, fmt='%d')

def do_plots():
    figure(figsize=(16,7))
    subplot(131)

    loglog(data[1][exgal_filter], data[2][exgal_filter], '.', markersize=msize, label='ExGal')
    loglog(data[1][gal_filter], data[2][gal_filter], '.', markersize=msize, label='Galactic')
    loglog(data[1][other_filter], data[2][other_filter], '.', markersize=msize, label='Other')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 20 MJ/sr')
    title('PLW')
    xl = xlim()
    ylim(0,10**7)
    hlines(100, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=4)

    subplot(132)

    loglog(data[4][exgal_filter], data[5][exgal_filter], '.', markersize=msize, label='ExGal')
    loglog(data[4][gal_filter], data[5][gal_filter], '.', markersize=msize, label='Galactic')
    loglog(data[4][other_filter], data[5][other_filter], '.', markersize=msize, label='Other')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 20 MJ/sr')
    title('PMW')
    xl = xlim()
    hlines(278.8, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=4)

    subplot(133)
    loglog(data[7][exgal_filter], data[8][exgal_filter], '.', markersize=msize, label='ExGal')
    loglog(data[7][gal_filter], data[8][gal_filter], '.', markersize=msize, label='Galactic')
    loglog(data[7][other_filter], data[8][other_filter], '.', markersize=msize, label='Other')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 20 MJ/sr')
    title('PSW')
    xl = xlim()
    hlines(544.4, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=4)

    tight_layout()
    show()

if __name__ == '__main__':
    do_plots()
    run_filters()
