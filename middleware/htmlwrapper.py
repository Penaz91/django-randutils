"""
This file is part of the Django-RandUtils Project.
Copyright © 2023, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2023-08-29

Author: Penaz
"""
import json
from django.http import HttpResponse
from django.conf import settings


class HtmlWrapperMiddleware:
    """
    A middleware that wraps a response into an HTML one to allow debugging
    with Django Debug Toolbar

    It scans for a "debug" query parameter to turn on
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.DEBUG is True:
            if request.GET.get("debug", None) is not None:
                if response["Content-Type"] == "application/json":
                    # If it's a JSON Response, do some pretty printing
                    content = json.dumps(
                        json.loads(response.content),
                        sort_keys=True,
                        indent=4
                    )
                else:
                    # Else just wrap it
                    content = response.content
                response = HttpResponse(
                    f"<html><body><pre>{content}</pre></body></html>"
                )
        return response
