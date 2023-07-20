"""
This file is part of the Django-RandUtils Project.
Copyright © 2023, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2023-07-20

Author: Penaz
"""
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class SearchListView(ListView):
    """
    A ListView subclass that allows filtering via GET parameters
    """
    search_parameter: str = "q"
    search_fields: tuple[str] = tuple()

    def get_search_fields(self) -> tuple[str]:
        """
        Return a tuple of strings representing the fields of the model
        the view should search on
        """
        if len(self.search_fields) == 0:
            raise ImproperlyConfigured(
                "SearchListView requires at least a definition of "
                "'search_fields' or an implementation of "
                "'get_search_fields()'."
            )
        return self.search_fields

    def get_queryset(self):
        """
        Gets the queryset and filters it by the GET parameter set in
        self.search_parameter for each field in search_fields.
        If more than one search_field is defined, the query ORs all the
        searched fields.
        """
        filter_value = self.request.GET.get(self.search_parameter, "")
        queryset = super().get_queryset()
        if filter_value:
            query = Q()
            for filter_inst in self.get_search_fields():
                query |= Q(**{filter_inst: filter_value})
            queryset = queryset.filter(query)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        """
        Adds the filter GET parameter to the context so it can be pre-filled
        at page reload
        """
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', "")
        return context
