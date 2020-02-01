from setuptools import setup, find_packages

with open("./README.md", encoding="utf-8") as f:
    LONG_DESC = "\n" + f.read()

CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
    "Environment :: Console",
    "Intended Audience :: Developers",
]


setup(
    name="gputree",
    version="0.1.0",
    description="Remote GPUs Monitoring.",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author="Thomas Le Meur",
    author_email="thmslmr@gmail.com",
    url="https://github.com/thmslmr/gputree",
    license="MIT",
    classifiers=CLASSIFIERS,
    python_requires=">=3.5.0",
    install_requires=["asyncssh", "blessings", "pyyaml"],
    extras_require={},
    packages=find_packages(),
    entry_points={"console_scripts": ["gputree=gputree.cli:main"]},
    include_package_data=True,
)
