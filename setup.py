from setuptools import setup
import re

_version_re = re.compile(r"(?<=^__version__ = (\"|'))(.+)(?=\"|')")

def get_version(rel_path: str) -> str:
    """
    Searches for the ``__version__ = `` line in a source code file.

    https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
    """
    with open(rel_path, 'r') as f:
        matches = map(_version_re.search, f)
        filtered = filter(lambda m: m is not None, matches)
        version = next(filtered, None)
        if version is None:
            raise RuntimeError(f'Could not find __version__ in {rel_path}')
        return version.group(0)


setup(
    name='pl-nesvor',
    version=get_version('nesvor_wrapper.py'),
    description='GPU-accelerated slice-to-volume reconstruction for fetal brain MRI',
    author='Junshen Xu',
    author_email='junshen@mit.edu',
    url='https://github.com/FNNDSC/pl-NeSVoR',
    py_modules=['nesvor_wrapper'],
    install_requires=['chris_plugin==0.2.0'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'nesvor_reconstruct = nesvor_wrapper:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1'
        ]
    }
)