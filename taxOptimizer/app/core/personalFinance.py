## Personal Finance Table

import pandas as pd

class PersonalFinance:

    def __init__(self, table: dict) -> None:
        self._personal_finance_table = pd.DataFrame.from_dict(table).set_index('name')

    @property
    def personal_finance_table(self):
        return self._personal_finance_table


    @personal_finance_table.setter
    def set_personal_finance_table(self, table: dict):
        self._personal_finance_table = pd.DataFrame(table)






    # def get_personal_finance_information(self) -> object:
 
    #     ### INCOME TAX ###

    #     # Custom RRSP
    #     custom_income_tax = self.get_tax_income(self.custom_contribution)

    #     # No RRSP
    #     no_income_tax = self.get_tax_income(self.no_contribution)

    #     # Max RRSP
    #     max_income_tax = self.get_tax_income(self.max_contribution)

    #     ### NET INCOME ###

    #     # Custom RRSP
    #     custom_net_income = self.get_net_income(custom_income_tax)

    #     # No RRSP
    #     no_net_income = self.get_net_income(no_income_tax)

    #     # Max RRSP
    #     max_net_income = self.get_net_income(max_income_tax)

    #     ### MONTHLY NET INCOME ###

    #     # Custom RRSP
    #     custom_monthly_income = self.get_monthly_income(custom_net_income)

    #     # No RRSP
    #     no_monthly_income = self.get_monthly_income(no_net_income)

    #     # Max RRSP
    #     max_monthly_income = self.get_monthly_income(max_net_income)

    #     ### TAX SAVING ###

    #     # Custom RRSP
    #     custom_tax_saving = custom_net_income - no_net_income

    #     # Max RRSP
    #     max_tax_saving = max_net_income - no_net_income

    #     ### AVERAGE TAX RATE ###

    #     # Custom RRSP
    #     custom_avg_tax_rate = self.get_average_tax_rate(custom_income_tax)

    #     # Max RRSP
    #     max_avg_tax_rate = self.get_average_tax_rate(max_income_tax)

    #     table = {
    #         'name': [self.name],
    #         'family_id': [self.family_id],
    #         'children': [self.children],
    #         'total_income': [self.total_income],
    #         'custom_contribution': [self.custom_contribution],
    #         'max_contribution': [self.max_contribution],
    #         'income_tax_custom_contribution': [custom_income_tax],
    #         'income_tax_max_contribution': [max_income_tax],
    #         'income_tax_no_contribution': [no_income_tax],
    #         'net_income_custom_contribution': [custom_net_income],
    #         'net_income_max_contribution': [max_net_income],
    #         'net_income_no_contribution': [no_net_income],
    #         'monthly_income_custom_contribution': [custom_monthly_income],
    #         'monthly_income_max_contribution': [max_monthly_income],
    #         'monthly_no_contribution': [no_monthly_income],
    #         'tax_saving_custom_contribution': [custom_tax_saving],
    #         'tax_saving_max_contribution': [max_tax_saving],
    #         'avg_tax_rate_custom_contribution': [custom_avg_tax_rate],
    #         'avg_tax_rate_max_contribution': [max_avg_tax_rate]         
    #     }

    #     df = pd.DataFrame.from_dict(table)
    #     df = df.set_index('name')

    #     return df