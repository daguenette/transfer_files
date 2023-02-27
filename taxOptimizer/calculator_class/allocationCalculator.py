import app.util.reader_functions as reader_functions


def number_to_text_children(children: int) -> str:
    """Tranform given number of children to text.

    Args:
        children (int): Amount of children the user have.

    Returns:
        str: A string of the amount of children the user have.
    """
    
    if children == 1:
        children = 'one_children'
    elif children == 2:
        children = 'two_children'
    elif children == 3:
        children = 'three_children'
    elif children == 4:
        children = 'four_children'
    elif children == 5:
        children = 'five_children'
    else:
        children = 'five_children'

    return children

def calculate_allocation_qc(family_income: float, children: int) -> float:
    """Calculate the annual allocation for Quebec citizen with children

    Args:
        family_income (float): Annual family income of the family requesting an allocation.
        children (int): The amount of children the family have.

    Returns:
        float: Allocation for Quebec resident.
    """

    if children == 0:
        return 0
    else:
        children = number_to_text_children(children)

        brackets = reader_functions.allocation_qc_data['family_income'].to_numpy()
        allocation = reader_functions.allocation_qc_data[children].to_numpy()
        
        for i in range(len(brackets) -1):
            if family_income <= brackets[i]:
                return allocation[i]

        return allocation[-1]

def calculate_allocation_canada(family_income: float, children: int) -> float:
    """Calculate the annual allocation for Canadian citizen with children

    Args:
        family_income (float): Annual family income of the family requesting an allocation.
        children (int): The amount of children the family have.

    Returns:
        float: Allocation for Canadian resident.
    """

    allocation = 0
    minimum_allocation = reader_functions.allocation_canada_data['allocation'].to_numpy()[0]
    lower_bracket = reader_functions.allocation_canada_data['bracket'].to_numpy()[0]
    higher_braket = reader_functions.allocation_canada_data['bracket'].to_numpy()[1]
    lower_reduction_rate = reader_functions.allocation_canada_data['reduction_rate'].to_numpy()[0]
    higher_reduction_rate = reader_functions.allocation_canada_data['reduction_rate'].to_numpy()[1]
    additional_reduction = reader_functions.allocation_canada_data['additional_reduction'].to_numpy()[1]


    if family_income <= lower_bracket:
        allocation = minimum_allocation * children
    elif family_income <= higher_braket:
        over_limit = family_income - lower_bracket
        reduction = over_limit * lower_reduction_rate
        allocation = (minimum_allocation - reduction) * children
    else: 
        over_limit = family_income - higher_braket
        reduction = over_limit * higher_reduction_rate + additional_reduction
        allocation = (minimum_allocation - reduction) * children     

    return allocation
