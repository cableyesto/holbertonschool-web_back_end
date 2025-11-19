#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
import bcrypt

auth = Auth()

email = "bob@bob_test.com"
old_password = "MyPwdOfBob"
new_password = "NewPass123"

print("\n=== Creating user ===")
user = auth.register_user(email, old_password)
print("User created:", user)
print("Old hashed_password:", user.hashed_password)


# -------------------------------------------------------------
# ❌ 1. Update password with an invalid reset token → ValueError
# -------------------------------------------------------------
print("\n=== Test: invalid reset token ===")
invalid_token = "this-token-does-not-exist"

try:
    auth.update_password(invalid_token, new_password)
    print("FAILED: No ValueError raised with invalid token")
except ValueError:
    print("SUCCESS: ValueError correctly raised with invalid token")


# -------------------------------------------------------------
# ✔️ 2. Generate reset token, update password
# -------------------------------------------------------------
print("\n=== Generating valid reset token ===")
token = auth.get_reset_password_token(email)
print("Valid token:", token)


print("\n=== Test: valid reset token updates password ===")

# Store old password hash so we can confirm it changed
old_hash = user.hashed_password

auth.update_password(token, new_password)

print("Password updated successfully")

print("User after update:", user)
print("New hashed_password:", user.hashed_password)

# Check reset_token was cleared
if user.reset_token is None:
    print("SUCCESS: reset_token was cleared")
else:
    print("FAILED: reset_token was not cleared")

# Check password hash changed
if old_hash != user.hashed_password:
    print("SUCCESS: hashed_password was updated")
else:
    print("FAILED: hashed_password did not change")

# Check bcrypt compatibility (optional but good)
# if bcrypt.checkpw(new_password.encode(), user.hashed_password.encode()):
if bcrypt.checkpw(new_password.encode(), user.hashed_password):
    print("SUCCESS: New password is valid (bcrypt matches)")
else:
    print("FAILED: New password does NOT validate with bcrypt")

print("\n=== All tests completed ===")
