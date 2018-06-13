from setuptools import setup

setup(
    name="ekscore",
    version="0.1",
    description="A basic project using Amazon EKS.",
    author="lucdenz",
    author_email="lucdenz@protonmail.com",
    url="https://github.com/lucdenz/ekscore",
    license="MIT",
    packages=["ekscore"],
    install_requires=[
        "awscli",
        "boto3"
    ],
    entry_points={
        "console_scripts": ["ekscore=ekscore.cli:main"]
    },
    zip_safe=False
)