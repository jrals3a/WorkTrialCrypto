# utils/funding_rate.py
# define calculate_apr
def calculate_apr(funding_rate: float, payout_frequency: int = 3) -> float:
    """
    Calculate estimated APR from funding rate
    
    Args:
        funding_rate: Current funding rate (e.g., 0.0001 for 0.01%)
        payout_frequency: Number of funding payments per day (typically 3 for 8-hour intervals)
    
    Returns:
        Estimated APR as a percentage (e.g., 10.95 for 10.95%)
    """
    daily_rate = funding_rate * payout_frequency
    annual_rate = ((1 + daily_rate) ** 365 - 1) * 100
    return annual_rate

# define analyze_funding_rates
def analyze_funding_rates(rates: Dict[str, float]) -> Dict:
    """
    Analyze funding rates across multiple exchanges
    
    Args:
        rates: Dictionary of {exchange: funding_rate}
    
    Returns:
        Dictionary with analysis including best/worst rates and arbitrage opportunities
    """
    if not rates:
        return {}
    
    sorted_rates = sorted(rates.items(), key=lambda x: x[1])
    
    return {
        'highest_rate': sorted_rates[-1],
        'lowest_rate': sorted_rates[0],
        'rate_spread': sorted_rates[-1][1] - sorted_rates[0][1],
        'arbitrage_opportunity': abs(sorted_rates[-1][1] - sorted_rates[0][1]) > 0.0005  # Threshold
    }