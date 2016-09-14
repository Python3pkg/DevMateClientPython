class LicenseStatus(object):
    NOT_USED = 1
    ACTIVE = 2
    EXPIRED = 3
    BLOCKED = 4
    RETURNED = 5


class HistoryRecordType(object):
    ACTIVATION = 1
    CREATING = 2
    EXPIRING = 3
    BLOCKING = 4
    RETURNING = 5
    RESETTING = 6
