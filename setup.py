import os

from setuptools import find_packages, setup

# not so bad: http://joebergantine.com/blog/2015/jul/17/releasing-package-pypi/
version = __import__("socials").__version__


def read(fname):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django-socials",
    version=version,
    url="https://github.com/rouxcode/django-socials",
    license="MIT",
    platforms=["OS Independent"],
    description="fetch posts from various social media",
    long_description="none yet",
    author="Alaric Mägerle, Ben Stähli",
    author_email="info@rouxcode.ch",
    packages=find_packages(),
    install_requires=(
        "django>=1.11",
        "requests",
        "Pillow",
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
