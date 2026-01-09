class DomainError(Exception):
    """Base class for domain/service errors."""


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class UserNotFound(NotFoundError):
    pass


class EmailAlreadyExists(ConflictError):
    pass


class UsernameAlreadyExistsInCompany(ConflictError):
    pass

# --- Company ---
class CompanyNotFound(NotFoundError):
    pass


class CompanyCuiAlreadyExists(ConflictError):
    pass