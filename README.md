# ct-covid19-triage-prediction
# CT-based Patient Triage of COVID-19: Radiomics Prediction of ICU Admission, Mechanical Ventilation, and Death

## Overview

This project implements an end-to-end pipeline to predict ICU admission, mechanical ventilation, and death for COVID-19 patients using radiomics features extracted from chest CT scans combined with clinical data. It includes automated lung segmentation, feature extraction, and machine learning using Random Forest models.

## Repository Structure

- `discover_patients.py` - Identify eligible patients with complete CT and clinical data
- `batch_segmentation.py` - Automated lung segmentation of CT images
- `batch_feature_extraction.py` - Radiomics features extraction
- `run_all_patients.py` - Pipeline orchestration script
- `complete_triage_prediction.py` - ML prediction models training and evaluation
- `Dockerfile` - Docker environment setup
- `docker-compose.yaml` - Compose file for Docker container
- `README.md` - This file

## Getting Started

### Requirements

- Docker installed (preferred)
- Or Python 3.8+ with packages: numpy, pandas, scikit-learn, SimpleITK, pyradiomics

### Setup Docker (Recommended)

Build Docker image:
docker run -it -v $(pwd):/app covid-triage /bin/bash


### Install Python Packages (Non-Docker)
pip install numpy pandas scikit-learn SimpleITK pyradiomics


## Running the Pipeline

Execute steps sequentially inside Docker or your Python environment:

1. Discover Patients
python discover_patients.py

2. Segment Lung CT Scans
python batch_segmentation.py


3. Extract Radiomics Features
python batch_feature_extraction.py


4. Predict Clinical Outcomes (ICU admission, ventilation, death)
python complete_triage_prediction.py


The predictions will be saved as `complete_covid_triage_all_predictions.csv` in the `/app/results/` directory.

## Results Summary

| Outcome                | Prevalence (%) | AUC Score |
|------------------------|----------------|-----------|
| ICU Admission          | 29.5           | 0.725     |
| Mechanical Ventilation | 24.6           | 0.681     |
| Death                  | 18.0           | 0.217     |

## Notes

- CT image data (DICOM) is not included due to size and privacy.
- Clinical data CSV should be placed in the repository (`COVID_NY_SBU_clinical.csv`).
- Docker container provides environment reproducibility.

## Citation

Please cite your project if used in research or development. Inspired by methodologies such as Zhan & Li, Stanford University 2020.

## License

This project is intended for academic and research use only.
