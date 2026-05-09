import hashlib
import hmac
import json
import os
from pathlib import Path

from itsdangerous import URLSafeSerializer


BASE = Path('.projecttrack')
BASE.mkdir(exist_ok=True)

USERS_FILE = BASE / 'users.json'

if not USERS_FILE.exists():
    USERS_FILE.write_text('[]')


SECRET_KEY = os.environ.get('PROJECTTRACK_SECRET_KEY', 'projecttrack-dev-secret')
serializer = URLSafeSerializer(SECRET_KEY)


class AuthManager:
    def load_users(self):
        return json.loads(USERS_FILE.read_text())

    def save_users(self, users):
        USERS_FILE.write_text(json.dumps(users, indent=2))

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def signup(self, email: str, password: str):
        users = self.load_users()

        if any(u['email'] == email for u in users):
            raise ValueError('user already exists')

        user = {
            'email': email,
            'password_hash': self.hash_password(password),
            'role': 'owner',
        }

        users.append(user)
        self.save_users(users)

        return user

    def authenticate(self, email: str, password: str):
        users = self.load_users()
        password_hash = self.hash_password(password)

        for user in users:
            if user['email'] == email and hmac.compare_digest(user['password_hash'], password_hash):
                return user

        return None

    def create_session(self, email: str):
        return serializer.dumps({'email': email})

    def verify_session(self, token: str):
        try:
            return serializer.loads(token)
        except Exception:
            return None
