import math # Library required to perform some more advanced functions.
import pandas as pd # Used data frames to clean up the output visually from the analysis calculator as its in tabular form.

def RentalCalc():
    while True:
        print("Rental Calculator\n" +
              "____________________________\n" +
              "Enter the number of the desired rental calculation.\n" +
              "____________________________\n")
        print("1. Rental Property Analysis (Known Price)\n2. Calculate Rental Property Offer (Known Cap Rate)")

        choice = input("1 or 2: ")  # Input prompt for user.

        if choice == "1":  # Following lines of code are just checking which type the user chose and calling the corresponding code.
            PropertyAnalysis()
        elif choice == "2":
            OfferCalc()
        else:
            print("Please enter a valid option (1 or 2).\n")
            continue  # Restart the loop if the input is invalid

        # Ask user if they want to end the program or run another analysis
        while True:  # Loop until valid input is provided
            end_program = input("Do you want to end the program? (yes/no): ").lower()
            if end_program == "yes":
                print("Thank you for using the Rental Calculator!")
                return  # Exit the function, ending the program
            elif end_program == "no":
                break  # Exit the loop to continue with another analysis
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                continue  # Restart the loop if the input is invalid

        
def cmhcrate(downpercent): # This function is called for both analysis and offer calculators and returns the cmhc insurance premium ratio based on loan to value ratio.
    if downpercent <0.05: # The followig lines of code are just evaluating against the downpayment ratio and returning the corresponding insurance premium rate.
        print('Downpayment Too Small For Conventional Mortgage')
        return
    elif downpercent <0.1:
        cmhc = 0.04
    elif downpercent<0.15:
        cmhc = 0.031
    elif downpercent < 0.2:
        cmhc = 0.028
    else:
        cmhc = 0
    return cmhc


def ippcalc(rate, loantype): # Returns the monthly interst rate based on the apr rate and type of loan.
    if loantype==1: # If else statement checking what type as fixed and variable loands compound differently, type 1 is fixed, type 2 is variable.
        return pow(rate/200+1,1/6)-1
    else:
        return rate/1200

    
def mortgagecalc(down, price, rate, amor, loantype): # This function returns the mortgage payment required for the property, amor is short for amoratization.
    ipp = ippcalc(rate, loantype) # Calling the ip function to determine the monthly interest rate.
    output = (((price-down)+cmhcrate(down/price))*ipp*pow(1+ipp,amor*12))/(pow(1+ipp,amor*12)-1) # Equation used to calculate a mortgage payment which includes CMHC preiums.
    return output    


def offerdenominator(downrate, transfertax, length, taxrate, ipp, cap): # Called multiple times within the offer calculator, returns the denominator of the equation used to calculate the offer.
        output = cap/1200*(downrate + transfertax/100) + (1+cmhcrate(downrate))*(1-downrate)*ipp*pow(1+ipp,length*12)/(pow(1+ipp,length*12)-1)+ taxrate/1200 # Basic math equation using most of the user inputs.
        return output
    
    
def PropertyAnalysis():
    try:  # Making sure all inputs are the correct type.
        price = float(input('Property Price ($):'))
        if price < 0:
            raise ValueError("Property price cannot be negative")
        rate = float(input('Interest Rate (%):'))
        if rate < 0:
            raise ValueError("Interest rate cannot be negative")
        loantype = int(input('Loan Type (Fixed = 1, Variable = 2):'))
        if loantype not in [1, 2]:
            raise ValueError("Loan type must be either 1 or 2")
        length = int(input('Amortization Length (Years):'))
        down = float(input('Down Payment ($):'))
        if down < 0:
            raise ValueError("Down payment cannot be negative")
        income = float(input('Expected Monthly Income ($):'))
        if income < 0:
            raise ValueError("Monthly income cannot be negative")
        RVpercent = float(input('Repairs and Vacancies (%):'))
        if RVpercent < 0:
            raise ValueError("Repairs and Vacancies percentage cannot be negative")
        taxrate = float(input('Property Tax Rate (%):'))
        if taxrate < 0:
            raise ValueError("Property tax rate cannot be negative")
        utilities = float(input('Monthly Utilities Expense ($):'))
        if utilities < 0:
            raise ValueError("Monthly utilities expense cannot be negative")
        insurance = float(input('Monthly Insurance Expense ($):'))
        if insurance < 0:
            raise ValueError("Monthly insurance expense cannot be negative")
        transfertax = float(input('Land Transfer Tax (%):'))
        if transfertax < 0:
            raise ValueError("Land transfer tax cannot be negative")
        legal = float(input('Expected Legal Fees ($):'))
        if legal < 0:
            raise ValueError("Legal fees cannot be negative")
    
        totalcost = down + legal + transfertax * price / 100  # Calculating and storing total investment required by user.
        mortgage = mortgagecalc(down, price, rate, length, loantype)  # Calling the mortgage function and storing the value.
        cmhc = (price - down) * cmhcrate(down / price)  # Calculating total cost of using CMHC insurance and storing it.
        expenses = mortgage + income * RVpercent / 100 + insurance + utilities + taxrate / 100 * price / 12  # Summing all monthly expenses and storing the value.
        net = income - expenses  # Calculating monthly net.
        cap = net * 12 / totalcost * 100  # Calculating cap rate - annual.
    
        # Printing the results.
        print("Monthly Net Income: $%.2f\n" % net +
              "Cap Rate: %.2f" % cap + "%\n" +
              "Monthly Expenses: $%.2f\n" % expenses +
              "Mortgage Payment: $%.2f\n" % mortgage +
              "Investment: $%.2f\n\n" % totalcost)
    
        print('Monthly Projection')
        print('_________________________________________________')
    
        # This section is the monthly breakdown which returns a handful of useful values in tabular form.
        monthly = [[a + 1, 0, 0, 0, 0, 0] for a in range(length * 12)]  # List creation for storage and conversion to df.
        balance = price - down + cmhc  # Initial balance of loan including mortgage insurance.
        equity = down  # Initial equity in property.
        ipp = ippcalc(rate, loantype)  # Storing monthly interest rate value to find the interest on each payment.
    
        for i in range(len(monthly)):  # Loops through every month for the length of the loan calculating the different values.
            monthly[i][1] = round(net * (i + 1), 2)  # Total net.
            monthly[i][2] = round(mortgage - (ipp * balance), 2)  # Principal.
            monthly[i][3] = round(ipp * balance, 2)  # Interest.
            balance = balance - (mortgage - (ipp * balance))  # Recalculating the balance after making a payment.
            monthly[i][4] = round(balance, 2)  # Balance.
            equity = equity + mortgage - (ipp * balance)  # Recalculating the equity after making a payment.
            monthly[i][5] = round(equity, 2)  # Equity.
    
        monthlydf = pd.DataFrame(monthly,
                                 columns=['Month', 'Net Total Return', 'Principle', 'Interest', 'Loan Balance',
                                          'Equity'])  # Converting the list to a data frame.
        pd.set_option("display.max_rows", None, "display.max_columns",
                      None)  # Makes it so we can see the whole data frame and not just the first 5 and last 5 rows.
        print(monthlydf)  # Outputs it.
    except ValueError as e:  # Error handling, if there is a value error it will re-ask for user inputs.
        print(e)
        print("Please enter valid numeric values.")

# Completion of the Property Analysis.

    
def OfferCalc(): # Second calculator included in the program, takes all the known cash flow and desired cap rate as well as financing info to produce an offer that would return the desired cap rate.
    try:
        cap = float(input('Desired Cap Rate (%):')) # Next few rows are prompts for inputs from the user.
        if cap < 0:
            raise ValueError("Capitalization rate cannot be negative")
        rate = float(input('Interest Rate (%):'))
        if rate < 0:
            raise ValueError("Interest rate cannot be negative")
        loantype = int(input('Loan Type (Fixed = 1, Variable = 2):'))
        if loantype not in [1, 2]:
            raise ValueError("Loan type must be either 1 or 2")
        length = int(input('Ammortization Length (Years):'))
        if length < 0:
            raise ValueError("Ammortization length cannot be negative")
        income = float(input('Expected Monthly Income ($):'))
        if income < 0:
            raise ValueError("Excepected income cannot be negative")
        RVpercent = float(input('Repairs and Vacancies (%):'))
        if RVpercent < 0:
            raise ValueError("Repairs and Vacancies percentage cannot be negative")
        taxrate = float(input('Property Tax Rate (%):'))
        if taxrate < 0:
            raise ValueError("Property tax rate cannot be negative")
        utilities = float(input('Monthly Utilities Expense ($):'))
        if utilities < 0:
            raise ValueError("Monthly utilities expense cannot be negative")
        insurance = float(input('Monthly Insurance Expense ($):'))
        if insurance < 0:
            raise ValueError("Monthly insurance expense cannot be negative")
        transfertax = float(input('Land Transfer Tax (%):'))
        if transfertax < 0:
            raise ValueError("Land transfer tax cannot be negative")
        legal = float(input('Expected Legal Fees ($):'))
        if legal < 0:
            raise ValueError("Legal fees cannot be negative")
        ipp = ippcalc(rate, loantype) # Storing the monthly interest rate based on user input.
        downamount = float(0.05) # Initlization of the lowest downpayment required.
        top = income - ipp*pow(1+ipp,length*12)/(pow(1+ipp,length*12)-1)*cmhcrate(downamount) - income*RVpercent/100 - insurance - utilities - legal*cap/1200 # Numerator of the initial offer.
        bottom = offerdenominator(0.05, transfertax, length, taxrate, ipp, cap) # Denominator of the initial offer via the denomiator function.
        offer = top/bottom # Equation used to derrive the initial offer to evaluate.
        twentybottom =offerdenominator(0.2, transfertax, length, taxrate, ipp, cap) # Same calculation as above but using 20% which will abide by all laws.
        twentytop = income - ipp*pow(1+ipp,length*12)/(pow(1+ipp,length*12)-1)*cmhcrate(0.2) - income*RVpercent/100 - insurance - utilities - legal*cap/1200
        twentydown = twentytop/twentybottom # Same calculation as above just using 20% instead of a smaller downpayment.
        
        
        if offer <= 500000: # Following if else statements are checking which loan to value the mortgage falls under.
            mindown = offer # Initial calculated offer abides by all rules and can be used.
            print("Using a CMHC loan with a minimum downpayment of  %.2f"%(downamount*100)+"% yields:\n") # Minimum downpayment will be used at 5%.
            print("Offer: %.2f \n" %mindown) # Outputing the calculated offer using the min down percent.
            print("Total Investment: $%.2f \n" %(downamount*mindown + legal + offer*transfertax/100)) # Total amount invested.
            print("Rental property mortgage requiring a 20% downpayment yields:\n") # Ouput visual for 20% down.
            print("Offer: $%.2f \n" %twentydown) # Offer to make at 20% down.
            print("Total Investment: $%.2f" %(0.2*twentydown + legal + offer*transfertax/100)) # Total investment.
        elif offer <= 1000000: # Checking if it sits between 500k and 1mil, if so the initial offer wont abide by all mortgage laws but a close offer can be found using a hgher downpayment.
            while downamount < 0.1: # Starting at 5% down, recalculate a new offer and if it doesnt pass the check increase the downpayment size and loop again.
                temptop = income - ipp*pow(1+ipp,length*12)/(pow(1+ipp,length*12)-1)*cmhcrate(downamount) - income*RVpercent/100 - insurance - utilities - legal*cap/1200
                tempbottom = offerdenominator(downamount, transfertax, length, taxrate, ipp, cap) # Calculate a new denominator with current down payment size.
                newoffer = temptop/tempbottom # New offer.
                if round((newoffer*downamount-25000)/(newoffer-500000),3) == 0.10: # Checks to see if the new offer abides by the CMHC requirments.
                    print("Using a CMHC loan with a minimum downpayment of %.2f"%(downamount*100)+"% yields:\n") # If a pass, output the accepted offer values.
                    print("Offer: $%.2f \n" %newoffer)
                    print("Total Investment: $%.2f \n" %(downamount*newoffer + legal + newoffer*transfertax/100))
                    print("Rental property mortgage requiring a 20% downpayment yields:\n")
                    print("Offer: $%.2f \n" %twentydown)
                    print("Total Investment: $%.2f" %(0.2*twentydown + legal + twentydown*transfertax/100))
                    downamount = 1 # End loop.
                else:
                    downamount = float(downamount + 0.00001) # If it fails to pass the check, increase downpayment and loop again.
        else: # Of the offer is above 1 million a 20% downpayment is required.
            downamount = 0.2 # Set down amount to 20%.
            offer = twentydown # Lowest down offer is twenty percent.
            print("Rental property mortgage requiring a minimum 20% downpayment yields:\n") # Output the 20% down values.
            print("Offer: $%.2f \n" %twentydown)
            print("Total Investment: $%.2f" %(0.2*twentydown + legal + offer*transfertax/100))
    except ValueError as e:
        print(e)
        print("Please enter valid numeric values.")
# Completion of the Offer Calculator.

RentalCalc()





