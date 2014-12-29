__author__ = 'jkf'
from adengine.models.user import User
from adengine.models.ad import Ad  # noqa
from adengine.models.comment import Comment


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


def test_comments_refers_both_ad_and_user(session):
    "Ensure comments added are referneced from the Ad"
    # given
    user = _add_resource(session, _new_user(name='PeterGeneralUser'))
    user1 = _add_resource(session, _new_user(name='PeterGeneralUserGrant'))
    ad = _add_resource(session, _new_ad(user, text="ad1-text1"))
    comment = _add_resource(session, _new_comment(ad, user, text="ad11-text1"))
    comment1 = _add_resource(session, _new_comment(ad, user1,
                                                   text="ad12-text1"))
    # exercise
    comments = ad.comments

    # verify
    assert comments == [comment, comment1]
    # verify comment have user filled in
    assert comment.user == user
    assert comment1.user == user1
    # verify comment have backref on Ad
    assert comment.ad == ad
    assert comment1.ad == ad
