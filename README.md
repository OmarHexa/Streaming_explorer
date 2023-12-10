# Byte by Byte ML

## Requirements
requirements.yml file contains the necessary packages to run the code in this repository. To install the packages, run the following command:
```
conda env create -f requirements.yml
```

requirements.yml is generated using the following command:
```
conda env export --no-builds | grep -v "prefix" > requirements.yml
```