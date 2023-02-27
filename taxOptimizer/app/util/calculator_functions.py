## Packages
import app.util.reader_functions as reader_functions

## General Calculators

def calculate_annual_net_income(gross_annual_income: float, annual_tax_income: float) -> float:

    annuel_net_income = gross_annual_income - annual_tax_income

    return annuel_net_income

def calculate_monthly_net_income(annuel_net_income: float) -> float:

    monthly_net_income = annuel_net_income / 12

    return monthly_net_income


def calcualte_average_tax_rate(gross_annual_income: float, annual_tax_income: float) -> float:

    average_tax_rate = annual_tax_income / gross_annual_income * 100

    return average_tax_rate


## Provincial & Federal Plan Calculators

def calculate_qpp(gross_annual_income: float, rrsp_contribution: float) -> float:

    deducted_annuel_income = gross_annual_income - rrsp_contribution

    brackets = reader_functions.qpp_data['brackets'].to_numpy()
    contribution = reader_functions.qpp_data['contributions'].to_numpy()

    for i in range(len(brackets) -1):
        if deducted_annuel_income <= brackets[i]:
            return contribution[i]

    return contribution[-1]


    pass

def calculate_qpip(gross_annual_income: float, rrsp_contribution: float) -> float:
    
    deducted_annuel_income = gross_annual_income - rrsp_contribution

    rate = reader_functions.qpip_data['rate'].to_numpy()[0]
    maximum = reader_functions.qpip_data['maximum'].to_numpy()[0]

    qpip = deducted_annuel_income * rate

    if qpip >= maximum:
        return maximum
    else:
        return qpip

def calculate_ie(gross_annual_income: float, rrsp_contribution: float) -> float:

    deducted_annuel_income = gross_annual_income - rrsp_contribution

    rate = reader_functions.ei_preniums_data['rate'].to_numpy()[0]
    maximum = reader_functions.ei_preniums_data['maximum'].to_numpy()[0]

    if deducted_annuel_income <= maximum:
        return deducted_annuel_income / 100 * rate
    else:
        return maximum /100 * rate


## Provincial & Federal Tax Calculators

def calculate_provincial_tax_bracket(gross_annual_income: float, rrsp_contribution: float) -> float:

    deducted_annuel_income = gross_annual_income - rrsp_contribution

    # TODO change qc_tax_data to provincial_tax_data
    brackets = reader_functions.qc_tax_data['brackets'].to_numpy()
    rates = reader_functions.qc_tax_data['rates'].to_numpy()

    if deducted_annuel_income <= brackets[0]:
        return deducted_annuel_income
    elif deducted_annuel_income <= brackets[1]:
        return (brackets[1]) * rates[0]
    elif deducted_annuel_income <= brackets[2]:
        return (brackets[1]) * rates[0] + (deducted_annuel_income - brackets[1]) * rates[1]
    elif deducted_annuel_income <= brackets[3]:
        return (brackets[1]) * rates[0] + (brackets[2] - brackets[1]) * rates[1] + (deducted_annuel_income - brackets[2]) * rates[2]
    else:
        return (brackets[1]) * rates[0] + (brackets[2] - brackets[1]) * rates[1] + (brackets[3] - brackets[2]) * rates[2] + (deducted_annuel_income - brackets[3]) * rates[3]

def calculate_federal_tax_bracket(gross_annual_income: float, rrsp_contribution: float) -> float:

    deducted_annuel_income = gross_annual_income - rrsp_contribution

    # TODO change canada_tax_data to provincial_tax_data
    brackets = reader_functions.canada_tax_data['brackets'].to_numpy()
    rates = reader_functions.canada_tax_data['rates'].to_numpy()

    if deducted_annuel_income <= brackets[0]:
        return deducted_annuel_income
    elif deducted_annuel_income <= brackets[1]:
        return (brackets[1]) * rates[0]
    elif deducted_annuel_income <= brackets[2]:
        return (brackets[1]) * rates[0] + (deducted_annuel_income - brackets[1]) * rates[1]
    elif deducted_annuel_income <= brackets[3]:
        return (brackets[1]) * rates[0] + (brackets[2] - brackets[1]) * rates[1] + (deducted_annuel_income - brackets[2]) * rates[2]
    elif deducted_annuel_income <= brackets[4]:
        return (brackets[1]) * rates[0] + (brackets[2] - brackets[1]) * rates[1] + (brackets[3] - brackets[2]) * rates[2]  + (deducted_annuel_income - brackets[3]) * rates[3]
    else:
        return (brackets[1]) * rates[0] + (brackets[2] - brackets[1]) * rates[1] + (brackets[3] - brackets[2]) * rates[2] + (brackets[4] - brackets[3]) * rates[3]  + (deducted_annuel_income - brackets[4]) * rates[4]

def calculate_provincial_tax(gross_annual_income: float, rrsp_contribution: float) -> float:

    ## - 1 Calculate Provincial Tax Bracket
    provincial_tax = calculate_provincial_tax_bracket(gross_annual_income, rrsp_contribution)

    ## - 2 Provincial Tax Credit (BPA / QPP Base contributions / EI Preniums / QPIP)
    bpa = reader_functions.bpa_data['qc'].to_numpy()[0]
    qpp = 3776.10 # calculate_qpp(income) test for 2022
    qpip = calculate_qpip(gross_annual_income, rrsp_contribution)
    ei_preniums = calculate_ie(gross_annual_income, rrsp_contribution)

    provincial_tax_credit = bpa + qpp + ei_preniums + qpip
    
    ## - 3 Mutiply Federal Tax Credit By Lowest Federal Tax Rate
    provincial_tax_credit *= 0.15

    provincial_tax -= provincial_tax_credit

    ## - 4 Total Federal Tax Payable For The Year
    return round(float(provincial_tax)) 

def calculate_federal_tax(gross_annual_income: float, rrsp_contribution: float) -> float:
    
    ## - 2 Calculate federal tax
    federal_tax = calculate_federal_tax_bracket(gross_annual_income, rrsp_contribution)

    ## - 3 Federal Tax Credit (BPA / QPP Base contributions / EI Preniums / QPIP / CAE)
    bpa = reader_functions.bpa_data['canada'].to_numpy()[0]
    qpp = 3776.10 # calculate_qpp(income) test for 2022
    qpip = calculate_qpip(gross_annual_income, rrsp_contribution)
    ei_preniums = calculate_ie(gross_annual_income, rrsp_contribution)
    cae = 1368.00

    federal_tax_credit = bpa + qpp + ei_preniums + qpip + cae

    ## - 4 Mutiply Federal Tax Credit By Lowest Federal Tax Rate TODO remove hardcoded value
    federal_tax_credit *= 0.15

    ## - 5 Federal Tax Minus Federal Tax Credit
    federal_tax -= federal_tax_credit

    ## - 6 Find Abatement TODO Remove hardcoded value
    abatement = federal_tax * 0.165

    ## - 7 Total
    federal_tax -= abatement

    ## - 8 Return Total Federal Tax Payable For The Year
    return round(float(federal_tax))
    
def calculate_contributions(gross_annual_income: float, rrsp_contribution: float) -> float:

    ## - 2 Calculate contributions
    qpp =  3776.10 # calculate_qpp(income) test for 2022
    ei_preniums = calculate_ie(gross_annual_income, rrsp_contribution)
    qpip = calculate_qpip(gross_annual_income, rrsp_contribution)

    ## - 3 Add All Contributions
    contributions = qpp + ei_preniums + qpip

    ## - 4 Return Total
    return round(float(contributions))

def calculate_annual_income_tax(gross_annual_income: float, rrsp_contribution: float) -> float:

    provincial_tax = calculate_provincial_tax(gross_annual_income, rrsp_contribution)

    federal_tax = calculate_federal_tax(gross_annual_income, rrsp_contribution)

    contributions = calculate_contributions(gross_annual_income, rrsp_contribution)

    annual_income_tax = provincial_tax + federal_tax + contributions

    return annual_income_tax

