from enum import Enum, auto
from .factories_utils import enum_choices_factory


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class NomenclatureType(AutoName):
    PRODUCT = auto()
    RAW_MATERIAL = auto()


class NomenclatureKind(AutoName):
    PEN_FORM = auto()
    PEN_REFILL = auto()
    PENCIL_FORM = auto()
    PEN = auto()
    PENCIL = auto()
    PAINT = auto()


class Waybill(AutoName):
    SUPPLY = auto()
    SELLING = auto()


NOMENCLATURE_TYPE = enum_choices_factory(NomenclatureType)
NOMENCLATURE_KIND = enum_choices_factory(NomenclatureKind)
WAYBILL_TYPE = enum_choices_factory(Waybill)
