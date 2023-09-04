"""
This file is part of the Django-Randutils Project.
Copyright © 2023, Daniele Penazzo. All Rights Reserved.
The use of this code is governed by the MIT license attached.
See the LICENSE file for the full license.

Created on: 2023-09-04

Author: Penaz
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.admin.sites import all_sites
from django.contrib.auth import get_user_model
from parameterized import parameterized


PARAMS = [
    (
        f"{site.name}_{str(model_admin).replace('.', '_')}",
        f"{site.name}:{model._meta.app_label}_{model._meta.model_name}_{page}",
        []
    )
    for page in ("changelist", "add")
    for site in all_sites
    for model, model_admin in site._registry.items()
]


class AdminTestCase(TestCase):
    """
    Tests admin sanity for some cases
    """
    fixtures = []

    def setUp(self):
        """
        Sets up the environment, creating the superuser needed to test
        the admin
        """
        User = get_user_model()
        User.objects.create_superuser(
            "testadmin", "test@test.com", "testpass"
        )
        self.client.login(
            username="testadmin",
            password="testpass"
        )

    @parameterized.expand(PARAMS)
    def test_admin_view(self, name, rev, urlargs):
        """
        Tests that the admin view is viewable and doesn't throw exceptions
        """
        url = reverse(rev, args=urlargs)
        resp = self.client.get(url)
        # Check the status Code
        self.assertIn(resp.status_code, (200, 403))

    @parameterized.expand(PARAMS)
    def test_admin_search(self, name, rev, urlargs):
        """
        Tests that the admin view is searchable and doesn't throw exceptions
        """
        url = reverse(rev, args=urlargs)
        resp = self.client.get(f"{url}?q=tests")
        # Check the status Code
        self.assertIn(resp.status_code, (200, 403))
