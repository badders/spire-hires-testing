from pylab import *

data = loadtxt('obs-lists/obs-stats.csv', delimiter=',', skiprows=1, unpack=True)
types = loadtxt('obs-lists/obs-types.csv', delimiter=',', skiprows=1, unpack=True)

psw_extra = loadtxt('stats/results-PSW.csv', delimiter=',', skiprows=7, unpack=True)
pmw_extra = loadtxt('stats/results-PMW.csv', delimiter=',', skiprows=7, unpack=True)
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
msize = 2

exgal_test = logical_or(types[2] == 1, types[2] == 2)
gal_test = logical_or(types[2] == 3, types[2] == 4, types[2] == 5)
other_test = logical_not(logical_or(exgal_test, gal_test))

gal_ids = types[0][gal_test]
exgal_ids = types[0][exgal_test]
other_ids = types[0][other_test]

small_ids = types[0][types[1] == 1]
large_ids = types[0][types[1] == 2]
parallel_ids = types[0][types[1] == 3]

small_filter = np.in1d(data[0], small_ids)
large_filter = np.in1d(data[0], large_ids)
parallel_filter = np.in1d(data[0], parallel_ids)

small_filter_pmw = np.in1d(pmw_extra[0], small_ids)
large_filter_pmw = np.in1d(pmw_extra[0], large_ids)
parallel_filter_pmw = np.in1d(pmw_extra[0], parallel_ids)

small_filter_psw = np.in1d(psw_extra[0], small_ids)
large_filter_psw = np.in1d(psw_extra[0], large_ids)
parallel_filter_psw = np.in1d(psw_extra[0], parallel_ids)

gal_filter = np.in1d(data[0], gal_ids)
exgal_filter = np.in1d(data[0], exgal_ids)
other_filter = np.in1d(data[0], other_ids)

gal_filter_psw = np.in1d(psw_extra[0], gal_ids)
exgal_filter_psw = np.in1d(psw_extra[0], exgal_ids)
other_filter_psw = np.in1d(psw_extra[0], other_ids)

gal_filter_pmw = np.in1d(pmw_extra[0], gal_ids)
exgal_filter_pmw = np.in1d(pmw_extra[0], exgal_ids)
other_filter_pmw = np.in1d(pmw_extra[0], other_ids)

def run_filters():
    filt = logical_and(data[2] > 100, data[1] > 10)
    obs_ids_pass = data[0][filt]
    obs_ids_fail = data[0][logical_not(filt)]
    print('PLW: %d pass test' % len(obs_ids_pass))
    print('PLW: %d fail test' % len(obs_ids_fail))
    savetxt('obs-to-hires/plw-pass.csv', obs_ids_pass, fmt='%d')

    filt = logical_and(pmw_extra[7] > 278, pmw_extra[3] > 15)
    obs_ids_pass = pmw_extra[0][filt]
    obs_ids_fail = pmw_extra[0][logical_not(filt)]
    print('PMW: %d pass test' % len(obs_ids_pass))
    print('PMW: %d fail test' % len(obs_ids_fail))
    savetxt('obs-to-hires/pmw-pass.csv', obs_ids_pass, fmt='%d')

    filt = logical_and(psw_extra[9] > 544, psw_extra[3] > 30)
    obs_ids_pass = psw_extra[0][filt]
    obs_ids_fail = psw_extra[0][logical_not(filt)]
    print('PSW: %d pass test' % len(obs_ids_pass))
    print('PSW: %d fail test' % len(obs_ids_fail))
    savetxt('obs-to-hires/psw-pass.csv', obs_ids_pass, fmt='%d')

    print('Halving the area')
    filt = logical_and(data[2] > 50, data[1] > 10)
    obs_ids_pass = data[0][filt]
    obs_ids_fail = data[0][logical_not(filt)]
    print('PLW: %d pass test' % len(obs_ids_pass))
    print('PLW: %d fail test' % len(obs_ids_fail))

    filt = logical_and(pmw_extra[6] > 193, pmw_extra[3] > 15)
    obs_ids_pass = pmw_extra[0][filt]
    obs_ids_fail = pmw_extra[0][logical_not(filt)]
    print('PMW: %d pass test' % len(obs_ids_pass))
    print('PMW: %d fail test' % len(obs_ids_fail))

    filt = logical_and(psw_extra[9] > 270, psw_extra[3] > 30)
    obs_ids_pass = psw_extra[0][filt]
    obs_ids_fail = psw_extra[0][logical_not(filt)]
    print('PSW: %d pass test' % len(obs_ids_pass))
    print('PSW: %d fail test' % len(obs_ids_fail))
    # Pass all
    pass_plw = logical_and(data[2] > 100, data[1] > 10)
    obs_ids_pass_plw = data[0][pass_plw]
    pass_pmw = logical_and(pmw_extra[6] > 287, pmw_extra[3] > 15)
    obs_ids_pass_pmw = pmw_extra[0][pass_pmw]
    pass_psw = logical_and(psw_extra[9] > 544, psw_extra[3] > 30)
    obs_ids_pass_psw = psw_extra[0][pass_psw]

    obs_pass_pmw_psw = obs_ids_pass_pmw[in1d(obs_ids_pass_pmw, obs_ids_pass_psw)]
    obs_pass_plw_psw = obs_ids_pass_plw[in1d(obs_ids_pass_plw, obs_ids_pass_psw)]
    obs_pass_plw_pmw = obs_ids_pass_plw[in1d(obs_ids_pass_plw, obs_ids_pass_pmw)]

    obs_pass_all = obs_ids_pass_plw[in1d(obs_ids_pass_plw, obs_pass_pmw_psw)]
    print('Pass all bands:', len(obs_pass_all))

    # Pass 2
    obs_pass_2_1 = obs_pass_pmw_psw[in1d(obs_pass_pmw_psw, obs_pass_all, invert=True)]
    obs_pass_2_2 = obs_pass_plw_psw[in1d(obs_pass_plw_psw, obs_pass_all, invert=True)]
    obs_pass_2_3 = obs_pass_plw_pmw[in1d(obs_pass_plw_pmw, obs_pass_all, invert=True)]
    obs_pass_2 = concatenate((obs_pass_2_1, obs_pass_2_2, obs_pass_2_3))
    print('Pass 2 Bands:', len(obs_pass_2))

    # Pass 1
    obs_pass_1_1 = obs_ids_pass_psw[in1d(obs_ids_pass_psw, obs_pass_all, invert=True)]
    obs_pass_1_2 = obs_ids_pass_pmw[in1d(obs_ids_pass_pmw, obs_pass_all, invert=True)]
    obs_pass_1_3 = obs_ids_pass_plw[in1d(obs_ids_pass_plw, obs_pass_all, invert=True)]
    obs_pass_1 = concatenate((obs_pass_1_1, obs_pass_1_2, obs_pass_1_3))
    obs_pass_1 = obs_pass_1[in1d(obs_pass_1, obs_pass_2, invert=True)]
    print('Pass 1 Bands:', len(obs_pass_1))

    # > threshold buts less than 5 SNR:
    filt = logical_and(data[1] < 5, data[2] > 279)
    obs_ids = data[0][filt]
    savetxt('obs-lists/ids-abovethresh-lowsnr.csv', obs_ids, fmt='%d')

    # < threshold but above 17 SNR
    filt = logical_and(data[1] > 17, data[2] < 100)
    obs_ids = data[0][filt]
    savetxt('obs-lists/ids-belowthresh-highsnr.csv', obs_ids, fmt='%d')

    # Nearby Thresholds
    filt = logical_and(data[1] > 5, data[1] < 15)
    filt2 = logical_and(data[2] > 50, data[2] < 200)
    filt = logical_and(filt, filt2)
    obs_ids = data[0][filt]
    #passes_pixcount = zeroes_like(obs_ids)

    savetxt('obs-lists/nearby.csv', obs_ids, fmt='%d')

def do_plots():
    figure(figsize=(5,6))

    loglog(data[1][exgal_filter], data[2][exgal_filter], '.', markersize=msize, label='ExGal')
    loglog(data[1][gal_filter], data[2][gal_filter], '.', markersize=msize, label='Galactic')
    loglog(data[1][other_filter], data[2][other_filter], '.', markersize=msize, label='Other')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 20 MJy/sr')
    title('PLW')
    xl = xlim()
    yl = ylim()
    ylim(0,10**7)
    hlines(100, *xl, colors='r')
    vlines(10, *yl, colors='r')

    legend(loc=2, numpoints=1, fontsize=10, markerscale=msize*2)
    savefig('doc/stats-both-thresholds.pdf')

    figure(figsize=(16,7))
    subplot(131)

    loglog(data[1][exgal_filter], data[2][exgal_filter], '.', markersize=msize, label='ExGal')
    loglog(data[1][gal_filter], data[2][gal_filter], '.', markersize=msize, label='Galactic')
    loglog(data[1][other_filter], data[2][other_filter], '.', markersize=msize, label='Other')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 20 MJy/sr')
    title('PLW')
    xl = xlim()
    ylim(0,10**7)
    hlines(100, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=msize*2)

    subplot(132)

    loglog(data[4][exgal_filter], data[5][exgal_filter], '.', markersize=msize, label='ExGal')
    loglog(data[4][gal_filter], data[5][gal_filter], '.', markersize=msize, label='Galactic')
    loglog(data[4][other_filter], data[5][other_filter], '.', markersize=msize, label='Other')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 20 MJy/sr')
    title('PMW')
    xl = xlim()
    hlines(278.8, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=msize*2)

    subplot(133)
    loglog(data[7][exgal_filter], data[8][exgal_filter], '.', markersize=msize, label='ExGal')
    loglog(data[7][gal_filter], data[8][gal_filter], '.', markersize=msize, label='Galactic')
    loglog(data[7][other_filter], data[8][other_filter], '.', markersize=msize, label='Other')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 20 MJy/sr')
    title('PSW')
    xl = xlim()
    hlines(544.4, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=msize*2)

    tight_layout()
    savefig('doc/snr-thresholds.pdf')

    ##### PMW Pixels > 30 MJy
    figure()
    loglog(pmw_extra[3][exgal_filter_pmw], pmw_extra[6][exgal_filter_pmw], '.', markersize=msize, label='ExGal')
    loglog(pmw_extra[3][gal_filter_pmw], pmw_extra[6][gal_filter_pmw], '.', markersize=msize, label='Galactic')
    loglog(pmw_extra[3][other_filter_pmw], pmw_extra[6][other_filter_pmw], '.', markersize=msize, label='Other')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 30 MJy/sr')
    title('PMW')
    xl = xlim()
    hlines(278.8, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=msize*2)
    savefig('doc/snr-thresholds-pmw30.pdf')

    ##### PSW Pixels > 100 MJy
    figure()
    loglog(psw_extra[3][exgal_filter_psw], psw_extra[9][exgal_filter_psw], '.', markersize=msize, label='ExGal')
    loglog(psw_extra[3][gal_filter_psw], psw_extra[9][gal_filter_psw], '.', markersize=msize, label='Galactic')
    loglog(psw_extra[3][other_filter_psw], psw_extra[9][other_filter_psw], '.', markersize=msize, label='Other')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 100 MJy/sr')
    title('PSW')
    xl = xlim()
    hlines(544.4, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=msize*2)
    savefig('doc/snr-thresholds-psw100.pdf')

    # Plot same but for different split
    figure(figsize=(16,7))
    subplot(131)

    loglog(data[1][large_filter], data[2][large_filter], '.', markersize=msize, label='Large')
    loglog(data[1][small_filter], data[2][small_filter], '.', markersize=msize, label='Small')
    loglog(data[1][parallel_filter], data[2][parallel_filter], '.', markersize=msize, label='Parallel')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 20 MJy/sr')
    title('PLW')

    xl = xlim()
    ylim(0,10**7)
    hlines(100, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=msize*2)

    subplot(132)
    loglog(pmw_extra[3][large_filter_pmw], pmw_extra[6][large_filter_pmw], '.', markersize=msize, label='Large')
    loglog(pmw_extra[3][small_filter_pmw], pmw_extra[6][small_filter_pmw], '.', markersize=msize, label='Small')
    loglog(pmw_extra[3][parallel_filter_pmw], pmw_extra[6][parallel_filter_pmw], '.', markersize=msize, label='Parallel')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 30 MJy/sr')
    title('PMW')
    ylim(0,10**7)
    xl = xlim()
    hlines(278.8, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=msize*2)

    subplot(133)
    loglog(psw_extra[3][large_filter_psw], psw_extra[9][large_filter_psw], '.', markersize=msize, label='Large')
    loglog(psw_extra[3][small_filter_psw], psw_extra[9][small_filter_psw], '.', markersize=msize, label='Small')
    loglog(psw_extra[3][parallel_filter_psw], psw_extra[9][parallel_filter_psw], '.', markersize=msize, label='Parallel')

    xlabel('99th Percentile Signal')
    ylabel('Pixel Count > 100 MJy/sr')
    title('PSW')
    xl = xlim()
    hlines(544.4, *xl, colors='r')
    legend(loc=2, numpoints=1, fontsize=10, markerscale=msize*2)
    savefig('doc/snr-thresholds-byobstype.pdf')
    show()

if __name__ == '__main__':
    #do_plots()
    run_filters()
