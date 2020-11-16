""" embed2roman.py - produce Roman prism-like spectra from a given SNIa embedding parameters.
"""

import numpy as np
import sncosmo

from embed2spec import TwinsEmbedding, SNF_BANDS


# From David
# Normalize the SN spectra to -19.1 (+-), then model.flux should be in ergs/cm^2/s/A. That flux can be divided by the “noise” column in the file to make a S/N.

ROMAN_PRISM_DATA = pd.read_csv(
    "AB_25_1hour.txt", sep="\s+", names=["wave", "SNR", "signal", "noise"], header=0
)

def build_lc(**params):
    """Creates a light curve with the given model parameters.

    From Sam Dixon.

    Returns:
            model: `sncosmo.Model` object with the input parameters set.
            lc: `dict` with necessary keys for use in `sncosmo`.
    """
    model = sncosmo.Model(source=TwinsEmbedding())
    model.set(**params)

    # phases = np.arange(-10, 40, 3)
    phases = [0]
    # TwinsEmbedding is defined from ~3300--8600 AA restframe
    # Softcoding is better, since I want full wavelength range
    wave_full = np.arange(model.minwave(), model.maxwave())
    wave_union = (model.minwave() < ROMAN_PRISM_DATA["wave"].values) & (ROMAN_PRISM_DATA["wave"].values < model.maxwave())
    wave_roman = ROMAN_PRISM_DATA.loc[wave_union, "wave"].values

    flux_true = model.flux(wave=wave_full, time=phases)
    spec_true = sncosmo.Spectrum(wave_full, flux_true[0, :], time=phases[0])

    # From David,
    # Normalize the SN spectra to -19.1 (+-)
    # then model.flux should be in ergs/cm^2/s/A. 
    flux_roman = model.flux(wave=wave_roman, time=phases)

    # That flux can be divided by the “noise” column in the file to make a S/N.
    spec_roman = sncosmo.Spectrum(wave_roman, flux_roman[0, :]/ROMAN_PRISM_DATA.loc[wave_union, "noise"].values, time=phases[0])


    #what is flux and why would I want it?
    # return model, flux, spectrum
    return model, spec_true, spec_roman

if __name__ == "__main__":

    model, spec_true, spec_roman = embed2roman(
        z=0.8,
        dm=35 + np.random.randn(),   # What is this ? 
        av=np.random.randn() + 1,
        xi1=np.random.randn(),
        xi2=np.random.randn(),
        xi3=np.random.randn(),
    )

    print(spec_true.bandflux("sdssz"))
    print(spec_roman.bandflux("sdssz"))
