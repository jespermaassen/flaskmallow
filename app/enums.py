import enum


class Ticker(enum.Enum):
    """
    Ticker names found on the virtual exchange
    """

    bitcoin = "btc_usd"
    ethereum = "eth_usd"
    ripple = "xrp_usd"

    def __str__(self):
        return f"{self.value}"


class ContractType(enum.Enum):
    """
    Contract Types that can be used on the exchange
    """

    long = "long"
    short = "short"

    def __str__(self):
        return f"{self.value}"


class ContractStatus(enum.Enum):
    """
    Contract Types that can be used on the exchange
    """

    open = "open"
    close = "close"
    cancelled = "cancelled"

    def __str__(self):
        return f"{self.value}"