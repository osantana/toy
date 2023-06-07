import base64
import hashlib
import random
from datetime import timedelta
from uuid import uuid4

from sqlalchemy import Boolean, Column, ForeignKey, Interval, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from sqlalchemy_utils import TSVectorType

from .database import db


# from django code
def _gen_salt():
    rnd = random.SystemRandom()
    allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(rnd.choice(allowed_chars) for _ in range(12))


def hash_password(password, salt=None, iterations=180000, alg='pbkdf2_sha256'):
    if salt is None:
        salt = _gen_salt()

    password = password.encode('utf-8')

    passwd_hash = hashlib.pbkdf2_hmac(
        hashlib.sha256().name,
        password,
        salt.encode('ascii'),
        iterations,
    )
    passwd_hash = base64.b64encode(passwd_hash).decode('ascii').strip()

    return f'{alg}${iterations}${salt}${passwd_hash}'


class User(db.Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(length=255), unique=True)
    password = Column(String(length=255), nullable=True)

    def set_password(self, raw_password):
        self.password = hash_password(raw_password)

    def check_password(self, raw_password):
        if self.password.count('$') < 3:
            return False

        alg, iterations, salt, _ = self.password.split('$', 3)
        result = hash_password(raw_password, salt, int(iterations), alg)
        return self.password == result


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(length=255), index=True)
    prep_time = Column(Interval, nullable=False)
    difficulty = Column(SmallInteger, nullable=False)
    vegetarian = Column(Boolean, nullable=False, default=False)

    ratings = relationship('Rating', back_populates='recipe', cascade='all, delete-orphan')

    search = Column(TSVectorType('name'))

    @validates('prep_time')
    def validate_preptime(self, _, value):
        if value < timedelta(0):
            raise ValueError('Invalid prep_time value')
        return value

    @validates('difficulty')
    def validate_difficulty(self, _, value):
        if value < 1 or value > 3:
            raise ValueError('Invalid difficulty value')
        return value


class Rating(db.Model):
    __tablename__ = 'ratings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey('recipes.id'), nullable=False)
    recipe = relationship('Recipe', back_populates='ratings')
    value = Column(SmallInteger, nullable=False)

    @validates('value')
    def validate_value(self, _, value):
        if value < 1 or value > 5:
            raise ValueError('Invalid rating value')
        return value
