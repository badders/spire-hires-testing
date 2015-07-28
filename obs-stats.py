datafile = '/Users/Tom/Projects/spire-hires-testing/obs.csv'

data = asciiTableReader(file=datafile, columnNames=True, tableType='ADVANCED', columnType=AsciiParser.GUESS_ALL)

data_range = (0, 78)

obs_ids = data[0].getData()

x = obs_ids[data_range[0]:data_range[1]]
bands = ['PLW']

flux_totals = []
flux_medians = []
signal_99s = []

for id in x:
    obsIn = getObservation(obsid=id, useHsa=True, instrument='SPIRE')
    l2_image = obsIn.level2.getProduct('extdPLW').image
    flux_total = sum(l2_image[l2_image.where(IS_FINITE(l2_image))])
    
    d = SORT(RESHAPE(l2_image))
    d = d[d.where(IS_FINITE(d))]
    assert(len(d) > 100)
    k = int(CEIL(len(d) * .99))
    signal_99 = d[k]
    
    flux_median = MEDIAN(NAN_FILTER(d))
    
    flux_totals.append(flux_total)
    flux_medians.append(flux_median)
    signal_99s.append(signal_99)
    
results = TableDataset(description='Observation Analysis')
results['Observation ID'] = Column(x)
results['Total Flux'] = Column(Float1d(flux_totals))
results['Median Flux'] = Column(Float1d(flux_medians))
results['99th Percentile Signal'] = Column(Float1d(signal_99s))
    