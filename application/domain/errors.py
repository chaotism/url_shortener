class ApplicationError(Exception):
    pass


class EntityError(ApplicationError):
    pass


class RepositoryError(ApplicationError):
    pass


class ServiceError(ApplicationError):
    pass


class UserNotFound(ApplicationError):
    pass


class AccountNotFound(ApplicationError):
    pass


class TransactionNotFound(ApplicationError):
    pass


class StatusFinalized(ApplicationError):
    pass


class AmountNotSet(ApplicationError):
    pass
