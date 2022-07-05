from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]
setup(
    name="FHIR DataFrames",
    version="0.0.1",
    description="Toolkit to handle FHIR Resources in Pandas DataFrames like real data scientists.",
    long_description=open("README.md").read(),
    url="",
    author="",
    author_email="",
    license="MIT",
    classifiers=classifiers,
    keywords="",
    packages=find_packages(),
    install_requires=["fhirkit", "pandas"],
)
