from enum import auto, StrEnum


class PortalRole(StrEnum):
    USER = auto()
    ADMIN = auto()
    SUPERADMIN = auto()
