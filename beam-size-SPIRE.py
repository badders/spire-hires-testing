# Settings
outDir = "/Users/Tom/HIPE/plots/SPIRE/"

# M74, NGC4151, M81
obsids = [1342189427, 1342188588, 1342185538]
bands = ['PLW', 'PMW', 'PSW']

beamSizes = {
    'PLW' : [20, 50, 100, 125, 150],
    'PMW' : [15, 35, 65, 100, 125],
    'PSW' : [10, 25,  50, 70, 100],
}

########## DEBUG #############################
obsids = [1342249237]
bands = ['PLW']

beamSizes = {
    'PLW' : [50]
}
##############################################


# Get the observation from the archive if not already stored in the pool locally
def loadObservation(obsid):
    print 'Downloading from HSA ...'
    obs = getObservation(obsid=obsid, useHsa=True, instrument='SPIRE')
    obs.refs.remove('level0')
    obs.refs.remove('level0_5')
    return obs

def loadBeams(obsIn):
    fullBeams = {}
    for band in bands:
        fullBeams[band] = obsIn.calibration.getPhot().getProduct('BeamProfList').getProduct(band, 'fine')
    return fullBeams

def processHiRes(inLevel1, inArray, inBeam, inWcs, inMapMin, inMapMax):
    level1 = Level1Context()
    selectRefs = filter(lambda x:x.meta['bbid'].value>>16==0xa103, inLevel1.refs)
    for ref in selectRefs: 
        level1.addProduct(ref.getProduct().copy())

    wcs = inWcs.copy()

    #Update wcs cdelt, naxis and crpix values
    keyMap = {'cdelt':[float, 0.5], 'naxis':[int, 2.], 'crpix':[float, 2.]}
    map(lambda x: wcs.meta[x].setValue(keyMap[x[:-1]][0](wcs.meta[x].value*keyMap[x[:-1]][1])) , \
        map(lambda x:keyMap.keys()[x/2]+str(x%2+1), range(2*len(keyMap.keys()))))

    hiresImage, hiresBeam = hiresMapper(level1, array = inArray, beam=inBeam, wcs=wcs)
    tempIndx = hiresImage.image.where((hiresImage.image>2*inMapMax).or(hiresImage.coverage<1e-10))
    hiresImage.image[tempIndx] = Double.NaN
    return hiresImage


for obsid in obsids:
    obs = loadObservation(obsid)
    # Save out nominal maps
    for band in bands:
        nominal = obs.level2.getProduct("psrc"+band)
        simpleFitsWriter(nominal, outDir + 'NOMINAL_%d.fits' % obsid)

    # Generate HiRes maps for each observation at all the beam sizes
    fullBeams = loadBeams(obs)

    for band in bands:
        level1 = obs.getLevel1()

        for beamSize in beamSizes[band]:
            bcenter = fullBeams[band].image.dimensions
            bcenter[0] = bcenter[0] / 2
            bcenter[1] = bcenter[1] / 2
            beam = crop(fullBeams[band], int(bcenter[0] - beamSize) , int(bcenter[1] - beamSize), int(bcenter[0] + beamSize+1), int(bcenter[1] + beamSize+1))
            
            level2 = obs.level2
            wcs = level2.getProduct('extd%s'%band).wcs
            mapMax = MAX(level2.getProduct('psrc%s'%band).image[\
                level2.getProduct('psrc%s'%band).image.where(IS_FINITE)])
            mapMin = MIN(level2.getProduct('psrc%s'%band).image[\
                level2.getProduct('psrc%s'%band).image.where(IS_FINITE)])
            tempMap = processHiRes(level1, band, beam, wcs, mapMin, mapMax)
            simpleFitsWriter(tempMap, outDir + str(obsid) + '_HIRES_' + band +'_BEAMHSIZE_' + str(beamSize) + '.fits')