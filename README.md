# pypicoip
A python library for communicating with PicoIP


[PicoIP](https://lan.neomontana-bg.com/doc/pdf/PicoIP-Bg.pdf)

```sh
python -m pip install --upgrade git+https://github.com/orlin369/pypicoip.git#egg=pypicoip
```

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin
[0, 0, 0, 66, 99, 91, 301, 485, 441, 385, 261]
```

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin --p3 255
[255, 0, 0, 295, 20, 55, 82, 77, 241, 464, 387]
```

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin --p5 255
[255, 0, 0, 295, 20, 55, 82, 77, 241, 464, 387]
```

```sh
python -m pypicoip --host http://172.16.100.2 --user admin --password admin --p3 255 --p5 255
[255, 255, 0, 86, 100, 153, 456, 526, 403, 355, 156]
```
