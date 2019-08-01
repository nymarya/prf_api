import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brazilian_roads_api",
    version="0.0.1",
    author="Mayra Azevedo",
    author_email="mayradazevedo@ufrn.edu.br",
    description="Brazilian roads data API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nymarya/brazilian-roads-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
