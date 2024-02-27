# Rental Property Analyzer

# Description 
The Rental Property Analyzer is a Python program designed to be used before investing in real estate. The program offers two options to the user, either a Rental Property Analysis or an Offer Calculator. The Rental Property Analysis is used to determine the capitalization rate, inital investment, and monthly cash flow. Pandas data frames are used to display a monthly projection for the ammortization term. The Offer Calculator is used to determine an offer price based on a targeted capitalization rate and known expenses. The program is operated from the command line.

# Prerequisites
* Python 3.12
* Pandas 2.1.3 (`pip install pandas` in your terminal)

# Running the Application
No database is required for this program. To use it properly, run `main.py` in your IDE or terminal after ensuring the required versions of Python and Pandas are installed. Select '1' or '2' based on which tool you are trying to run, and input the values based on the questions asked. Entering an invalid value will require re-entry of the data.

# Suggested Inputs
The calculator is meant to work with any valid inputs, but for those unfamilliar with real estate values these example numbers work well:

* Price: `450000`, but any value should work.
* Cap: `10`, real world typically 1 to 4.
* Mortgage rate: `5`, current mortgage rate is around 5.1 but they have gone as low as 1.
* Loan type: `1` or `2`, most mortgages would be 1 (fixed).
* Ammortization: `25` or `30` years is typical.
* Downpayment: `25000`, property dependent so larger price higher downpayment required.
* Rental income: `5000`, can be any number but entirely property dependent.
* Repairs and  maintenance: `1`, 1% to 2% is typical value but its all about risk tolerance.
* Property tax rate: `1.2`, 1.2 is novascotias rate but ranges between 0.5-2 nationally.
* Utilities: `400`, once again can be anything depending on property.
* Monthly insurance: `110`, can be 50-200+ depending on property type and worth.
* Transfer tax: `1.5`, 1.5% is nova scotias rate and varies province to province.
* Legal fees: `1200`, usually correllated to property price.


# Academic Requirements
A video presentation of the projects use along with a detailed report can be found at the following Google Drive link:

PLACEHOLDER
