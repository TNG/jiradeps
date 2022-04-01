# Copyright 2018,2022 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory
from pathlib import Path

from setuptools import find_packages
from setuptools import setup

LICENSE = """
   Copyright 2018,2022 TNG Technology Consulting GmbH, Unterföhring, Germany

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


setup(
    name="jiradeps",
    version="0.1",
    description=Path("README.md").read_text(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "": ["README.md", "LICENSE.md"],
        "jiradeps": ["default.jiradepsrc"],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Topic :: Office/Business :: Scheduling",
    ],
    install_requires=[
        "click>=6.7",
        "click-log>=0.3",
        "colorama>=0.3",
        "keyring>=13.2",
        "jira>=3.0",
        "networkx>=2.4",
        "graphviz>=0.8",
    ],
    entry_points="""
        [console_scripts]
        jiradeps=jiradeps.main:cli
    """,
)
