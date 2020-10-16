# SN with Roman Prism

> Characterizing SN Observations with the Roman ST Prism

## Project Goals

* Given an embedding (c1, c2, & c2), phase, redshift, and Roman ST exposure time, can we recover the original c1, c2, and c3?
* Use `embed2spec` but also need Roman prism specific characteristics.
* Use `???` to fit Roman prism spectra for expected embedding parameters

## Installation

Create a new `conda` environment with 
```
conda env create -f embed2spec/environment.yml
```
and activate it
```
conda activate embed2spec
```

We also require the latest version of `sncosmo` (not yet pip/conda installable). You can install it from source with
```
pip install git+https://github.com/sncosmo/sncosmo.git
```
You need at least v2.2.0.

## Contents

* embed2roman.py - WIP - produce Roman prism-like 1D spectra for a collection of embedding parameters.
* analysis.py - WIP - Do we fit the same embedding parameters we used?