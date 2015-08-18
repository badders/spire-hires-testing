# Settings
outDir = "/Users/Tom/HIPE/plots/SPIRE/"

# M74, NGC4151, M81
obsids = [1342189427, 1342188588, 1342185538, 1342249237]
bands = ['PLW', 'PMW', 'PSW']

beamSizes = {
    'PLW' : [20, 50, 100, 125, 150],
    'PMW' : [15, 35, 65, 100, 125],
    'PSW' : [10, 25,  50, 70, 100],
}

for obsid in obsids:
    for band in bands:
        beamSize = beamSizes[band][0]
        nominal = simpleFitsReader(outDir + '%d_NOMINAL_%s.fits' % (obsid, band))
        hires = simpleFitsReader(outDir + str(obsid) + '_HIRES_' + band +'_BEAMHSIZE_' + str(beamSize) + '.fits')
        rnom = regrid(source=nominal, target=hires)
        rnom = imageMultiply(rnom, 4)
        simpleFitsWriter(rnom, outDir + '%d_NOMINAL_REGRID_%s.fits' % (obsid, band))

