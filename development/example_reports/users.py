"""This script contains an example of report about users."""
from django.contrib.auth import get_user_model
from extras.reports import Report

User = get_user_model()


class CheckUser(Report):
    """Report for Users."""

    def test_is_uppercase(self):
        """Check that every user has his/her name in lowercase."""
        for user in User.objects.all():
            if user.username != user.username.lower():
                self.log_failure(user, f"{user.username} is not in lowercase")
            else:
                self.log_success(user, f"{user.username} is in lowercase")
