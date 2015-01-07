__author__ = 'signalpillar'

import json

from adengine.models.user import User
from adengine.models.ad import Ad  # noqa

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


def test_get_all_users(session, app):
    """
    Should return all added users.
    """
    # given
    user1 = _new_user(name='Eugene')
    user2 = _new_user(name='Vova')
    _add_user(session, user1)
    _add_user(session, user2)
    client = app.test_client()

    # execute
    all_users = json.loads(client.get(build_api_url()).data)

    # verify
    assert 2 == len(all_users.get("objects"))


def test_delete_non_existing_user(session, app):
    """
    Should fail in attempt to delete non-existing user.
    """
    # given
    user_id = -1
    client = app.test_client()

    # exercise
    query = '/api/v1.0/users/{user_id}'.format(user_id=user_id)
    result = client.delete(query)

    # verify
    result.status_code == 404


# TODO: fix the test case
def _test_user_deleted(session, app):
    """
    Should delete user using View class for users.
    """
    # given
    user = _new_user(name='to-delete')
    _add_user(session, user)
    client = app.test_client()

    # exercise
    print build_api_url(user.id)
    result = client.delete(build_api_url(user.id))

    # verify
    assert user.id == json.loads(result.data).get('id')
    assert None == User.query.filter_by(id=user.id).first()
    result.status_code == 404


def test_get_user_by_id(session, app):
    """
    Should return user by its identifier.
    """
    # given
    user = _new_user(name='Ivan')
    _add_user(session, user)
    client = app.test_client()
    # exercise
    query = build_api_url(user.id)
    user_in_db = json.loads(client.get(query).data)

    # verify
    assert user.id == user_in_db.get('id')


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
