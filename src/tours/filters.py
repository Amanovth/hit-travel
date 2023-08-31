import django_filters


class Search(django_filters.FilterSet):
    authlogin = django_filters.CharFilter()
    authpass = django_filters.CharFilter()
    requestid = django_filters.CharFilter()
    departure = django_filters.NumberFilter()
    country = django_filters.NumberFilter()

    class Meta:
        model = None
        fields = ['authlogin', 'authpass', 'requestid', 'departure', 'country']


class Result(django_filters.FilterSet):
    authlogin = django_filters.CharFilter()
    authpass = django_filters.CharFilter()
    requestid = django_filters.CharFilter()

    class Meta:
        model = None
        fields = ['authlogin', 'authpass']