import calculator_class.allocationCalculator as ac
import pandas as pd



def grouby_two_sum(colname1, colname2, df):

    df = df.groupby([colname1, colname2]).sum()

    return df


def drop_two_columns(colname1, colname2, df):

    df = df.drop([colname1, colname2], axis=1)
    df = df.reset_index()

    return df


def get_qc_allocations(net_income_col, df):

    net_income_ls = df[net_income_col].to_numpy()
    children_ls = df['children'].to_numpy()

    yearly_allocation = []
    monthly_allocation = []

    for i in range(len(net_income_ls)):
        yearly_allocation.append(ac.calculate_allocation_qc(net_income_ls[i], children_ls[i]))
        monthly_allocation.append(ac.calculate_allocation_qc(net_income_ls[i], children_ls[i]) / 12)

    dict = {

        'yearly_allocation': yearly_allocation,
        'monthly_allocation': monthly_allocation

    }

    return dict


def add_allocations_to_df(array, df, new_col_name):

    df[new_col_name] = array

    return df

