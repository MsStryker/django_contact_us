import os
from setuptools import setup, find_packages

from contact_us import __version__


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


setup(
    name='Django Contact Us',
    version=__version__,
    description='Django Contact Us Page',
    long_description=README,
    author='Morgyn Stryker',
    author_email='hey@morgynstryker.com',
    url='https://github.com/MsStryker/django_contact_us',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'django>=1.11',
    ],
    extras_require={
        'test': [
            'factory_boy',
            'freezegun',
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
