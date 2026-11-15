class BetgameError(Exception):
    """Basis für alle fachlichen Fehler im Spiel"""

    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(BetgameError):
    status_code = 404


class BettingClosedError(BetgameError):
    status_code = 409


class InsufficientCoinsError(BetgameError):
    status_code = 409
