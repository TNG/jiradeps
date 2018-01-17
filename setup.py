# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory


LICENSE = """
   Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

with open('README.md') as readme_file:
    README = readme_file.read()

from setuptools import setup, find_packages

setup(
    name='jiradeps',
    version='0.1',
    description=README,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'': ['README.md', 'LICENSE.md']},
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business :: Scheduling',
    ],
    install_requires=[
        'click>=6.7',
        'click-log>=0.2.1',
        'colorama>=0.3.9',
        'keyring>=10.5.0',
        'jira>=1.0.10',
        'networkx>=2.0',
        'graphviz>=0.8.1',
    ],
    entry_points='''
        [console_scripts]
        jiradeps=jiradeps.main:cli
    ''',
)
