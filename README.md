# pypicoip
A python library for communicating with PicoIP

# Description

The library is dedicated to communicate with PicoIP device via HTTP interface.
Main goal to create this library is to make this device to be part of home automation and small automation projects written mainly in python.

This is the documentation of the device with version (4.094)
[PicoIP v1](https://lan.neomontana-bg.com/picoip.php)

This is the documentation of the device with version (2.2)
[PicoIP v2](https://lan.neomontana-bg.com/picoipv2.php)

Red this document to understand how device is operating.

# Installation

## Environment

 - For better experience is good to have git client. This will will alow you to install easy from github this library. The link to the [git client](https://git-scm.com/download/win).

 - This script is written in Python 3.8.5. To [download](https://www.python.org/downloads/) it please visit official site of the Python and download [3.8.5](https://www.python.org/ftp/python/3.8.5/python-3.8.5.exe)


## Create a virtual environment (Optional)
 - Make virtual environment
```sh
python -m venv venv
```

 - For Windows machines
```sh
venv/bin/activate.ps1
```
 - For Linux or macOS machines:
```sh
source venv/bin/activate
```

## Update the environment
 - Update the pip system
```bash
python -m pip install --upgrade pip 
```

## Install the library
 - Install the repository from link
```sh
python -m pip install --upgrade git+https://github.com/orlin369/pypicoip.git#egg=pypicoip
```
 - You are ready for the first run.

## Install the library manually (optional)
 - Download the repository from [link](git+https://github.com/robko01/app_python3)

 - Install setuptools
```sh
python -m pip install setuptools
```

 - Unzip the downloaded repo.
 - Navigate to the unziped folder in terminal.
 - Install the package
```sh
python setup.py install
```
 - You are ready for the first run.

## First run
After installation, the script is ready for operation. This happens in the following way.

 - For Windows machines:

Only read information for the IO.

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin
[0, 0, 0, 66, 99, 91, 301, 485, 441, 385, 261]
```

Set port P3 to 255.

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin --p3 255
[255, 0, 0, 295, 20, 55, 82, 77, 241, 464, 387]
```

Set port P5 to 255.

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin --p5 255
[255, 0, 0, 295, 20, 55, 82, 77, 241, 464, 387]
```

Set port P3 to 255 and port P5 to 255.

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin --p3 255 --p5 255
[255, 255, 0, 86, 100, 153, 456, 526, 403, 355, 156]
```

 - For Linux machines:

Only read information for the IO.

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin
[0, 0, 0, 66, 99, 91, 301, 485, 441, 385, 261]
```

Set port P3 to 255.

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin --p3 255
[255, 0, 0, 295, 20, 55, 82, 77, 241, 464, 387]
```

Set port P5 to 255.

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin --p5 255
[255, 0, 0, 295, 20, 55, 82, 77, 241, 464, 387]
```

Set port P3 to 255 and port P5 to 255.

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin --p3 255 --p5 255
[255, 255, 0, 86, 100, 153, 456, 526, 403, 355, 156]
```

# Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your changes: `git checkout -b my-new-feature`.
4. Make your modifications and write tests if applicable.
5. Commit your changes: `git commit -am 'Add some feature'`.
6. Push the branch to your forked repository: `git push origin my-new-feature`.
7. Create a pull request on the main repository.

We appreciate your contributions!

# License

This project is licensed under the MIT License. See the [MIT](https://choosealicense.com/licenses/mit/) file for more details.
