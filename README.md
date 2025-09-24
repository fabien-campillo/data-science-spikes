# README
This repository contains a Jupyter Book called **Data Science & Spikes**  designed to help you get started in data science by exploring electrophysiological data, especially spike train recordings, in a practical and accessible way.

To install and run a Jupyter Book (or any Jupyter Notebook project), it is recommended to use a dedicated `conda` virtual environment defined in an `environment.yml` file:

**1.** create the virtual environment from the file `environment.yml`:

```bash
conda env create -f environment.yml
```

**2.**  and activate the environment:

```bash
conda activate python-dsspikes-env
```
(`python-dsspikes-env` is the name of the virtual environment)

**3.** if the virtual environment already exists and you want to update it:

```bash
conda env update -f environment.yml --prune
```
(`--prune` removes dependencies no longer listed in the YAML.)


`environment.yml ` is the YAML specification file of the Conda environment.

<br>

The present version of `environment.yml`

```yml
name: python-dsspikes-env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy=1.26  # compatible version for macOS
  - matplotlib=3.8
  - pandoc=3.8=h694c41f_0
  - seaborn=0.12
  - jupyter-book=1.0.4
  - jupyterlab=4.1
  - ipykernel
  - pip
  - pip:
      - pyabf==2.3.8  # install via pip
```
all installed with `conda` ecxept `pylab` only available with `pip`.

[Fabien Campillo](https://www-sop.inria.fr/members/Fabien.Campillo/index.html)


[![Jupyter Book Badge](https://jupyterbook.org/badge.svg)](https://fabien-campillo.github.io/data-science-spikes/)