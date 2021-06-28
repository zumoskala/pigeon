import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="example-pkg-zuzannamoskala",
    version="0.0.2",
    author="Zuzanna Moskała",
    author_email="zuzanna.moskala@student.uw.edu.pl",
    description="A package that provides useful tools in analysing data about population and schools in Poland, "
                "according to data provided by Główny Urząd Statystyczny and System Informacji Oświatowej: "
                "Wykaz szkół i placówek wg stanu na 30.IX. 2018 r., "
                "and Ludność. Stan i struktura ludności oraz ruch naturalny w przekroju terytorialnym "
                "(stan w dniu 30.06.2020)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject", #UPDATE!
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'pandas', 'openpyxl'],
    python_requires='>=3.6',
)
