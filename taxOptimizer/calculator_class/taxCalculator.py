"""
Tax Calculator Class

This file can be imported as a module and contains the following
class:

    TaxCalculator - represent a Tax Calculator
"""


import app.util.reader_functions as reader_functions

class TaxCalculator:
    """
    A classs to represent a Tax Calculator
    
    Attributes
    ----------

    income : float
        gross annual income of the user
    rrsp_contribution : float
        annual contribution to rrsp 

    
    Methods
    -------
    calculate_tax_qc(income) : float
        returns the basic quebec income tax

    calculate_tax_fed(income) : float
        returns the basic federal income tax

    calculate_qpp(income) : float
        return the contribution for the Quebec Pension Plan (QPP)

    calculate_qpip(income) : float
        return the contribution for the Quebec Parental Insurance Plan (QPIP)

    calculate_ie(income) : float
        return the contribution for the Employment Insurances Preniums (EI Preniums)

    calculate_annual_tax_income(): float
        return the gross annuel income minus the rrsp contribution

    calculate_full_canada_tax(): float
        return the comple Canada Income Tax (w/t deductions & abatement)

    calculate_full_quebec_tax(): float
        return the complete Quebec Income Tax (w/t deductions)

    calculate_total_contribution(): float
        return the total of all contributions (QPP, QPIP, EI Preniums) to pay for the year.
    """

    def __init__(self, income=0.00, rrsp_contribution=0.00):

        self.income = income
        self.rrsp_contribution = rrsp_contribution

    def calculate_tax_qc(self, income) -> float:
        """
        Calculate the basic quebec income tax.

        Parameters
        ----------
        income : float
            gross annual income
        
        Returns
        -------
        float
            returns the basic quebec income tax
        """

        brackets = reader_functions.qc_tax_data['brackets'].to_numpy()
        rates = reader_functions.qc_tax_data['rates'].to_numpy()

        if income <= brackets[0]:
            return income
        elif income <= brackets[1]:
            return (brackets[1]) * rates[0]
        elif income <= brackets[2]:
            return (brackets[1]) * rates[0] + (income - brackets[1]) * rates[1]
        elif income <= brackets[3]:
            return (brackets[1]) * rates[0] + (brackets[2] - brackets[1]) * rates[1] + (income - brackets[2]) * rates[2]
        else:
            return (brackets[1]) * rates[0] + (brackets[2] - brackets[1]) * rates[1] + (brackets[3] - brackets[2]) * rates[2] + (income - brackets[3]) * rates[3]

    def calculate_tax_canada(self, income) -> float:
        """
        Calculate the basic canada income tax.

        Parameters
        ----------
        income : float
            gross annual income
        
        Returns
        -------
        float
            returns the basic federal income tax
        """

        brackets = reader_functions.canada_tax_data['brackets'].to_numpy()
        rates = reader_functions.canada_tax_data['rates'].to_numpy()

        if income <= brackets[0]:
            return income
        elif income <= brackets[1]:
            return (brackets[1]) * rates[0]
        elif income <= brackets[2]:
            return (brackets[1]) * rates[0] + (income - brackets[1]) * rates[1]
        elif income <= brackets[3]:
            return (brackets[1]) * rates[0] + (brackets[2] - brackets[1]) * rates[1] + (income - brackets[2]) * rates[2]
        elif income <= brackets[4]:
            return (brackets[1]) * rates[0] + (brackets[2] - brackets[1]) * rates[1] + (brackets[3] - brackets[2]) * rates[2]  + (income - brackets[3]) * rates[3]
        else:
            return (brackets[1]) * rates[0] + (brackets[2] - brackets[1]) * rates[1] + (brackets[3] - brackets[2]) * rates[2] + (brackets[4] - brackets[3]) * rates[3]  + (income - brackets[4]) * rates[4]

    def calculate_qpp(self, income) -> float:
        """
        Calculate the contribution for the Quebec Pension Plan (QPP).

        Parameters
        ----------
        income : float
            gross annual income
        
        Returns
        -------
        float
            returns the contribution for the Quebec Pension Plan (QPP)
        """

        brackets = reader_functions.qpp_data['brackets'].to_numpy()
        contribution = reader_functions.qpp_data['contributions'].to_numpy()

        for i in range(len(brackets) -1):
            if income <= brackets[i]:
                return contribution[i]

        return contribution[-1]

    def calculate_qpip(self, income) -> float:
        """
        Calculate the contribution for the Quebec Parental Insurance Plan (QPIP)

        Parameters
        ----------
        income : float
            gross annual income
        
        Returns
        -------
        float
            returns the contribution for the Quebec Parental Insurance Plan (QPIP)
        """

        rate = reader_functions.qpip_data['rate'].to_numpy()[0]
        maximum = reader_functions.qpip_data['maximum'].to_numpy()[0]

        qpip = income * rate

        if qpip >= maximum:
            return maximum
        else:
            return qpip

    def calculate_ie(self, income) -> float:
        """
        Calculate the contribution for the Employment Insurances Preniums (EI Preniums)

        Parameters
        ----------
        income : float
            gross annual income
        
        Returns
        -------
        float
            returns the contribution for the Employment Insurances Preniums (EI Preniums)
        """

        rate = reader_functions.ei_preniums_data['rate'].to_numpy()[0]
        maximum = reader_functions.ei_preniums_data['maximum'].to_numpy()[0]

        if income <= maximum:
            return income / 100 * rate
        else:
            return maximum /100 * rate

    def calculate_annual_tax_income(self) -> float:
        """
        Calculate the gross annuel income minus the rrsp contribution

        Parameters
        ----------
        None
        
        Returns
        -------
        float
            returns the gross annuel income minus the rrsp contribution
        """

        return self.income - self.rrsp_contribution

    def calculate_full_canada_tax(self) -> float:
        """
        Calculate the comple Canada Income Tax (w/t deductions & abatement)

        Parameters
        ----------
        None
        
        Returns
        -------
        float
            returns the comple Canada Income Tax (w/t deductions & abatement)
        """


        ## - 1 Calculate annual income
        income = self.calculate_annual_tax_income()

        ## - 2 Calculate federal tax
        federal_tax = self.calculate_tax_canada(income)

        ## - 3 Federal Tax Credit (BPA / QPP Base contributions / EI Preniums / QPIP / CAE)
        bpa = reader_functions.bpa_data['canada'].to_numpy()[0]
        qpp = 3776.10 # calculate_qpp(income) test for 2022
        ei_preniums = self.calculate_ie(income)
        qpip = self.calculate_qpip(income)
        cae = 1368.00
        federal_tax_credit = bpa + qpp + ei_preniums + qpip + cae

        ## - 4 Mutiply Federal Tax Credit By Lowest Federal Tax Rate
        federal_tax_credit = federal_tax_credit * 0.15

        ## - 5 Federal Tax Minus Federal Tax Credit
        sub_total = federal_tax - federal_tax_credit

        ## - 6 Find Abatement
        abatement = sub_total * 0.165

        ## - 7 Total
        total = sub_total - abatement

        ## - 8 Return Total Federal Tax Payable For The Year
        return round(float(total))

    def calculate_full_quebec_tax(self) -> float:
        """
        Calculate the complete Quebec Income Tax (w/t deductions)

        Parameters
        ----------
        None
        
        Returns
        -------
        float
            returns the complete Quebec Income Tax (w/t deductions)
        """

        ## - 1 Calculate Annual Income
        income = self.calculate_annual_tax_income()

        ## - 2 Calculate Quebec Tax
        quebec_tax = self.calculate_tax_qc(income)

        ## - 3 Provincial Tax Credit (BPA / QPP Base contributions / EI Preniums / QPIP)
        bpa = reader_functions.bpa_data['qc'].to_numpy()[0]
        qpp = 3776.10 # calculate_qpp(income) test for 2022
        ei_preniums = self.calculate_ie(income)
        qpip = self.calculate_qpip(income)
        provincial_tax_credit = bpa + qpp + ei_preniums + qpip
        
        ## - 4 Mutiply Federal Tax Credit By Lowest Federal Tax Rate
        provincial_tax_credit = provincial_tax_credit * 0.15
        total = quebec_tax - provincial_tax_credit

        ## - 5 Total Federal Tax Payable For The Year
        return round(float(total))

    def calculate_total_contribution(self) -> float:
        """
        Calculate the total of all contributions (QPP, QPIP, EI Preniums) to pay for the year.

        Parameters
        ----------
        None
        
        Returns
        -------
        float
            returns the total of all contributions (QPP, QPIP, EI Preniums) to pay for the year.
        """


        ## - 1 Calculate annual income
        income = self.calculate_annual_tax_income()

        ## - 2 Calculate contributions
        qpp =  3776.10 # calculate_qpp(income) test for 2022
        ei_preniums = self.calculate_ie(income)
        qpip = self.calculate_qpip(income)

        ## - 3 Add All Contributions
        total = qpp + ei_preniums + qpip

        ## - 4 Return Total
        return round(float(total))

    def calculate_income_tax(self) -> float:

        qc = self.calculate_full_quebec_tax()

        canada = self.calculate_full_canada_tax()

        contribution = self.calculate_total_contribution()

        income_tax = qc + canada + contribution

        return income_tax



    


