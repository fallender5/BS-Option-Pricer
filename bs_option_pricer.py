

import math
from scipy.stats import norm

def main():
    # Get user input
    option_type, S, K, r, t, sigma = get_input()

    # Calculate option-related values
    option_price = bsmodel(option_type, S, K, r, t, sigma)
    delta_value = delta(option_type, S, K, r, t, sigma)
    gamma_value = gamma(S, K, r, t, sigma)
    theta_value = theta(option_type, S, K, r, t, sigma)
    vega_value = vega(S, K, r, t, sigma)
    rho_value = rho(option_type, S, K, r, t, sigma)

    # Display results
    if option_type in ["c", "call"]:
        print(f"Call Option Price is {option_price}.")
    elif option_type in ["p", "put"]:
        print(f"Put Option Price is {option_price}.")
    print(f"Delta is {delta_value}.")
    print(f"Gamma is {gamma_value}.")
    print(f"Theta is {theta_value}.")
    print(f"Vega is {vega_value}.")
    print(f"Rho is {rho_value}.")


def bsmodel(option_type, S, K, r, t, sigma):
    '''
    The Black–Scholes or Black–Scholes–Merton model is a mathematical model for the dynamics
    of a financial market containing derivative investment instruments, using various underlying assumptions.
    Black–Scholes formula gives a theoretical estimate of the price of European-style options and shows
    that the option has a unique price given the risk of the security and its expected return.
    Assumptions:    1. No Opportunities For Risk-Free Arbitrage
                    2. Constant Risk-Free Interest Rate
                    3. Constant Volatility
                    4. Log-Normal Distribution of Returns
                    5. No Transaction Cost or Taxes
                    6. Perfect Liquidity
                    7. European-Style Options

    Inputs:         S = Current(spot) price of an underlying asset
                    K = Strike price
                    r = Risk-Free Interest Rate
                    t = Time To Maturity
                    sigma = Volatility of Returns of an Underlying Asset
    '''
    # Calculate d1 and d2
    d1 = (math.log(S/K) + (r + (sigma**2)/2)*t)/(sigma*math.sqrt(t))
    d2 = d1 - sigma*math.sqrt(t)

    # Calculate cumulative distribution functions
    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)
    N_neg_d1 = norm.cdf(-d1)
    N_neg_d2 = norm.cdf(-d2)

    # Calculate option price based on option type
    if option_type in ["c", "call"]:
        C = N_d1*S - N_d2*K*math.exp(-r*t)
        return C
    elif option_type in ["p", "put"]:
        P = math.exp(-r * t) * K * N_neg_d2 - (S *N_neg_d1)
        return P


def get_input():
    '''
    Gets the user input.
    '''
    while True:
        try:
            # Get option type, stock price, strike price, risk-free interest rate, time to maturity, and volatility
            option_type = input("Option type - type 'c' or 'call' for call option, 'p' or 'put' for put option: ").lower()
            if option_type not in ["c", "call", "p", "put"]:
                raise ValueError("Please input 'c' or 'call' for call option, and 'p' or 'put' for put option")

            S = float(input("Current stock price: ").replace(",", "."))

            K = float(input("Strike price: ").replace(",", "."))

            r = str(input("Risk-free interest rate: ").replace(",", "."))
            # If input is in percentage, remove the percentage sign and convert to float
            if "%" in str(r):
                r = r.replace("%", "")
                r = float(r) / 100
            r = float(r)

            t = float(input("Time to maturity (in years): ").replace(",", "."))
            # If time to maturity is inputted as days to maturity, convert it to time to maturity in years
            if t > 1:
                t = t / 365

            sigma = input("Volatility of returns of an underlying asset: ").replace(",", ".")
            # If input is in percentage, remove the percentage sign and convert to float
            if "%" in str(sigma):
                sigma = sigma.replace("%", "")
                sigma = float(sigma) / 100
            sigma = float(sigma)

            return option_type, S, K, r, t, sigma
        except ValueError as e:
            print(str(e))



def delta(option_type, S, K, r, t, sigma):
    '''
    Delta is a measure of the sensitivity of an option’s price changes relative to the changes in the underlying asset’s price.
    In other words, if the price of the underlying asset increases by $1, the price of the option will change by Δ amount.
    Mathematically, the delta is defined as the first partial derivative of the option price with respect to the price of the underlying asset.
    '''
    d1 = (math.log(S/K) + (r + (sigma**2)/2)*t)/(sigma*math.sqrt(t))
    if option_type in ["c", "call"]:
        delta_value = norm.cdf(d1) # N(d1) is equal to options delta
        return delta_value
    elif option_type in ["p", "put"]:
        delta_value = -norm.cdf(-d1)
        return delta_value


def gamma(S, K, r, t, sigma):
    '''
    Gamma is a measure of the delta’s change relative to the changes in the price of the underlying asset.
    If the price of the underlying asset increases by $1, the option’s delta will change by the gamma amount.
    Mathematically, gamma of an option is the second partial derivative of the option's price with respect to the underlying asset's price.
    '''
    d1 = (math.log(S/K) + (r + (sigma**2)/2)*t)/(sigma*math.sqrt(t))
    N_d1 = norm.pdf(d1)
    gamma_value = N_d1 / (S * sigma *math.sqrt(t))
    return gamma_value

def theta(option_type, S, K, r, t, sigma):
    '''
    Theta is a measure of the sensitivity of the option price relative to the option’s time to maturity.
    If the option’s time to maturity decreases by one day, the option’s price will change by the theta amount.
    '''
    d1 = (math.log(S/K) + (r + (sigma**2)/2)*t)/(sigma*math.sqrt(t))
    d2 = d1 - sigma*math.sqrt(t)
    N_d1 = norm.pdf(d1)
    N_d2 = norm.cdf(d2)
    N_neg_d2 = norm.cdf(-d2)
    if option_type in ["c", "call"]:
        theta_value = - S * N_d1 * sigma/(2 * math.sqrt(t)) - r * K * math.exp(-r * t) * N_d2
        return theta_value/365
    elif option_type in ["p", "put"]:
        theta_value = - S * N_d1 * sigma/(2 * math.sqrt(t)) + r * K * math.exp(-r * t) * N_neg_d2
        return theta_value/365


def vega(S, K, r, t, sigma):
    '''
    Vega is an option Greek that measures the sensitivity of an option price relative to the volatility
    of the underlying asset. If the volatility of the underlying asses increases by 1%,
    the option price will change by the vega amount.
    '''
    d1 = (math.log(S/K) + (r + (sigma**2)/2)*t)/(sigma*math.sqrt(t))
    N_d1 = norm.pdf(d1)
    vega_value = S * math.sqrt(t) * N_d1
    return vega_value/100 # We are interested in 1% increase in volatility, thus we divide by 100


def rho(option_type, S, K, r, t, sigma):
    '''
    Rho measures the sensitivity of the option price relative to interest rates.
    If a benchmark interest rate increases by 1%, the option price will change by the rho amount.
    '''
    d1 = (math.log(S/K) + (r + (sigma**2)/2)*t)/(sigma*math.sqrt(t))
    d2 = d1 - sigma*math.sqrt(t)
    N_d2 = norm.cdf(d2)
    N_neg_d2 = norm.cdf(-d2)
    if option_type in ["c", "call"]:
        rho_value = K * t * math.exp(-r * t) * N_d2
        return rho_value/100 # We are interested in 1% increase in rates, thus we divide by 100
    elif option_type in ["p", "put"]:
        rho_value = -K * t * math.exp(-r * t) * N_neg_d2
        return rho_value/100 # We are interested in 1% increase in rates, thus we divide by 100


if __name__ == "__main__":
    main()




