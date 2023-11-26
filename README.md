
# Project Title

Black-Scholes Option Pricing Calculator


## Description

This Python program calculates option price and option "greeks" using the Black–Scholes model. The Black–Scholes model is a mathematical model for the dynamics of a financial market containing derivative investment instruments, providing a theoretical estimate of the price of European-style options.

 


## Prerequisites

- Python 3.x
- Required Python packages: `math`, `scipy`
## Usage

To use the option pricing calculator, run the main() function in the provided Python script. The program will prompt you to input the option type, current stock price, strike price, risk-free interest rate, time to maturity, and volatility of returns. Follow the on-screen instructions to input the required information.

I created two versions of the program; the original verion named "bs_option_pricer.py" and the OOP version named "bs_option_pricer_oop.py"

To run "bs_option_pricer.py" execute the following command in terminal: 
python bs_option_pricer.py

To run "bs_option_pricer_oop.py" execute the following command in terminal: 
python bs_option_pricer_oop.py
## Inputs
Option type: 'c' or 'call' for a call option, 'p' or 'put' for a put option.
option_type = Call or Put Option
S - Current(spot) price of an underlying asset
K - Strike Price
r - Risk-Free Interest Rate
t - Time to maturity
sigma -  Volatility of returns of the underlying asset, input as a decimal.
## Output
The program will display the calculated option price, delta, gamma, theta, vega, and rho based on the provided inputs.

Feel free to use, modify, and distribute this code as needed. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
