from setuptools import setup, find_packages

setup(
    name='dropper',
    version='0.0.1',
    author='tonic',
    zip_safe=False,
    author_email='tonicbupt@gmail.com',
    description='CLI tool to build elastic IP from AWS',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts':[
            'dropper=dropper.main:main',
        ],
    },
    install_requires=[
        'click==7.0',
        'tabulate==0.8.2',
        'boto3==1.9.16',
    ],
)
