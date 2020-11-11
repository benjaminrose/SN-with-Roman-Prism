""" embed2roman.py - produce Roman prism-like spectra from a given SNIa embedding parameters.
"""

from embed2spec import TwinsEmbedding, SNF_BANDS


#From David
#Normalize the SN spectra to -19.1 (+-), then model.flux should be in ergs/cm^2/s/A. That flux can be divided by the “noise” column in the file to make a S/N.

def build_lc(**params):
	"""Creates a light curve with the given model parameters.
	
	From Sam Dixon.
	
	Returns:
		model: `sncosmo.Model` object with the input parameters set.
		lc: `dict` with necessary keys for use in `sncosmo`.
	"""
	model = sncosmo.Model(source=TwinsEmbedding())
	model.set(**params)
	phases = np.arange(-10, 40, 3)
	lc = {'time': [],
		  'band': [],
		  'flux': [],
		  'fluxerr': [],
		  'zp': [],
		  'zpsys': []}
	for band_name, band in SNF_BANDS.items():
		try:
			flux = model.bandflux(time=phases, band=band, zp=0, zpsys='ab')
			fluxerr = 0.05 * max(flux)
			flux += np.random.randn(len(phases)) * fluxerr
			lc['time'] += list(phases)
			lc['flux'] += list(flux)
			lc['fluxerr'] += [fluxerr for _ in phases]
			lc['band'] += [band for _ in phases]
			lc['zp'] += [0 for _ in phases]
			lc['zpsys'] += ['ab' for _ in phases]
		except ValueError:
			continue
	for k, v in lc.items():
		lc[k] = np.array(v)
	return model, lc
	
	
model, lc = build_lc(
	z=0.1,
	dm=35 + np.random.randn(),
	av=np.random.randn() + 1,
	xi1=np.random.randn(),
	xi2=np.random.randn(),
	xi3=np.random.randn()
)

