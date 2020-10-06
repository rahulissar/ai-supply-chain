# AI-Supply-Chain

Repository for common AI use cases in supply chain, procurement

v 1.0 - Added project to normalize legal entity names of vendors/suppliers. You can utilize your spend data or simply choose a custom vendor dataset to perform legal name normalization.

## Requirements

fuzzywuzzy library (For fuzzy matching of string) - https://pypi.org/project/fuzzywuzzy/
levenshtein library (For faster computation of Levenshtein Distance) - https://pypi.org/project/python-Levenshtein/

## Datasets

a) Goverment of California's 2012-2015 Purchase Orders - https://data.ca.gov/dataset/purchase-order-data/resource/bb82edc5-9c78-44e2-8947-68ece26197c5

b) Custom dataset - Refer sample vendor_data.csv available

All input to the program requires data as per format prescribed in above two links. Additionally, you can customize the settings.py file to accomodate data in your own format.
