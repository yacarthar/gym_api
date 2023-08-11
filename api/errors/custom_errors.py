"""Customized Error"""
from typing import Dict


class Error(Exception):
    """BaseError"""
    def __init__(self, error: Dict[str, str], status_code: int):
        super().__init__()
        self.error = error
        self.status_code = status_code

class AuthError(Error):
    """Error in Authentication"""
    def __init__(self):
        self.error = {"test": "data"}
        self.status_code = 500