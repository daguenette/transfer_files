import calculator_class.taxCalculator  as tc
import pandas as pd

class User:

    def __init__(self, name, family_id, annual_gross_income, rrsp_contribution, children) -> None:

        self.name = name
        self.family_id = family_id
        self.annual_gross_income = annual_gross_income
        self.custom_contribution = annual_gross_income * rrsp_contribution
        # self.max_contribution = 29210.00 # TODO change hard coded value
        self.children = children

        pass

    def get_user_data(self):

        user_data = {

            'name': self.name,
            'family_id': self.family_id,
            'annual_gross_income': self.annual_gross_income,
            'custom_contribution': self.custom_contribution,
            'children': self.children
        }

        return user_data





