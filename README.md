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


## Pre-Commit hooks
Install pre-commit for static code checking of all files before a new commit.
```
pip install pre-commit
``` 
To initiate pre-commit hooks to any git repistory do..
```
pre-commit install
```
Now pre-commit will run automatically on every git commit and commit will only happens when all the check are passed. Check .per-commit-config.yaml file to see more on the type of all static code check for furthure details. 

