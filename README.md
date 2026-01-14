# AIA Software Training

Learn the fundamentals of transform-based low-order modelling and analysis

## Developer Guide

### Dependencies

To install the dependencies inside a virtual environment using [venv](https://docs.python.org/3/library/venv.html), run:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Documentation

This repository uses [MkDocs](https://www.mkdocs.org/) to generate a static documentation site for users.
The source files for the site can be found in the [`docs/`](docs) directory and sit configuration in [`mkdocs.yml`](mkdocs.yml).

To serve the site locally, run:

```
mkdocs serve
```

## Project Description

The "required global fleet" can be estimated using a very simple model that assumes:

1. The number of global passengers flying annually is known.
2. The number of seats flown globally per day is known.

### Constants

| True Constant | Value | Unit |
| ------------- | ----- | ---- |
| days per year | $365$ | .    |

| Inputs                       | Value           | Unit        | Source   |
| ---------------------------- | --------------- | ----------- | -------- |
| passengers per year          | $5 \times 10^9$ | $year^{-1}$ | ATAG[^1] |
| seats per aircraft           | $150$           | .           |          |
| flights per aircraft per day | $2$             | $day^{-1}$  |          |

### Equations

Given that the two sourced imputs that are time dependent are given in different time bases, it is convenient to convert one of these so that the two are consistent

$\text{passengers per day} = \frac{\text{passengers per year}}{\text{days per year}}$

The total required global fleet can then be calculated as a function of this intermediate value and the other inputs.

$\text{passengers per day} =\frac{\text{passengers per day}}{\text{seats per aircraft}\times{\text{flights per aircraft per day}}}$

[^1]: [ATAG Facts & Figures](https://atag.org/facts-figures)
