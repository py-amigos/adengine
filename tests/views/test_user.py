import json

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


def test_user_added(client):
    """
    User should be added to the database and ID generated.
    """
    user = _new_user()
    result = client.post(
        build_api_url(),
        data=json.dumps(user.as_dict()),
        content_type='application/json'
    )
    print result.data, result
    assert 201 == result.status_code


def test_get_all_users(session, client):
    """
    Should return all added users.
    """
    # given
    user1 = _new_user(name='Eugene')
    user2 = _new_user(name='Vova')
    _add_user(session, user1)
    _add_user(session, user2)

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


def test_user_deleted(session, client):
    """Should delete user using View class for users."""
    # given
    user = _new_user(name='to-delete')
    _add_user(session, user)

    # exercise
    result = client.delete(build_api_url(user.id))

    # verify
    assert result.status_code == 204
    assert None == User.query.filter_by(id=user.id).first()


def test_get_user_by_id(session, app):
    """
    Should return user by its identifier.
    """
    # given
    user = _new_user(name='Ivan')
    _add_user(session, user)
    client = app.test_client()
    query = build_api_url(user.id)

    # exercise
    user_in_db = json.loads(client.get(query).data)

    # verify
    assert user.id == user_in_db.get('id')
