import setuptools

setuptools.setup(
    name="ec_tools",
    version="2.8",
    description="EC Tools",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=["dataclasses", "typing"],
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
