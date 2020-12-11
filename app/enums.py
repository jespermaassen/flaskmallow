import enum


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
    closed = "closed"
    cancelled = "cancelled"

    def __str__(self):
        return f"{self.value}"