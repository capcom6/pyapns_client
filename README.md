<a name="readme-top"></a>

# pyapns_client3

[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](https://github.com/capcom6/pyapns_client/blob/main/LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/capcom6/pyapns_client.svg?style=for-the-badge)](https://github.com/capcom6/pyapns_client/issues)
[![GitHub Stars](https://img.shields.io/github/stars/capcom6/pyapns_client.svg?style=for-the-badge)](https://github.com/capcom6/pyapns_client/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/capcom6/pyapns_client.svg?style=for-the-badge)](https://github.com/capcom6/pyapns_client/network)
[![PyPI Version](https://img.shields.io/pypi/v/pyapns_client3.svg?style=for-the-badge)](https://pypi.org/project/pyapns_client3/)
[![Python Version](https://img.shields.io/pypi/pyversions/pyapns_client3.svg?style=for-the-badge)](https://pypi.org/project/pyapns_client3/)
[![Downloads](https://img.shields.io/pypi/dm/pyapns_client3.svg?style=for-the-badge)](https://pypi.org/project/pyapns_client3/)

<br />
<div align="center">
  <h3 align="center">Python APNS Client</h3>

  <p align="center">
    Simple, flexible, and fast Apple Push Notifications on iOS, OSX, and Safari using the HTTP/2 Push provider API.
    <br />
    <a href="https://github.com/capcom6/pyapns_client/issues">Report Bug</a>
    ·
    <a href="https://github.com/capcom6/pyapns_client/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
- [pyapns\_client3](#pyapns_client3)
  - [Features](#features)
  - [Built with](#built-with)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Client](#client)
    - [Authentificator](#authentificator)
    - [Payload](#payload)
    - [Exceptions](#exceptions)
    - [Logging](#logging)
  - [Example](#example)
  - [Roadmap](#roadmap)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)



## Features

- Uses the new Apple APNs HTTP/2 protocol with persistent connections
- Supports token-based authentication (no need to renew your certificates anymore) and certificate-based authentication
- Uses the httpx HTTP client library
- Supports the new iOS 10 features such as Collapse IDs, Subtitles, and Mutable Notifications
- Makes integration and error handling simple with auto-retry on APNs errors
- Supports asynchronous sending of notifications

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built with

- [![Python](https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
- [![httpx[http2]](https://img.shields.io/badge/httpx%5Bhttp2%5D-000000?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/httpx/)
- [![PyJWT](https://img.shields.io/badge/PyJWT-000000?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/PyJWT/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Prerequisites

Before using `pyapns_client3`, make sure you have the following:

- Python 3.6 or higher installed
- APNs SSL certificates (if using certificate-based authentication)
- An Apple Developer account with access to the Apple Push Notification service

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation

Install using pip:

```bash
pip install pyapns_client3
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

The library contains four main parts:

- Clients (sync and async)
- Authentificators (by token and certificate)
- Payloads
- Exceptions

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Client

The `APNSClient` and `AsyncAPNSClient` classes provide the main functionality for sending push notifications. The synchronous client allows you to send notifications in a blocking manner, while the asynchronous client enables you to send notifications in a non-blocking manner, suitable for asyncio-based applications. Both client classes can be used as context managers, allowing for automatic resource cleanup.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Authentificator

The library supports two types of authentication for sending push notifications. The `TokenBasedAuth` class allows you to authenticate using token-based authentication, eliminating the need to renew your APNS SSL certificates. The `CertificateBasedAuth` class enables certificate-based authentication, where you provide the path to your APNs SSL certificate and private key.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Payload

The library provides classes for creating different types of payloads for your push notifications. The `IOSPayload` class allows you to create a payload with various properties such as alert, badge, sound, and custom data. You can also use the `IOSPayloadAlert` class to create a payload alert with title, subtitle, and body.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Exceptions

The library defines several exceptions that can be raised during the push notification process. These exceptions include `UnregisteredException`, `APNSDeviceException`, `APNSServerException`, and `APNSProgrammingException`. You can catch these exceptions to handle different scenarios, such as unregistered devices, device-related errors, server-related errors, and programming errors.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Logging

`pyapns_client3` utilizes the standard `logging` package to provide built-in logging capabilities. The library includes an internal logger named `pyapns_client` that you can configure to track and debug the push notification process.

## Example

Here's an example of using the `AsyncAPNSClient` with token-based authentication to send push notifications asynchronously:

```python
# Import necessary classes and modules
from pyapns_client import AsyncAPNSClient, TokenBasedAuth, IOSPayload, IOSNotification

async def send_push_notifications():
    # Create an instance of the AsyncAPNSClient with the necessary parameters
    async with AsyncAPNSClient(
        mode=AsyncAPNSClient.MODE_DEV,
        authentificator=TokenBasedAuth(
            auth_key_path='/path/to/auth_key.p8',
            auth_key_id='AUTHKEY123',
            team_id='TEAMID1234'
        ),
        root_cert_path='/path/to/root_cert.pem',
    ) as client:
        try:
            # Create the payload for the notification
            payload = IOSPayload(alert='Hello from pyapns_client3!', sound='default')

            # Create the notification object with the payload and other optional parameters
            notification = IOSNotification(payload=payload, priority=10)

            # Send the notification asynchronously to one or more device tokens
            await client.push(notification=notification, device_token='DEVICE_TOKEN_HERE')
        except UnregisteredException as e:
            print(f'device is unregistered, compare timestamp {e.timestamp_datetime} and remove from db')
        except APNSDeviceException:
            print('flag the device as potentially invalid and remove from db after a few tries')
        except APNSServerException:
            print('try again later')
        except APNSProgrammingException:
            print('check your code and try again later')
        else:
            # Handle successful push
            print('Push notification sent successfully!')

# Run the async function to send push notifications
asyncio.run(send_push_notifications())
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

See the [open issues](https://github.com/capcom6/pyapns_client/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

The `pyapns_client3` library is licensed under the MIT License. You can find the full text of the license in the [LICENSE](https://github.com/capcom6/pyapns_client/blob/master/LICENSE) file.

This means that you are free to use, modify, and distribute this library for both personal and commercial purposes. However, the library is provided "as is" without any warranty, and the authors are not liable for any damages or issues arising from the use of the library.

By using `pyapns_client3`, you agree to the terms of the MIT License.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Project Link: [https://github.com/capcom6/pyapns_client](https://github.com/capcom6/pyapns_client)

<p align="right">(<a href="#readme-top">back to top</a>)</p>