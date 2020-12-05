import enum


class Ticker(enum.Enum):
    """
    Ticker names found on the virtual exchange
    """

    BITCOIN = "btc_usd"
    ETHEREUM = "eth_usd"

    def __str__(self):
        return f"{self.value}"


class ContractType(enum.Enum):
    """
    Contract Types that can be used on the exchange
    """

    LONG = "long"
    SHORT = "short"

    def __str__(self):
        return f"{self.value}"