import typing

import pytest

from pyapns_client import (
    IOSNotification,
    IOSPayload,
    IOSPayloadAlert,
    SafariPayload,
    SafariPayloadAlert,
)


# iOS
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


def test_ios_payload_alert(ios_payload_alert: IOSPayloadAlert):
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
    ios_payload = IOSPayload(
        alert="my_alert",
        badge=2,
        sound="chime",
        content_available=True,
        mutable_content=True,
        category="my_category",
        custom={"extra": "something"},
        thread_id="42",
    )
    assert ios_payload.to_dict() == {
        "aps": {
            "alert": {"body": "my_alert"},
            "badge": 2,
            "sound": "chime",
            "content-available": 1,
            "mutable-content": 1,
            "thread-id": "42",
            "category": "my_category",
        },
        "extra": "something",
    }
    assert ios_payload.to_json() == (
        b'{"aps":{"alert":{"body":"my_alert"},"badge":2,"category":"my_category",'
        b'"content-available":1,"mutable-content":1,"sound":"chime","thread-id":"42"},'
        b'"extra":"something"}'
    )


def test_ios_notification():
    ios_payload = IOSPayload(
        alert="my_alert",
        badge=2,
        sound="chime",
        content_available=True,
        mutable_content=True,
        category="my_category",
        custom={"extra": "something"},
        thread_id="42",
    )
    notification = IOSNotification(
        ios_payload, "com.example.test", priority=IOSNotification.PRIORITY_LOW
    )

    assert notification.get_json_data() == (
        b'{"aps":{"alert":{"body":"my_alert"},"badge":2,"category":"my_category",'
        b'"content-available":1,"mutable-content":1,"sound":"chime","thread-id":"42"},'
        b'"extra":"something"}'
    )

    assert notification.get_headers() == {
        "Content-Type": "application/json; charset=utf-8",
        "apns-priority": "5",
        "apns-topic": "com.example.test",
    }


def test_ios_payload_with_ios_payload_alert(ios_payload_alert: IOSPayloadAlert):
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
    assert payload.to_json() == (
        b'{"aps":{"alert":{"body":"body","launch-image":"img","loc-args":["body_loc_a"],'
        b'"loc-key":"body_loc_k","subtitle":"subtitle","subtitle-loc-args":["subtitle_loc_a"],'
        b'"subtitle-loc-key":"subtitle_loc_k","title":"title","title-loc-args":["title_loc_a"],'
        b'"title-loc-key":"title_loc_k"},'
        b'"badge":2,"category":"my_category","content-available":1,"mutable-content":1,'
        b'"sound":"chime","thread-id":"42"},"extra":"something"}'
    )


def test_ios_notification_with_ios_payload_alert(ios_payload_alert: IOSPayloadAlert):
    ios_payload = IOSPayload(
        alert=ios_payload_alert,
        badge=2,
        sound="chime",
        content_available=True,
        mutable_content=True,
        category="my_category",
        custom={"extra": "something"},
        thread_id="42",
    )
    notification = IOSNotification(
        ios_payload, "com.example.test", priority=IOSNotification.PRIORITY_LOW
    )

    assert notification.get_json_data() == (
        b'{"aps":{"alert":{"body":"body","launch-image":"img","loc-args":["body_loc_a"],'
        b'"loc-key":"body_loc_k","subtitle":"subtitle","subtitle-loc-args":["subtitle_loc_a"],'
        b'"subtitle-loc-key":"subtitle_loc_k","title":"title","title-loc-args":["title_loc_a"],'
        b'"title-loc-key":"title_loc_k"},'
        b'"badge":2,"category":"my_category","content-available":1,"mutable-content":1,'
        b'"sound":"chime","thread-id":"42"},"extra":"something"}'
    )

    assert notification.get_headers() == {
        "Content-Type": "application/json; charset=utf-8",
        "apns-priority": "5",
        "apns-topic": "com.example.test",
    }


# Safari
@pytest.fixture
def safari_payload_alert(action: typing.Union[str, None]):
    return SafariPayloadAlert(title="title", body="body", action=action)


@pytest.fixture
def safari_payload(
    alert: typing.Union[SafariPayloadAlert, str],
    url_args: typing.Union[typing.List[str], None],
):
    return SafariPayload(
        alert=alert,
        url_args=url_args,
        custom={"extra": "something"},
    )


@pytest.mark.parametrize(
    "action,additional_fields", [(None, {}), ("send", {"action": "send"})]
)
def test_safari_payload_alert(
    safari_payload_alert: SafariPayloadAlert,
    additional_fields: typing.Dict[str, typing.Any],
):
    expected = {
        "title": "title",
        "body": "body",
    }
    expected.update(additional_fields)

    assert safari_payload_alert.to_dict() == expected


@pytest.mark.parametrize(
    "url_args,expected_url_args", [(None, []), (["args"], ["args"])]
)
@pytest.mark.parametrize(
    "alert,expected_alert",
    [
        ("my_alert", {"body": "my_alert"}),
        (
            SafariPayloadAlert(title="title", body="body", action="send"),
            {
                "title": "title",
                "body": "body",
                "action": "send",
            },
        ),
    ],
)
def test_safari_payload(
    safari_payload: SafariPayload, expected_url_args, expected_alert
):
    assert safari_payload.to_dict() == {
        "aps": {
            "alert": expected_alert,
            "url-args": expected_url_args,
        },
        "extra": "something",
    }
