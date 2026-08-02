# Changelog

All notable changes and key methodology decisions for this project are documented here.

## [Unreleased]

### Added
- `CITATION.cff` for proper academic citation (accompanying paper: DOI 10.5281/zenodo.21422532).

## Methodology Notes

### RNN branch reframing
The RNN branch was originally scoped and described as "AIS spoofing detection." Given that spoofing
(AIS transmitting but with falsified position) cannot be reliably confirmed from the available Global
Fishing Watch data, this branch was repositioned as **positional and confidence anomaly detection**
between consecutive vessel detections — a claim the data actually supports.

### Paper corrections
The accompanying research paper had section numbering fixed, abstract overclaims walked back to match
reported metrics, and unverifiable citations removed prior to Zenodo publication.
