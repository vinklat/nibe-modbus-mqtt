# -*- coding: utf-8 -*-

import setuptools
from nibe_modbus_mqtt.version import __version__

try:
    with open('README.md', 'r', encoding='UTF-8') as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "README.md not found"

try:
    with open('requirements.txt', 'r', encoding='UTF-8') as fh:
        required = fh.read().splitlines()
except FileNotFoundError:
    required = []

setuptools.setup(name="nibe-modbus-mqtt",
                 version=__version__,
                 author="Václav Vinklát",
                 author_email="vin@email.cz",
                 description="MQTT bridge for a Nibe heat pump connected to the Modbus.",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/vinklat/nibe-modbus-mqtt",
                 include_package_data=True,
                 zip_safe=False,
                 packages=setuptools.find_packages(),
                 install_requires=required,
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 entry_points={
                     'console_scripts': ['nibe-modbus-mqtt=nibe_modbus_mqtt.main:main'],
                 })
