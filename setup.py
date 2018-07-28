from setuptools import setup

setup(
    name='paytrekv2',
    packages=['paytrekv2'],
    version='0.0.7',
    description='Python client library for Paytrek API',
    author='Erkan Ay',
    license='MIT',
    author_email='erkanaycom@gmail.com',
    url='https://bitbucket.org/erkanay/paytrek-v2-python-client',
    keywords=['paytrek', 'client', 'payment', 'gateway'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'requests',
    ],
)
