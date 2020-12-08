# This file should contain records you want created when you run flask db seed.
#
# Example:
from strength_log.models import User


initial_user = {"email": "superadmin", "password": "test"}
if User.find_by_email(initial_user["email"]) is None:
    User(**initial_user).save()
