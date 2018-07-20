# coding: utf-8

from __future__ import unicode_literals


_sessions = {}


def get(user_id):
    session_obj = _sessions.get(user_id)
    if not session_obj:
        session_obj = {
            'game': None,
            'last': None,
            'opponent': None,
        }
        _sessions[user_id] = session_obj
    return session_obj
