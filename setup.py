from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='cloudconvert',
    version="0.1.0",
    description='cloudconvert for python',
    long_description=long_description,
    url='',
    author='izabeera',
    author_email='izabeera@gmail.com',
    license="Beerware",
    keywords="conversion",
    packages=find_packages('src', exclude=['example*']),
    package_dir={'': 'src'},
    install_requires=[
        'six',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    test_suite="cloudconvert.tests",
)
