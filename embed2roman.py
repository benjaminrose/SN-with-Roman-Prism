""" embed2roman.py - produce Roman prism-like spectra from a given SNIa embedding parameters.
"""

import numpy as np
import sncosmo

from embed2spec import TwinsEmbedding, SNF_BANDS


# From David
# Normalize the SN spectra to -19.1 (+-), then model.flux should be in ergs/cm^2/s/A. That flux can be divided by the “noise” column in the file to make a S/N.


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
    # TwinsEmbedding is defined from ~3300--8600 AA restframe
    # Softcoding is better, since I want full wavelength range
    wave = np.arange(model.minwave(), model.maxwave())

    flux = model.flux(wave=wave, time=phases)
    spectrum = sncosmo.Spectrum(wave, flux[0, :], time=phases[0])

    return model, flux, spectrum


if __name__ == "__main__":
    print("running")

    model, flux, spec = build_lc(
        z=0.1,
        dm=35 + np.random.randn(),
        av=np.random.randn() + 1,
        xi1=np.random.randn(),
        xi2=np.random.randn(),
        xi3=np.random.randn(),
    )

    print(spec.bandflux("sdssr"))
