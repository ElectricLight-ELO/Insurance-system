class DomainError(Exception):
    """Нарушение бизнес-правил предметной области."""


class ValidationError(DomainError):
    """Ошибка валидации входных данных."""


class IntegrationError(DomainError):
    """Ошибка взаимодействия с внешней системой (API)."""
