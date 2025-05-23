from setuptools import find_packages, setup

setup(
    name="camunda-querytool",
    version="0.0.1",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[open("requirements.txt").read().splitlines()],
)
