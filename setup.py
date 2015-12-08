from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
setup(
    name="waketor",
    version="0.0.1",
    author="Pierre-Elouan Rethore",
    author_email="pe@retho.re",
    description=("A vectorised wake model for scripting languages"),
    license="Apache v2.0",
    keywords="vectorised wind farm flow model wake",
    url="https://github.com/rethore/waketor",
    packages=['waketor', 'tests'],
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Science",
        "License :: OSI Approved :: Apache 2.0 License",
    ],
)
