from enum import Enum


class Doctype(Enum):
    ENEDIS_MINUTE = "com.grandlyon.enedis.minute"
    ENEDIS_DAY = "com.grandlyon.enedis.day"
    ENEDIS_MONTH = "com.grandlyon.enedis.month"
