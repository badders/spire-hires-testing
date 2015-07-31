datafile = '/home/ug/c1145457/spire-hires-testing/obs.csv'

data = asciiTableReader(file=datafile, columnNames=True, tableType='ADVANCED', columnType=AsciiParser.GUESS_ALL)

data_range = (0, 78)

obs_ids = data[0].getData()

x = obs_ids[data_range[0]:data_range[1]]
bands = ['PLW', 'PMW', 'PSW']

thresholds = [10, 20, 30, 40, 50, 100, 300]

test_thresholds = {
	'PLW' : 100,
	'PMW' : 300,
	'PSW' : 400
}

results_tables = {}

for band in bands:
    flux_totals = []
    flux_medians = []
    signal_99s = []
    
    threshold_results = {}
    
    for t in thresholds:
        threshold_results[t] = []
    
    for id in x:
        obsIn = getObservation(obsid=id, useHsa=True, instrument='SPIRE')
        l2_image = obsIn.level2.getProduct('extd%s' % band).image
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
        
        for t in thresholds:
            threshold_results[t].append((d.where(d>t)).length())
        
    results = TableDataset(description='Observation Analysis')
    results['Observation ID'] = Column(x)
    results['Total Flux'] = Column(Float1d(flux_totals))
    results['Median Flux'] = Column(Float1d(flux_medians))
    results['99th Percentile Signal'] = Column(Float1d(signal_99s))
        
    for t in thresholds:
        results['Pixels > %d' % t] = Column(Float1d(threshold_results[t]))
        
    results_tables[band] = results
    asciiTableWriter(table=results, file='/home/ug/c1145457/results-%s.csv' % band)
    
# Check for pass/fails on each set of data
pfres = TableDataset(description='Threshold Checking')
pfres['Observation ID'] = Column(x)
pass_res_tot = Int1d(len(x))
for band in bands:
    col = results_tables[band]['Pixels > 20']
    pass_res = Int1d(len(col.data))
    pass_res[col.data.where(col.data >= test_thresholds[band])] = 1
    pass_res_tot += pass_res
    pfres['%s Pix> 20' % band] = Column(pass_res)
pfres['Total Pass'] = Column(pass_res_tot)
asciiTableWriter(table=pfres, file='/home/ug/c1145457/hires_check.csv' % band)