import base64
import hashlib
import random

from sqlalchemy import Boolean, Column, ForeignKey, Interval, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import TSVectorType

from .database import db


# from django code
def hash_password(password, salt=None, iterations=180000, alg='pbkdf2_sha256'):
    if salt is None:
        rnd = random.SystemRandom()
        allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        salt = ''.join(rnd.choice(allowed_chars) for _ in range(12))

    password = password.encode('utf-8')

    passwd_hash = hashlib.pbkdf2_hmac(
        hashlib.sha256().name,
        password,
        salt.encode('ascii'),
        iterations,
    )
    passwd_hash = base64.b64encode(passwd_hash).decode('ascii').strip()

    return f'{alg}${iterations}${salt}${passwd_hash}'


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(length=255), index=True)
    prep_time = Column(Interval)
    difficulty = Column(SmallInteger)
    vegetarian = Column(Boolean)

    ratings = relationship('Rating', back_populates='recipe')

    search = Column(TSVectorType('name'))


class User(db.Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True)
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


class Rating(db.Model):
    __tablename__ = 'ratings'

    id = Column(UUID(as_uuid=True), primary_key=True)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey('recipes.id'))
    recipe = relationship('Recipe', back_populates='ratings')
    value = Column(SmallInteger)
