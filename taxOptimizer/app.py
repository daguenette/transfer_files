import user_class.user as u
import app.core.personalFinance as pf


## -------------------------- Table 1 --------------------------

# Create User
user1 = u.User('Camille', 1, 132000.00, 0.11, 3)

# Log user data into database (User Info)
user_data = user1.get_user_data()

print(user_data)

basic_information = pf.PersonalFinance(user_data)

# print(basic_information.personal_finance_table)



## -------------------------- Table 2 --------------------------
