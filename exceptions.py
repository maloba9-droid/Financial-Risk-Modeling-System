# exceptions.py
class SystemError(Exception):
    """Base exception for the Financial Risk System."""
    pass

class DataFetchError(SystemError):
    """Raised when market data cannot be downloaded or found."""
    pass

class InvalidRiskParameterError(SystemError):
    """Raised when a risk parameter (like drop percentage) is mathematically invalid."""
    pass
