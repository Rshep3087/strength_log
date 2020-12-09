# This file should contain records you want created when you run flask db seed.
#
# Example:
from strength_log.models import User, AccessoryLift


initial_user = {"email": "superadmin@mail.com", "password": "test"}
if User.find_by_email(initial_user["email"]) is None:
    User(**initial_user).save()

initial_accessory_lifts = [
    {"lift": "Dips"},
    {"lift": "Chin-Ups"},
    {"lift": "Leg Press"},
    {"lift": "Ab Wheel"},
    {"lift": "Lunges"},
    {"lift": "Good Mornings"},
    {"lift": "Barbell Rows"},
    {"lift": "Front Squat"},
    {"lift": "Hammer Curl"},
    {"lift": "Face Pulls", "user_id": 1},
]

for lift in initial_accessory_lifts:
    AccessoryLift(**lift).save()
