""" embed2roman.py - produce Roman prism-like spectra from a given SNIa embedding parameters.

# SNR scalling

Noise scales proportioanl to (time)**(-1/2) due to poisson noise.
SNCosmo's output handles cosmological dimming.
"""
import warnings

import numpy as np
import sncosmo
import pandas as pd
import matplotlib.pyplot as plt

# import seaborn as sns

from embed2spec import TwinsEmbedding, SNF_BANDS

# sns.set(context="talk", style="ticks", font="serif", color_codes=True)
np.random.seed(419235820)
ROMAN_PRISM_DATA = pd.read_csv(
    "AB_25_1hour.txt", sep="\s+", names=["wave", "SNR", "signal", "noise"], header=0
)


def embed2roman(obs_time=3600, **params):
    """Generate spectra (noiseless & Roman prism-like) for the given model parameters.

    Parameters
    ----------
    obs_time: float
        In seconds. Converts from AB_25_1hour.txt to proper S/N given an
        exposure time in seconds.

    **params:
        parameters for the sncosmo.Model, such as redshift.

    spectrum: sncosmo.Spectrum
        Noiseless source spectra, observer frame



    Returns
    -------
    sncosmo.Model
        The SNCosmo TwinsEmbedding source model object with the input parameters set

    sncosmo.Spectrum
        Noiseless truth spectrum

    sncosmo.Spectrum
        Spectrum with noise and resolution characteristics of the Roman ST prism

    Example
    -------

    Call this function like::

        model, spec_true, spec_roman = embed2roman(
            z=0.8,
            dm=43 + np.random.randn(),
            av=np.random.randn() + 1,
            xi1=np.random.randn(),
            xi2=np.random.randn(),
            xi3=np.random.randn(),
        )
    """
    if obs_time < 200:
        warnings.warn(
            f"Observation time (obs_time) is in seconds. Value of {obs_time} appears to not.",
            RuntimeWarning,
        )

    model = sncosmo.Model(source=TwinsEmbedding())
    model.set(**params)

    # phases = np.arange(-10, 40, 3)
    phases = [0]
    # TwinsEmbedding is defined from ~3300--8600 AA restframe
    # Softcoding is better, since I want full wavelength range
    wave_full = np.arange(model.minwave(), model.maxwave())
    wave_union = (model.minwave() < ROMAN_PRISM_DATA["wave"].values) & (
        ROMAN_PRISM_DATA["wave"].values < model.maxwave()
    )
    wave_roman = ROMAN_PRISM_DATA.loc[wave_union, "wave"].values
    # Scale 1hr exposure noise via Poisson statistics
    noise_roman = ROMAN_PRISM_DATA.loc[wave_union, "noise"].values * (
        obs_time / 3600
    ) ** (-1 / 2)

    flux_true = model.flux(wave=wave_full, time=phases)
    spec_true = sncosmo.Spectrum(wave_full, flux_true[0, :], time=phases[0])

    # From David,
    # Normalize the SN spectra to -19.1 (+-)
    # then model.flux should be in ergs/cm^2/s/A.
    flux_roman = model.flux(wave=wave_roman, time=phases)

    # That flux + obs_noise can be divided by the “noise” column in the file to make a S/N.
    spec_roman = sncosmo.Spectrum(
        wave_roman,
        (flux_roman[0, :] + noise_roman * np.random.randn(len(wave_roman)))
        / noise_roman,
        time=phases[0],
    )

    # what is flux and why would I want it?
    # return model, flux, spectrum
    return model, spec_true, spec_roman


def plot(true, obs, save_fig=False):
    print(min(true.flux), max(true.flux), np.mean(true.flux))
    print(min(obs.flux), max(obs.flux))

    fig, ax = plt.subplots(tight_layout=True)
    # obs is divided by ~ 10-19 error, we need to rescale true.
    ax.plot(true.wave, true.flux / (10 ** (-19)), label=r"Truth divided by $10^{-19}$")
    ax.plot(obs.wave, obs.flux, label="Obs")
    ax.set_ylabel("Signal-to-Noise (per resolution element)")
    ax.set_xlabel("Wavelength (Ang)")
    ax.set_title(f"Redshift 1")
    plt.legend()
    if save_fig:
        plt.savefig(save_fig)
    else:
        plt.show()


if __name__ == "__main__":

    model, spec_true, spec_roman = embed2roman(
        z=1,
        dm=43 + np.random.randn(),  # What is this ?
        av=np.random.randn() + 1,
        xi1=np.random.randn(),
        xi2=np.random.randn(),
        xi3=np.random.randn(),
    )

    print(spec_true.bandflux("sdssz"))
    print(spec_roman.bandflux("sdssz"))

    plot(spec_true, spec_roman, "spec.pdf")
