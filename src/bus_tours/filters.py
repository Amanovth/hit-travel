import django_filters
from .models import BusTours


class BusToursFilter(django_filters.FilterSet):
    datefrom = django_filters.DateFilter(
        field_name="datefrom", lookup_expr="gte", label="Start Date"
    )

    class Meta:
        model = BusTours
        fields = {
            "departure": ["exact"],
            "num_of_tourists": ["exact"],
            "cat": ["exact"],
        }
