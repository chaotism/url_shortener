class ApplicationError(Exception):
    pass


class EntityError(ApplicationError):
    pass


class RepositoryError(ApplicationError):
    pass


class ServiceError(ApplicationError):
    pass
