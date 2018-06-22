import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eksbase",
    version="0.0.1",
    author="Luc Denereaz",
    author_email="lucdenz@protonmail.com",
    description="A basic project using Amazon EKS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucdenz/eksbase",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        "console_scripts": ["eksbase=eksbase.cli:main"]
    }
)
