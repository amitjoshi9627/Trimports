from setuptools import setup, find_packages

setup(
    name="trimports",
    version="0.1.2",
    description=(
        "A python class which automatically removes unused imports from your Python script."
    ),
    long_description=open("README.rst").read() + "\n\n" + open("CHANGELOG.txt").read(),
    url="https://github.com/amitjoshi9627/trimports",
    license="MIT",
    author="Amit Joshi",
    author_email="amitjoshi9627@gmail.com",
    keywords="unused imports",
    packages=find_packages(),
    install_requires=[""],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "trimports = Trimports.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
