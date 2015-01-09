__author__ = 'jkf'

import json

from adengine.model import User, Ad, Comment


def build_api_url(id_=None):
    if id_ is not None:
        return "/api/ads/{}".format(id_)
    return "/api/ads"


def _add_resource(session, resource):
    session.add(resource)
    session.commit()
    return resource


def _new_ad(user, text="ad-text"):
    ad = Ad(text=text, author_id=user.id)
    return ad


def _new_user(name='Peter'):
    user = User(email='{name}@example.com'.format(name=name),
                name=name,
                username=name,
                password_hash='12346')
    return user


def _new_comment(ad, user, text='bla-bla-bla'):
    comment = Comment(text=text,
                      ad_id=ad.id,
                      author_id=user.id)
    return comment


def test_comments_refers_both_ad_and_user(session, app):
    "Ensure comments added are referneced from the Ad"
    # given
    user = _add_resource(session, _new_user(name='PeterGeneralUser'))
    user1 = _add_resource(session, _new_user(name='PeterGeneralUserGrant'))
    ad = _add_resource(session, _new_ad(user, text="ad1-text1"))
    _add_resource(session, _new_comment(ad, user, text="ad11-text1"))
    _add_resource(session, _new_comment(ad, user1, text="ad12-text1"))

    client = app.test_client()

    # exercise
    query = build_api_url()
    doc = json.loads(client.get(query).data)

    # verify
    print doc
    assert 1 == len(doc.get("objects"))
