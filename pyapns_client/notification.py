import json
from math import floor
from typing import Any, Dict, List, Union


class _PayloadAlert:
    """
    Represents an alert payload for a push notification service.
    """

    def __init__(
        self,
        title: Union[str, None] = None,
        body: Union[str, None] = None,
    ):
        """
        Initializes a new instance of the `_PayloadAlert` class.

        Args:
            title (str or None): The title of the alert.
            body (str or None): The body text of the alert.

        """
        super().__init__()

        self.title = title
        self.body = body

    def to_dict(self, alert_body: Union[str, None] = None):
        """
        Converts the alert payload to a dictionary.

        Args:
            alert_body (str or None): The body text of the alert. If not provided, the
            `body` attribute of this instance will be used.

        Returns:
            dict: A dictionary representation of the alert payload.

        """
        if alert_body is None:
            alert_body = self.body

        d = {}
        if self.title:
            d["title"] = self.title
        if alert_body:
            d["body"] = alert_body
        return d


class IOSPayloadAlert(_PayloadAlert):
    def __init__(
        self,
        title: Union[str, None] = None,
        subtitle: Union[str, None] = None,
        body: Union[str, None] = None,
        title_loc_key: Union[str, None] = None,
        title_loc_args: Union[List, None] = None,
        subtitle_loc_key: Union[str, None] = None,
        subtitle_loc_args: Union[List, None] = None,
        loc_key: Union[str, None] = None,
        loc_args: Union[List, None] = None,
        launch_image: Union[str, None] = None,
    ):
        super().__init__(title=title, body=body)

        self.subtitle = subtitle
        self.title_loc_key = title_loc_key
        self.title_loc_args = title_loc_args
        self.subtitle_loc_key = subtitle_loc_key
        self.subtitle_loc_args = subtitle_loc_args
        self.loc_key = loc_key
        self.loc_args = loc_args
        self.launch_image = launch_image

    def to_dict(self, alert_body=None):
        d = super().to_dict(alert_body=alert_body)
        if self.subtitle:
            d["subtitle"] = self.subtitle
        if self.title_loc_key:
            d["title-loc-key"] = self.title_loc_key
        if self.title_loc_args:
            d["title-loc-args"] = self.title_loc_args
        if self.subtitle_loc_key:
            d["subtitle-loc-key"] = self.subtitle_loc_key
        if self.subtitle_loc_args:
            d["subtitle-loc-args"] = self.subtitle_loc_args
        if self.loc_key:
            d["loc-key"] = self.loc_key
        if self.loc_args:
            d["loc-args"] = self.loc_args
        if self.launch_image:
            d["launch-image"] = self.launch_image
        return d


class SafariPayloadAlert(_PayloadAlert):
    """
    Represents an alert payload for Safari push notifications.

    This class inherits from the `_PayloadAlert` class and adds an `action` attribute.
    """

    def __init__(self, title: str, body: str, action: Union[str, None] = None):
        """
        Initializes a new instance of the `SafariPayloadAlert` class.

        Args:
            title (str): The title of the alert.
            body (str): The body text of the alert.
            action (str or None): The action associated with the alert.

        """
        super().__init__(title=title, body=body)

        self.action = action

    def to_dict(self, alert_body: Union[str, None] = None):
        """
        Converts the alert payload to a dictionary.

        Args:
            alert_body (str or None): The body text of the alert. If not provided, the
            `body` attribute of this instance will be used.

        Returns:
            dict: A dictionary representation of the alert payload.

        """
        d = super().to_dict(alert_body=alert_body)
        if self.action:
            d["action"] = self.action
        return d


class _Payload:
    """
    Represents a push notification payload.

    Attributes:
        MAX_PAYLOAD_SIZE (int): The maximum size of a push notification payload in
        bytes. See
        https://developer.apple.com/documentation/usernotifications/setting_up_a_remote_notification_server/generating_a_remote_notification#overview
    """

    MAX_PAYLOAD_SIZE = 4096

    def __init__(self, alert: Union[_PayloadAlert, str, None] = None, custom=None):
        """
        Initializes a new instance of the `_Payload` class.

        Args:
            alert (_PayloadAlert or str or None): The alert associated with the payload.
            custom (dict or None): Custom data associated with the payload.

        Raises:
            TypeError: If `alert` is not a string or a `_PayloadAlert` object.
        """
        super().__init__()

        if isinstance(alert, _PayloadAlert) or alert is None:
            self.alert = alert
        elif isinstance(alert, str):
            # Recommended to use dictionary, see https://developer.apple.com/documentation/usernotifications/setting_up_a_remote_notification_server/generating_a_remote_notification#2943360
            self.alert = _PayloadAlert(body=alert)
        else:
            value_type = type(alert)
            raise TypeError(
                f"alert must be a string or _PayloadAlert object, not a '{value_type}'"
            )
        self.custom = custom or {}

    def to_dict(self, alert_body: Union[str, None] = None):
        """
        Converts the payload to a dictionary.

        Args:
            alert_body (str or None): The body text of the alert. If not provided, the
            `body` attribute of this instance will be used.

        Returns:
            dict: A dictionary representation of the payload.
        Raises:
            TypeError: If `alert` is not a string or a `_PayloadAlert` object.
        """
        d = {"aps": {}}
        if self.alert is not None:
            d["aps"]["alert"] = self.alert.to_dict(alert_body=alert_body)
        d.update(self.custom)
        return d

    def to_json(self):
        """
        Converts the payload to a JSON string.

        Returns:
            bytes: A JSON string representation of the payload.
        """
        # This method automatically truncates self.alert.body if it's long.
        json_data = self._to_json()

        if self.alert and self.alert.body:
            alert_body = self.alert.body

            while alert_body:
                extra_bytes = len(json_data) - self.MAX_PAYLOAD_SIZE
                if extra_bytes <= 0:
                    break

                chars_to_strip = max(1, floor(extra_bytes / 10))
                alert_body = alert_body[:-chars_to_strip]
                new_alert_body = f"{alert_body}..."
                json_data = self._to_json(alert_body=new_alert_body)

        return json_data

    def _to_json(self, alert_body: Union[str, None] = None):
        """
        Converts the payload to a JSON string.

        Args:
            alert_body (str or None): The body text of the alert. If not provided, the
            `body` attribute of the `_PayloadAlert` object will be used.

        Returns:
            bytes: A JSON string representation of the payload.
        """
        return json.dumps(
            self.to_dict(alert_body=alert_body), separators=(",", ":"), sort_keys=True
        ).encode("utf-8")


class IOSPayload(_Payload):
    def __init__(
        self,
        alert: Union[_PayloadAlert, str, None] = None,
        badge=None,
        sound=None,
        category=None,
        custom=None,
        content_available=False,
        mutable_content=False,
        thread_id=None,
        target_content_id=None,
        interruption_level=None,
        relevance_score=None,
    ):
        super().__init__(alert=alert, custom=custom)

        self.badge = badge
        self.sound = sound
        self.category = category
        self.content_available = content_available
        self.mutable_content = mutable_content
        self.thread_id = thread_id
        self.target_content_id = target_content_id
        self.interruption_level = interruption_level
        self.relevance_score = relevance_score

    def to_dict(self, alert_body=None):
        d = super().to_dict(alert_body=alert_body)
        if self.badge is not None:
            d["aps"]["badge"] = int(self.badge)
        if self.sound:
            d["aps"]["sound"] = self.sound
        if self.category:
            d["aps"]["category"] = self.category
        if self.content_available:
            d["aps"]["content-available"] = 1
        if self.mutable_content:
            d["aps"]["mutable-content"] = 1
        if self.thread_id:
            d["aps"]["thread-id"] = self.thread_id
        if self.target_content_id:
            d["aps"]["target-content-id"] = self.target_content_id
        if self.interruption_level:
            d["aps"]["interruption-level"] = self.interruption_level
        if self.relevance_score is not None:
            d["aps"]["relevance-score"] = float(self.relevance_score)
        return d


class SafariPayload(_Payload):
    def __init__(
        self,
        alert: Union[_PayloadAlert, str, None] = None,
        url_args: Union[List[str], None] = None,
        custom=None,
    ):
        super().__init__(alert=alert, custom=custom)

        self.url_args = url_args or []

    def to_dict(self, alert_body: Union[str, None] = None):
        d = super().to_dict(alert_body=alert_body)
        d["aps"]["url-args"] = self.url_args
        return d


class PasskitPayload(_Payload):
    """
    Payload for PassKit notifications.
    """

    def __init__(self):
        super().__init__()

    def to_dict(self, alert_body=None) -> Dict[str, Any]:
        return {}


class _Notification:
    PRIORITY_HIGH = 10
    PRIORITY_LOW = 5

    PUSH_TYPE_ALERT = "alert"
    PUSH_TYPE_BACKGROUND = "background"
    PUSH_TYPE_VOIP = "voip"
    PUSH_TYPE_COMPLICATION = "complication"
    PUSH_TYPE_FILEPROVIDER = "fileprovider"
    PUSH_TYPE_MDM = "mdm"

    def __init__(
        self,
        payload,
        topic,
        apns_id=None,
        collapse_id=None,
        expiration=None,
        priority=None,
        push_type=None,
    ):
        super().__init__()

        # A byte array containing the JSON-encoded payload of this push notification.
        # Refer to "The Remote Notification Payload" section in the Apple Local and
        # Remote Notification Programming Guide for more info.
        self.payload = payload

        # The topic for the notification. If you’re using token-based authentication
        # with APNs, you must include this header with the correct bundle ID and
        # suffix combination.
        self.topic = topic

        # An optional canonical UUID that identifies the notification. The canonical
        # form is 32 lowercase hexadecimal digits, displayed in five groups separated
        # by hyphens in the form 8-4-4-4-12. An example UUID is as follows:
        # 	123e4567-e89b-12d3-a456-42665544000
        # If you don't set this, a new UUID is created by APNs and returned in the
        # response.
        self.apns_id = apns_id

        # A string which allows a notification to be replaced by a new notification
        # with the same CollapseID.
        self.collapse_id = collapse_id

        # An optional time at which the notification is no longer valid and can be
        # discarded by APNs. If this value is in the past, APNs treats the
        # notification as if it expires immediately and does not store the
        # notification or attempt to redeliver it. If this value is left as the
        # default (ie, Expiration.IsZero()) an expiration header will not added to the
        # http request.
        self.expiration = expiration

        # The priority of the notification. Specify either apns2.PRIORITY_HIGH (10) or
        # apns2.PRIORITY_LOW (5) If you don't set this, the APNs server will set the
        # priority to 10.
        self.priority = priority

        # (Required for watchOS 6 and later; recommended for macOS, iOS, tvOS, and
        # iPadOS) The value of this header must accurately reflect the contents of
        # your notification’s payload. If there is a mismatch, or if the header is
        # missing on required systems, APNs may return an error, delay the delivery
        # of the notification, or drop it altogether.
        self.push_type = push_type

    def get_headers(self):
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if self.topic:
            headers["apns-topic"] = str(self.topic)
        if self.apns_id:
            headers["apns-id"] = str(self.apns_id)
        if self.collapse_id:
            headers["apns-collapse-id"] = str(self.collapse_id)
        if self.priority:
            headers["apns-priority"] = str(self.priority)
        if self.expiration:
            headers["apns-expiration"] = str(self.expiration)
        if self.push_type:
            headers["apns-push-type"] = str(self.push_type)
        return headers

    def get_json_data(self):
        return self.payload.to_json()


class IOSNotification(_Notification):
    pass


class SafariNotification(_Notification):
    pass
