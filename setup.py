from setuptools import setup

__version__ = '0.1.0'

setup(
    name="sguif",
    version=__version__,
    # url='https://github.com/sr9000/justree',
    author='Rogonov Stepan Alekseevich',
    author_email='rogonovstepan@gmail.com',
    description='Simplest GUI ever.',
    long_description='''Simple GUI components to build your Qt application in seconds.''',
    license="MIT License",
    packages=['sguif', 'sguif.engine', 'sguif.user_dialog', 'sguif.components', 'sguif.components.layout',
              'sguif.components.model', 'sguif.components.sketch'],
    keywords=['gui', 'qt', 'simple', 'framework'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
