class PSOWrapperError(Exception):
    """Error base del wrapper PSO."""


class PSOValidationError(PSOWrapperError):
    """Error de validacion de entrada para el wrapper PSO."""


class PSOExecutionError(PSOWrapperError):
    """Error de ejecucion del wrapper PSO."""