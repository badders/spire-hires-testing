obsid = 1342249237
band = 'PLW'
obs = getObservation(obsid=obsid, useHsa=True, instrument='SPIRE')
beam = obs.calibration.getPhot().getProduct('BeamProfList').getProduct(band, 'fine')

# n.b. this is copied from the the pipeline
def processHiRes(inLevel1, inArray, inBeam, inWcs, inMapMin, inMapMax, fluxOffsets):
    level1 = Level1Context()
    selectRefs = filter(lambda x:x.meta['bbid'].value>>16==0xa103, inLevel1.refs)
    for ref in selectRefs: 
        level1.addProduct(ref.getProduct().copy())

    wcs = inWcs.copy()

    #Update wcs cdelt, naxis and crpix values
    keyMap = {'cdelt':[float, 0.5], 'naxis':[int, 2.], 'crpix':[float, 2.]}
    map(lambda x: wcs.meta[x].setValue(keyMap[x[:-1]][0](wcs.meta[x].value*keyMap[x[:-1]][1])) , \
        map(lambda x:keyMap.keys()[x/2]+str(x%2+1), range(2*len(keyMap.keys()))))

    hiresImage, hiresBeam = hiresMapper(level1, array = inArray, beam=inBeam, wcs=wcs, fluxOffset=fluxOffsets)
    tempIndx = hiresImage.image.where((hiresImage.image>5*inMapMax).or(hiresImage.coverage<1e-10))
    hiresImage.image[tempIndx] = Double.NaN
    return hiresImage

level1 = obs.getLevel1()
level2 = obs.getLevel2()
    
# Apply relative gaines
chanRelGains = obs.calibration.getPhot().chanRelGain
DEBUG_pre_relgains = naiveScanMapper(level1)

level1RelGains = Level1Context()
    
for i in range(level1.getCount()):
    psp = level1.getProduct(i)
    if psp.type=="PPT": psp.setType("PSP") #for old Level 1 contexts
    psp = applyRelativeGains(psp, chanRelGains)
    level1RelGains.addProduct(psp)


#level1RelGains = level1
# Apply destriper
diag = level2.getProduct('extd%sdiag'%band)
DEBUG_pre_destriper = naiveScanMapper(level1RelGains)
akjahsdkhjas
level1Corrected,mapZero,diagZero, p4,p5 = destriper(level1=level1RelGains, array=band, withMedianCorrected=True, startParameters=diag)

# Generate beam for hires
beamSize = 80
bcenter = beam.image.dimensions
bcenter[0] = bcenter[0] / 2
bcenter[1] = bcenter[1] / 2
beam = crop(beam, int(bcenter[0] - beamSize) , int(bcenter[1] - beamSize), int(bcenter[0] + beamSize+1), int(bcenter[1] + beamSize+1))

wcs = level2.getProduct('extd%s'%band).wcs
mapMax = MAX(level2.getProduct('extd%s'%band).image[\
    level2.getProduct('extd%s'%band).image.where(IS_FINITE)])
mapMin = MIN(level2.getProduct('extd%s'%band).image[\
    level2.getProduct('extd%s'%band).image.where(IS_FINITE)])

# Get flux offsets
fluxOffsetsExtd = level2.getProduct('extd%s'%band).meta['zPointOffset'].value
beamAreaPipSr = obs.calibration.getPhot().getProduct('ColorCorrBeam').meta['beamPipeline%sSr'%band.capitalize()].value
fluxOffsetsPsrc = fluxOffsetsExtd * 1.e6 * beamAreaPipSr
# Run hires with flux offsets
DEBUG_pre_hires = naiveScanMapper(level1Corrected)
tempMap = processHiRes(level1Corrected, band, beam, wcs, mapMin, mapMax, fluxOffsetsPsrc)
DEBUG_post_hires = tempMap.copy()
# Remove flux offset 
mapHiresPsrcNew = imageSubtract( image1=tempMap, scalar=fluxOffsetsPsrc)
# Convert units to MJy/sr
beamAreaPipArc = obs.calibration.getPhot().getProduct('ColorCorrBeam').meta['beamPipeline%sArc'%band.capitalize()].value
mapHiresExtdNew = convertImageUnit(image=mapHiresPsrcNew,beamArea=beamAreaPipArc,newUnit='MJy/sr')
k4P = obs.calibration.getPhot().getProduct('FluxConvList')[0].meta['k4P_%s'%band].value
k4E = obs.calibration.getPhot().getProduct('FluxConvList')[0].meta['k4E_%s'%band].value

mapHiresExtdNew = imageDivide(image1=mapHiresExtdNew,scalar=k4P)
mapHiresExtdNew = imageMultiply(image1=mapHiresExtdNew,scalar=k4E)
mapHiresExtdNew = imageAdd(image1=mapHiresExtdNew,scalar=fluxOffsetsExtd)
