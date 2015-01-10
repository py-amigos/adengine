from adengine.model import User, Ad

NOT_FOUND_ERROR = {
    "error": "Not found"
}


def build_api_url(id_=None):
    if id_ is not None:
        return "/api/users/{}".format(id_)
    return "/api/users"


def _new_ad(user, text="ad-text"):
    ad = Ad(text=text, author_id=user.id)
    return ad


def _new_user(name='Peter'):
    user = User(email='{name}@example.com'.format(name=name),
                name=name,
                username=name,
                password_hash='12346')

    return user


def _add_user(session, user):
    return _add_resource(session, user)


def _add_resource(session, resource):
    session.add(resource)
    session.commit()
    return resource


def test_user_added(session):
    """
    User should be added to the database and ID generated.
    """
    user = _new_user()
    _add_user(session, user)
    assert user.id > 0


def test_ads_created_by_user(session, app):
    """Ensure user refers all his ads."""
    # given
    user = _add_resource(session, _new_user(name='PeterUser'))
    ad1 = _add_resource(session, _new_ad(user, text="ad1-text"))
    ad2 = _add_resource(session, _new_ad(user, text="ad2-text"))

    # exercise
    ads = user.ads

    # verify
    assert ads == [ad1, ad2]
    assert ad1.author == user
