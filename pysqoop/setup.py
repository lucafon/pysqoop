import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysqoop",
    version="0.0.7",
    author="Luca Fontanili",
    author_email="luca.fontanili93@gmail.com",
    description="A simple package to let you Sqoop in data in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucafon/pysqoop",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)