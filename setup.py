from setuptools import setup, find_packages

setup(
    name='Jenkins trigger build Utility service'
    version='1.0.0'
    description='This service can be used to fire build on jenkins for any dynamic job'
    author='Hitesh Bhandari'
    author_email='hbhandari@digite.com'
    url='http://swiftops.digite.com/pyjenkins_service/build',
    install_requires=open('requirements.txt').read(),
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.md').read(),
)
