from dateutil.relativedelta import relativedelta
import numpy_financial as npf
import pandas as pd

class MortageCalculator:
    """
    A classs to represent a Mortage Calculator
    
    Attributes
    ----------

    var : type
        descp

    
    Methods
    -------
    function_name(param) : type
        return descr
    """

    def __init__(self, payment_due_date: object, rate: float, loan_amount: float, term_year: int) -> None:
        self.payment_due_date = payment_due_date
        self.rate = rate
        self.loan_amount = loan_amount
        self.term_year = term_year
        pass

    def calculate_first_ls(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """

        monthly_payment = self.calculate_monthly_payment()
        interest = self.loan_amount * self.calculate_rate()
        
        principal = monthly_payment - interest
        end_balance = self.loan_amount - principal # TODO add extra payment

        dict = {
            
            'payment_due_date': [self.payment_due_date],
            'month_nbr': [1],
            'begin_balance': [round(self.loan_amount, 2)],
            'payment': [monthly_payment],
            'interest': [round(interest, 2)],
            'principal': [round(principal, 2)],
            'end_balance': [round(end_balance, 2)],
            'total_interest': [round(interest, 2)],
            'total_principal': [round(principal, 2)],
            'remaining_interest': [0]

        }

        return dict

    def calculate_rate(self) -> float:
        """_summary_

        Returns:
            float: _description_
        """

        rate = (self.rate / 2.0 + 1.0) ** (1.0 / 6.0) - 1.0
        return rate

    def calculate_term_month(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """

        term_month = self.term_year * 12

        return term_month

    def calculate_monthly_payment(self) -> float:
        """_summary_

        Returns:
            float: _description_
        """

        rate = self.calculate_rate()

        term_month = self.calculate_term_month()

        monthly_payment = round(-npf.pmt(rate, term_month, self.loan_amount), 2)

        return monthly_payment

    def calculate_payment_schedule(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """

        dict = self.calculate_first_ls()
        rate = self.calculate_rate()
        term_month = self.calculate_term_month()
        monthly_payment = self.calculate_monthly_payment()

        for i in range(term_month - 1):
            dict['payment_due_date'].append(dict['payment_due_date'][i] + relativedelta(months=1))
            dict['month_nbr'].append(dict['month_nbr'][i] + 1)
            dict['begin_balance'].append(round(dict['end_balance'][i], 2))
            dict['payment'].append(monthly_payment)
            dict['interest'].append(round(dict['end_balance'][i] * rate, 2))
            dict['principal'].append(round(monthly_payment - dict['interest'][i + 1], 2))
            dict['end_balance'].append(round(dict['end_balance'][i] - dict['principal'][i + 1], 2))
            dict['total_interest'].append(round(dict['total_interest'][i] + dict['interest'][i + 1], 2))
            dict['total_principal'].append(round(dict['total_principal'][i] + dict['principal'][i + 1], 2))

        dict['remaining_interest'][0] = dict['total_interest'][-1] - dict['total_interest'][0]

        for i in range(term_month - 1):
             dict['remaining_interest'].append(dict['total_interest'][-1] - dict['total_interest'][i + 1])

        return dict

    def get_mortage_dataframe(self) -> object:
        """_summary_

        Returns:
            object: _description_
        """

        print(type(self.payment_due_date))

        dict = self.calculate_payment_schedule()

        df = pd.DataFrame.from_dict(dict)
        return df
