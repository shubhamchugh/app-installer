# coding=utf-8

from setuptools import setup

setup(
    author="kinuxer",
    author_email="kinuxer@outlook.com",
    name="app-installer",
    version="0.2",
    license="MIT",
    url="https://github.com/aerfensi/app-installer",
    py_modules=['install_apps','download',],
    install_requires=[
        'requests',
        'pyquery'],
    description="Android apps installation tool",
    entry_points={
        'console_scripts': ['install-apps=install_apps:main']
    }
)
