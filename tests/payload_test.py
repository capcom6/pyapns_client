import pytest
from pyapns_client import (
    IOSPayload,
    IOSPayloadAlert,
    SafariPayload,
    SafariPayloadAlert,
)


@pytest.fixture
def ios_payload_alert():
    return IOSPayloadAlert(
        title="title",
        title_loc_key="title_loc_k",
        title_loc_args=["title_loc_a"],
        subtitle="subtitle",
        subtitle_loc_key="subtitle_loc_k",
        subtitle_loc_args=["subtitle_loc_a"],
        body="body",
        loc_key="body_loc_k",
        loc_args=["body_loc_a"],
        launch_image="img",
    )


def test_ios_payload_alert(ios_payload_alert):
    assert ios_payload_alert.to_dict() == {
        "title": "title",
        "title-loc-key": "title_loc_k",
        "title-loc-args": ["title_loc_a"],
        "subtitle": "subtitle",
        "subtitle-loc-key": "subtitle_loc_k",
        "subtitle-loc-args": ["subtitle_loc_a"],
        "body": "body",
        "loc-key": "body_loc_k",
        "loc-args": ["body_loc_a"],
        "launch-image": "img",
    }


def test_ios_payload():
    payload = IOSPayload(
        alert="my_alert",
        badge=2,
        sound="chime",
        content_available=True,
        mutable_content=True,
        category="my_category",
        custom={"extra": "something"},
        thread_id="42",
    )
    assert payload.to_dict() == {
        "aps": {
            "alert": "my_alert",
            "badge": 2,
            "sound": "chime",
            "content-available": 1,
            "mutable-content": 1,
            "thread-id": "42",
            "category": "my_category",
        },
        "extra": "something",
    }


def test_ios_payload_with_ios_payload_alert(ios_payload_alert):
    payload = IOSPayload(
        alert=ios_payload_alert,
        badge=2,
        sound="chime",
        content_available=True,
        mutable_content=True,
        category="my_category",
        custom={"extra": "something"},
        thread_id="42",
    )
    assert payload.to_dict() == {
        "aps": {
            "alert": {
                "title": "title",
                "title-loc-key": "title_loc_k",
                "title-loc-args": ["title_loc_a"],
                "subtitle": "subtitle",
                "subtitle-loc-key": "subtitle_loc_k",
                "subtitle-loc-args": ["subtitle_loc_a"],
                "body": "body",
                "loc-key": "body_loc_k",
                "loc-args": ["body_loc_a"],
                "launch-image": "img",
            },
            "badge": 2,
            "sound": "chime",
            "content-available": 1,
            "mutable-content": 1,
            "thread-id": "42",
            "category": "my_category",
        },
        "extra": "something",
    }


@pytest.fixture
def safari_payload_alert():
    return SafariPayloadAlert(
        title="title",
        body="body",
        action="send",
    )


def test_safari_payload_alert(safari_payload_alert):
    assert safari_payload_alert.to_dict() == {
        "title": "title",
        "body": "body",
        "action": "send",
    }


def test_safari_payload():
    payload = SafariPayload(
        alert="my_alert",
        # url_args = "args"  # omit this to test default
        custom={"extra": "something"},
    )
    assert payload.to_dict() == {
        "aps": {
            "alert": "my_alert",
            "url-args": [],
        },
        "extra": "something",
    }


def test_safari_payload_with_safari_payload_alert(safari_payload_alert):
    payload = SafariPayload(
        alert=safari_payload_alert,
        url_args="args",
        custom={"extra": "something"},
    )
    assert payload.to_dict() == {
        "aps": {
            "alert": {
                "title": "title",
                "body": "body",
                "action": "send",
            },
            "url-args": "args",
        },
        "extra": "something",
    }
