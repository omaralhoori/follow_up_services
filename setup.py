from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in document_follow_up/__init__.py
from document_follow_up import __version__ as version

setup(
	name="document_follow_up",
	version=version,
	description="Document follow up",
	author="Direct Direction for Information Technology",
	author_email="ibrahim.wahdan@direct-direction.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
