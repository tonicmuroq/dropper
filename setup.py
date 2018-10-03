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
            'eru-cli=erucli.console.cmdline:main',
            'dropper=dropper.main:main',
        ],
    },
    install_requires=[
        'click>=2.0',
        'tabulate',
        'boto3',
    ],
)
