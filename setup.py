from setuptools import setup

setup(
    name='pcpolicy',
    version='v0.3.0',
    description='This command line utility allows for bulk updating of Prisma Cloud policies',
    author='Erick Moore',
    license='MIT',
    packages=['modules'],
    install_requires=[
        'requests',
        'colorama',
        'pandas',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'pcpolicy=modules.pcpolicy:main',
        ],
    },
    zip_safe=True
)