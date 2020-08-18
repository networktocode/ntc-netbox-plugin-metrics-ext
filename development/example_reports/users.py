"""This script contains an example of report about users."""
from extras.reports import Report
from django.contrib.auth.models import User


class CheckUser(Report):
    """Report for Users."""

    def test_is_uppercase(self):
        """Check that every user has his/her name in lowercase."""
        for user in User.objects.all():

            # Skip if not master of virtual chassis as only master should have primary IP
            if user.username != user.username.lower():
                self.log_failure(user, f"{user.username} is not in lowercase")
            else:
                self.log_success(user, f"{user.username} is in lowercase")
