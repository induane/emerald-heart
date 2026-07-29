from __future__ import annotations

from django.contrib.gis.geos import Point
from django.test import TestCase

from emerald_heart.models import User
from emerald_heart.views.search.search_service import get_all_members, get_member_by_id, get_members


class TestSearchService(TestCase):
    """Tests for the member search service functions."""

    fixtures = ["auth.json", "test_member_search.json"]

    def setUp(self):
        self.alice = User.objects.get(username="alice")
        self.bob = User.objects.get(username="bob")
        self.carol = User.objects.get(username="carol")
        self.dave = User.objects.get(username="dave")
        self.eve = User.objects.get(username="eve")

    def test_get_all_members_excludes_current_user_and_admin(self):
        """Results should not include the current user or the built-in admin user."""
        members = get_all_members(current_user=self.alice)
        usernames = {m.username for m in members}
        self.assertNotIn("alice", usernames)
        self.assertNotIn("admin", usernames)

    def test_get_all_members_includes_expected_users(self):
        """Results should include every other non-admin active member."""
        members = get_all_members(current_user=self.alice)
        usernames = {m.username for m in members}
        expected = {"bob", "carol", "dave", "eve"}

        # john and jane are also loaded via auth.json and are expected
        self.assertTrue(expected.issubset(usernames))
        self.assertNotIn("alice", usernames)
        self.assertNotIn("admin", usernames)

    def test_get_all_members_annotates_has_sent_request(self):
        """Every result should carry the has_sent_request annotation."""
        members = get_all_members(current_user=self.alice)
        for member in members:
            self.assertTrue(hasattr(member, "has_sent_request"))

    def test_get_all_members_request_sent_true(self):
        """Users alice has already requested should have has_sent_request=True."""
        members = get_all_members(current_user=self.alice)
        self.assertTrue(members.get(username="bob").has_sent_request)
        self.assertTrue(members.get(username="dave").has_sent_request)

    def test_get_all_members_request_sent_false(self):
        """Users alice has NOT requested should have has_sent_request=False."""
        members = get_all_members(current_user=self.alice)
        self.assertFalse(members.get(username="carol").has_sent_request)
        self.assertFalse(members.get(username="eve").has_sent_request)

    def test_get_all_members_none_current_user(self):
        """Passing current_user=None returns an empty queryset."""
        members = get_all_members(current_user=None)
        self.assertEqual(0, members.count())

    def test_get_members_spatial_includes_nearby(self):
        """A 5-mile search around KC should include bob and carol."""
        location = Point(-94.6, 39.1, srid=3857)
        members = get_members(location=location, distance=5, current_user=self.alice)
        usernames = {m.username for m in members}
        self.assertIn("bob", usernames)
        self.assertIn("carol", usernames)

    def test_get_members_spatial_excludes_distant(self):
        """A 5-mile search around KC should exclude NY and LA users."""
        location = Point(-94.6, 39.1, srid=3857)
        members = get_members(location=location, distance=5, current_user=self.alice)
        usernames = {m.username for m in members}
        self.assertNotIn("dave", usernames)
        self.assertNotIn("eve", usernames)

    def test_get_members_spatial_excludes_current_user_and_admin(self):
        """Spatial results exclude the searcher and admin regardless of location."""
        location = Point(-94.6, 39.1, srid=3857)
        members = get_members(location=location, distance=5, current_user=self.alice)
        usernames = {m.username for m in members}
        self.assertNotIn("alice", usernames)
        self.assertNotIn("admin", usernames)

    def test_get_members_spatial_annotates_has_sent_request(self):
        """Spatial results should carry has_sent_request."""
        location = Point(-94.6, 39.1, srid=3857)
        members = get_members(location=location, distance=5, current_user=self.alice)
        for member in members:
            self.assertTrue(hasattr(member, "has_sent_request"))

    def test_get_members_spatial_request_sent_values(self):
        """Spatial results have correct has_sent_request values."""
        location = Point(-94.6, 39.1, srid=3857)
        members = get_members(location=location, distance=5, current_user=self.alice)
        self.assertTrue(members.get(username="bob").has_sent_request)
        self.assertFalse(members.get(username="carol").has_sent_request)

    def test_get_members_no_location_falls_back_to_all(self):
        """When location is None get_members delegates to get_all_members."""
        members = get_members(current_user=self.alice)
        usernames = {m.username for m in members}
        expected = {"bob", "carol", "dave", "eve"}
        self.assertTrue(expected.issubset(usernames))
        self.assertNotIn("alice", usernames)
        self.assertNotIn("admin", usernames)

        # Verify annotations still work
        self.assertTrue(members.get(username="bob").has_sent_request)
        self.assertFalse(members.get(username="carol").has_sent_request)

    def test_get_members_no_distance_falls_back_to_all(self):
        """When distance is None get_members delegates to get_all_members."""
        location = Point(-94.6, 39.1, srid=3857)
        members = get_members(location=location, distance=None, current_user=self.alice)
        usernames = {m.username for m in members}
        expected = {"bob", "carol", "dave", "eve"}
        self.assertTrue(expected.issubset(usernames))
        self.assertNotIn("alice", usernames)
        self.assertNotIn("admin", usernames)

    def test_get_members_no_current_user_spatial(self):
        """Spatial search without current_user should not exclude or annotate."""
        location = Point(-94.6, 39.1, srid=3857)
        members = get_members(location=location, distance=5, current_user=None)
        usernames = {m.username for m in members}

        # alice is NOT excluded when current_user is None, but admin still is
        self.assertIn("alice", usernames)
        self.assertIn("bob", usernames)
        self.assertIn("carol", usernames)
        self.assertNotIn("admin", usernames)

    def test_get_member_by_id_returns_user(self):
        """Should return the matching User instance."""
        member = get_member_by_id(self.bob.id)
        self.assertEqual(self.bob, member)

    def test_get_member_by_id_missing_raises_404(self):
        """A non-existent id should raise Http404."""
        from django.http import Http404

        with self.assertRaises(Http404):
            get_member_by_id("99999999-9999-4999-9999-999999999999")
