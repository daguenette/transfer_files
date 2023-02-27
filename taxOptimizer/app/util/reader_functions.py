"""
Tax Data

This file can be imported as a module and contains the following
Dataframes:

    * qc_tax_data - Dataframe representing the brackets & rates for quebec income tax.
    * fed_tax_data - Dataframe representing the brackets & rates for canada income tax.
    * qpp_data - Dataframe representing the brackets & contributions for the quebec pension plan (qpp).
    * qpip_data - Dataframe representing the rate & maximum for the quebec parental insurance plan (qpip).
    * ei_preniums_data - Dataframe representing the rate & maximum for the employment insurance preniums (ei preniums).
    * bpa_data - Dataframe representing the canada & quebec basic personal amount (bpa)
    * wealthsimple_data - Dataframe representing testing scenarios from wealthsimple to compare our calculator.

"""

import pandas as pd

## Quebec Tax Brackets & Rates
qc_tax_data = pd.read_csv('app/util/data/tax_calculator_data_quebec_tax.csv')

## Canada Tax Brackets & Rates
canada_tax_data = pd.read_csv('app/util/data/tax_calculator_data_canada_tax.csv')

## QPP Brackets & Contributions
qpp_data = pd.read_csv('app/util/data/tax_calculator_data_qpp.csv')

## QPIP Rate & Maximum
qpip_data = pd.read_csv('app/util/data/tax_calculator_data_qpip.csv')

## EI Preniums Rates & Maximum
ei_preniums_data = pd.read_csv('app/util/data/tax_calculator_data_ei_preniums.csv')

## BPA
bpa_data = pd.read_csv('app/util/data/tax_calculator_data_bpa.csv')

## Allocation QC
allocation_qc_data = pd.read_csv('app/util/data/tax_calculator_data_allocation_qc.csv')

## Allocation Canada
allocation_canada_data = pd.read_csv('app/util/data/tax_calculator_data_allocation_canada.csv')

## Wealthsimple Data -
wealthsimple_data = pd.read_csv('app/util/data/tax_calculator_data_wealthsimple.csv')
