# Lethargy - Option parsing, for simple apps

[![Released version](https://img.shields.io/pypi/v/lethargy?color=blue)](https://pypi.org/project/lethargy)
[![Python versions](https://img.shields.io/pypi/pyversions/lethargy)](https://python.org)
[![MIT License](https://img.shields.io/pypi/l/lethargy)](https://github.com/SeparateRecords/lethargy/blob/master/LICENSE)
[![Size](https://img.shields.io/github/size/separaterecords/lethargy/lethargy.py)](https://github.com/SeparateRecords/lethargy/blob/master/lethargy.py)

Lethargy takes care of option parsing in your scripts, so you can be more productive when writing the important stuff. It's simple, concise, explicit, and Pythonic.

Unlike [Click](https://click.palletsprojects.com/en/7.x/) and [Argparse](https://docs.python.org/3/library/argparse.html), Lethargy is succinct, can be implemented without changing the structure of a program, and requires no boilerplate code. This makes it especially suited to scripting and prototyping.

By design, it is not a full argument parser. If you're building a complete CLI application, you're probably better off using Click.

<a name="installation"></a>

## Installation

Lethargy only depends on the standard library. You can use [pip](https://pip.pypa.io/en/stable/) to install lethargy.

```bash
pip install lethargy
```

<a name="usage"></a>

## Usage

```python
from lethargy import Opt, argv

# --use-headers
headers = Opt("use headers").take_flag(argv)

# -f|--file <value>
output_file = Opt("f", "file").takes(1).take_args(argv)
```

Lethargy returns values appropriate to the option, safely mutating the list.

<a name="getting-started"></a>

## Getting Started

<a name="argv"></a>

### The default `argv`

To save you an additional import, lethargy provides `lethargy.argv` - a clone of the original argument list. Mutating it will not affect `sys.argv`.

<a name="options"></a>

### Options

Options will automatically convert their names to the appropriate format (`-o` or `--option`). Casing will be preserved.

```python
>>> from lethargy import Opt
>>> args = ["-", "--debug", "file.txt"]
>>> Opt("debug").take_flag(args)
True
>>> args
["script.py", "file.txt"]
```

To take arguments, use the `Opt.takes` method.

```python
>>> args = ["-", "--height", "185cm"]
>>> Opt("height").takes(1).take_args(args)
'185cm'
>>> args
["script.py"]
```

Taking 1 argument will return a single value. Taking multiple will return a list (see the [Argument unpacking](#unpacking) section for details).

You can also use a "greedy" value, to take every remaining argument. The canonical way to do this is using the Ellipsis literal (`...`).

```python
>>> args = []
>>> Opt("exclude").takes(...).take_args(args)
```

<a name="unpacking"></a>

### Argument unpacking

`lethargy.Opt` makes sure it's safe to unpack a returned list of values, unless you override the `default` parameter.

```python
>>> Opt("x").takes(2).take_args(["-x", "1", "2"])
["1", "2"]
>>> Opt("y").takes(2).take_args([])
[None, None]
```

If there are fewer arguments than expected, `lethargy.ArgsError` will be raised and no mutation will occur. Lethargy has clear and readable error messages.

```python
>>> args = ["-z", "bad"]
>>> Opt("z").takes(2).take_args(args)
Traceback (most recent call last):
...
lethargy.ArgsError: expected 2 arguments for '-z <value> <value>', found 1 ('bad')
>>> args
["-z", "bad"]
```

<a name="debug-and-verbose"></a>

### `--debug` and `-v`/`--verbose`

As these are such common options, lethargy provides functions to take these by default.

```python
>>> from lethargy import take_debug, take_verbose
>>> args = ["script.py", "--debug", "--verbose", "sheet.csv"]
>>> take_verbose(args)  # -v or --verbose
True
>>> take_debug(args)
True
>>> args
["script.py", "sheet.csv"]
```

By convention, passing `--verbose` will cause a program to output more information. To make implementing this behaviour easier, lethargy has the `print_if` function, which will return `print` if its input is true and a dumb function if not.

```python
from lethargy import take_verbose, print_if, argv

debug_print = print_if(take_verbose(argv))
```

<a name="str-and-repr"></a>

### Using `str` and `repr`

`Opt` instances provide a logical and consistent string form.

```python
>>> str(Opt("flag"))
'--flag'
>>> str(Opt("e", "example").takes(1))
'-e|--example <value>'
>>> str(Opt("e", "example").takes(...))
'--xyz [value]...'
```

The `repr` form makes debugging easy. Note that the order of the names is not guaranteed.

```python
>>> Opt("f", "flag")
<Opt('flag', 'f').takes(0)>
```

<a name="raising"></a>

### Raising instead of defaulting

If `Opt.take_args` is called with `raises=True`, `lethargy.MissingOption` will be raised instead of returning a default, even if the default is set explicitly.

This behaviour makes it easy to create a required option.

```python
from lethargy import Opt, argv, MissingOption

opt = Opt('example').takes(1)

try:
    value = opt.take_args(argv, raises=True)
except MissingOption:
    print(f'Missing required option: {opt}')
    exit(1)
```

<a name="contributing"></a>

## Contributing

Any contributions and feedback are welcome! I'd appreciate it if you could open an issue to discuss changes before submitting a PR, but it's not enforced.

<a name="license"></a>

## License

Lethargy is released under the [MIT license](https://github.com/SeparateRecords/lethargy/blob/master/LICENSE).
