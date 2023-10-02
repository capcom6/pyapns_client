import os
from distutils.command.clean import clean as _clean

from setuptools import setup


class CleanCommand(_clean):
    """
    A custom clean command to remove build artifacts.
    """

    def run(self):
        import os
        import shutil

        # remove the build directory
        build_dir = os.path.join(os.path.dirname(__file__), "build")
        shutil.rmtree(build_dir, ignore_errors=True)

        # remove any compiled Python files
        for root, dirs, files in os.walk(os.path.dirname(__file__)):
            for file in files:
                if file.endswith(".pyc") or file.endswith(".pyo") or file.endswith("~"):
                    os.remove(os.path.join(root, file))

        # call the base class's run method
        _clean.run(self)


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()
CHANGELOG = open(os.path.join(os.path.dirname(__file__), "CHANGELOG.rst")).read()


setup(
    name="pyapns_client3",
    version="3.0.3",
    packages=["pyapns_client"],
    include_package_data=True,
    license="MIT License",
    description="Simple, flexible and fast Apple Push Notifications on iOS, OSX and Safari using the HTTP/2 Push provider API with async support.",
    long_description="\n\n".join([README, CHANGELOG]),
    keywords="apns apple ios osx safari push notifications",
    url="https://github.com/capcom6/pyapns_client",
    author="Jakub Kleň",
    author_email="kukosk@gmail.com",
    maintainer="Aleksandr Soloshenko",
    maintainer_email="i@capcom.me",
    platforms="any",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    cmdclass={
        "clean": CleanCommand,
    },
    install_requires=[
        "httpx[http2]",
        "PyJWT>=2",
        "cryptography>=40.0.2",
        "pytz",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "wheel",
            "isort",
        ]
    },
)
