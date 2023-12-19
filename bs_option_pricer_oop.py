

import math
from scipy.stats import norm

class BlackScholesModel:
    def __init__(self, option_type, S, K, r, t, sigma):
        '''
        Initialize the BlackScholesModel object with the given parameters.
        '''
        self.option_type = option_type
        self.S = S
        self.K = K
        self.r = r
        self.t = t
        self.sigma = sigma

    def calculate_d1_d2(self):
        '''
        Calculate d1 and d2 for later use in option pricing formulas.
        '''
        d1 = (math.log(self.S / self.K) + (self.r + (self.sigma**2) / 2) * self.t) / (self.sigma * math.sqrt(self.t))
        d2 = d1 - self.sigma * math.sqrt(self.t)
        return d1, d2

    def calculate_N_values(self, d1, d2):
        '''
        Calculate various N values for option pricing.
        '''
        N_d1 = norm.cdf(d1)
        N_d1_gamma_theta_vega = norm.pdf(d1)
        N_d2 = norm.cdf(d2)
        N_neg_d1 = norm.cdf(-d1)
        N_neg_d2 = norm.cdf(-d2)
        return N_d1, N_d1_gamma_theta_vega, N_d2, N_neg_d1, N_neg_d2

    def calculate_call_price(self, N_d1, N_d2):
        '''
        Calculate call option price.
        '''
        return N_d1 * self.S - N_d2 * self.K * math.exp(-self.r * self.t)

    def calculate_put_price(self, N_neg_d1, N_neg_d2):
        '''
        Calculate put option price.
        '''
        return self.K * math.exp(-self.r * self.t) * N_neg_d2 - (self.S * N_neg_d1)

    def calculate_delta(self, N_d1, N_neg_d1):
        '''
        Calculate the delta value, a measure of option sensitivity to changes in the underlying asset price.
        '''
        if self.option_type in ["c", "call"]:
            return N_d1
        elif self.option_type in ["p", "put"]:
            return -N_neg_d1

    def calculate_gamma(self, N_d1_gamma_theta_vega):
        '''
        Calculate the gamma value, a measure of option sensitivity to changes in the underlying asset price.
        '''
        return N_d1_gamma_theta_vega / (self.S * self.sigma * math.sqrt(self.t))

    def calculate_theta(self, N_d1_gamma_theta_vega, N_d2, N_neg_d2):
        '''
        Calculate the theta value, a measure of option sensitivity to time decay.
        '''
        if self.option_type in ["c", "call"]:
            theta = -self.S * N_d1_gamma_theta_vega * self.sigma / (2 * math.sqrt(self.t)) - self.r * self.K * math.exp(-self.r * self.t) * N_d2
        elif self.option_type in ["p", "put"]:
            theta = -self.S * N_d1_gamma_theta_vega * self.sigma / (2 * math.sqrt(self.t)) + self.r * self.K * math.exp(-self.r * self.t) * N_neg_d2
        return theta / 365

    def calculate_vega(self, N_d1_gamma_theta_vega):
        '''
        Calculate the vega value, a measure of option sensitivity to changes in volatility.
        '''
        return (self.S * math.sqrt(self.t) * N_d1_gamma_theta_vega) / 100   # We are interested in 1% increase in volatility, thus we divide by 100

    def calculate_rho(self, N_d2, N_neg_d2):
        '''
        Calculate the rho value, a measure of option sensitivity to changes in interest rates.
        '''
        if self.option_type in ["c", "call"]:
            return (self.K * self.t * math.exp(-self.r * self.t) * N_d2) / 100  # We are interested in 1% increase in rates, thus we divide by 100
        elif self.option_type in ["p", "put"]:
            return (-self.K * self.t * math.exp(-self.r * self.t) * N_neg_d2) / 100 # We are interested in 1% increase in rates, thus we divide by 100

    def calculate_option_metrics(self):
        '''
        Calculate various option metrics using the Black-Scholes formulas.
        '''
        d1, d2 = self.calculate_d1_d2()
        N_d1, N_d1_gamma_theta_vega, N_d2, N_neg_d1, N_neg_d2 = self.calculate_N_values(d1, d2)

        # Call and put prices
        call_price = self.calculate_call_price(N_d1, N_d2)
        put_price = self.calculate_put_price(N_neg_d1, N_neg_d2)

        # Option "greeks"
        delta_value = self.calculate_delta(N_d1, N_neg_d1)
        gamma_value = self.calculate_gamma(N_d1_gamma_theta_vega)
        theta_value = self.calculate_theta(N_d1_gamma_theta_vega, N_d2, N_neg_d2)
        vega_value = self.calculate_vega(N_d1_gamma_theta_vega)
        rho_value = self.calculate_rho(N_d2, N_neg_d2)

        return call_price, put_price, delta_value, gamma_value, theta_value, vega_value, rho_value

def get_input():
    '''
    Gets the input from a user.
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
            r = float(r)
            # If input is in percentage, remove the percentage sign and convert to float
            if "%" in str(r):
                r = r.replace("%", "")
                r = float(r) / 100

            t = float(input("Time to maturity (in years): ").replace(",", "."))
            # If time to maturity is inputted as days to maturity, convert it to time to maturity in years
            if t > 1:
                t = t / 365

            sigma = input("Volatility of returns of an underlying asset: ").replace(",", ".")
            sigma = float(sigma)
            # If input is in percentage, remove the percentage sign and convert to float
            if "%" in str(sigma):
                sigma = sigma.replace("%", "")
                sigma = float(sigma) / 100

            return option_type, S, K, r, t, sigma
        except ValueError as e:
            print(str(e))

def main():
    # Get user input
    option_type, S, K, r, t, sigma = get_input()

    # Calculate option-related values
    option_model = BlackScholesModel(option_type, S, K, r, t, sigma)
    call_price, put_price, delta_value, gamma_value, theta_value, vega_value, rho_value = option_model.calculate_option_metrics()

    # Display results
    if option_type in ["c", "call"]:
        print(f"Call Option Price is {call_price}.")
    elif option_type in ["p", "put"]:
        print(f"Put Option Price is {put_price}.")

    print(f"Delta is {delta_value}.")
    print(f"Gamma is {gamma_value}.")
    print(f"Theta is {theta_value}.")
    print(f"Vega is {vega_value}.")
    print(f"Rho is {rho_value}.")


if __name__ == "__main__":
    main()

