""" Module for user data accessing functions. """

import os
from hashlib import sha256

from sqlalchemy.orm.exc import NoResultFound

from models import User

from exceptions import SocketIOEventError


class LoginError(SocketIOEventError):
    """ Thrown when an issue preventing a successful login occurs. """

    event = "login_failed"


class RegistrationError(SocketIOEventError):
    """ thrown when an issue preventing registration occurs. """

    event = "registration_failed"


def get_user(session, user_id):
    """ Get a user by their id. """

    return session.query(User).filter_by(id=user_id).one()


def create_user(session, name, email, password):
    """Create a new user in the database.

    The password is salted and hashed, so the value is not stored
    in plain text.
    """

    salt = os.urandom(32)
    hashed = sha256(salt + password.encode()).digest()

    if session.query(User).filter_by(email=email).first() is not None:
        raise RegistrationError(f"{email} email address is already in use")

    user = User(name=name, email=email, password=hashed.hex(), salt=salt.hex())

    session.add(user)
    return user


def login_user(session, email, password):
    """ Attempt to authenticate the user given their email and password. """

    try:
        user = session.query(User).filter_by(email=email).one()
    except NoResultFound as error:
        raise LoginError(f"{email} not associated with a user") from error

    hash = sha256(bytes.fromhex(user.salt) + password.encode()).digest()

    if hash != bytes.fromhex(user.password):
        raise LoginError(f"Password was incorrect for {email}")

    user.ping()
    session.commit()
    return user
