"""Custom exception hierarchy for clintools."""


class StudyDataError(Exception):
    """Raised when required study data is missing or malformed."""
