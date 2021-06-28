#Pigeon Package

Pigeon Package is a Python package that provides useful tools in analysing data about population and schools in Poland, according to data provided by Główny Urząd Statystyczny and System Informacji Oświatowej:
* Wykaz szkół i placówek wg stanu na 30.IX. 2018 r.
* Ludność. Stan i struktura ludności oraz ruch naturalny w przekroju terytorialnym (stan w dniu 30.06.2020)

## Main Features

Pigeon Package allows for loading and calculating basic statistics of aforementioned data. Main features are:
* load excel files and clean empty columns
* load files of multiple sheets and concatenate them into one dataframe
* calculate basic statistics like mean, minimum and maximum

## Where to get it
Install through PyPI:
```angular2html
pip install pigeon-schooldata-package
```

##Dependencies
* NumPy
* Pandas