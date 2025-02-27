from setuptools import setup

setup(
    name="Config loader",
    version="0.0.2",
    description="Simple config loader",
    author="Eliseev Alexey",
    license="MIT",
    url="https://github.com/cs-eliseev/config_loader",
    packages=["config_loader"],
    package_dir={"config_loader": "config_loader"},
    install_requires=[
        "dotenv>=0.9.9",
        "python-dotenv>=1.0.1"
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
)