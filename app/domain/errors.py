class DomainError(Exception):
    """Нарушение бизнес-правил предметной области."""


class NotFoundError(DomainError):
    """Сущность не найдена."""


class IntegrationError(DomainError):
    """Ошибка взаимодействия c внешней системой."""
