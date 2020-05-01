import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json-graph-lite",
    version="0.4a0",
    author="Roman Suzi",
    author_email="roman.suzi@gmail.com",
    description="Lightweight graph implementation with JSON serialization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rnd0101/json-graph-lite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    # setup_requires=['pytest-runner'],  # Breaks package-building
    tests_require=['pytest'],
)
