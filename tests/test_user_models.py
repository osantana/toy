from recipes.models import User


def test_user_password_check():
    user = User(email='foo@example.com')
    user.set_password('sekret')

    assert user.check_password('sekret')


def test_user_unusable_password_check():
    user = User(email='foo@example.com', password='unusable')
    assert not user.check_password('sekret')
