from setuptools import setup

setup (
    name="tr01-modules",
    version = "0.1",
    author="NickRodriguez",
    author_email="nick@dashanddata.com",
    description = "Tu Rincon modules includes models and config for TR applications",
    packages=['tr01_config','tr01_models'],
    python_requires=">=3.6",
    )