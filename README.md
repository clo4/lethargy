# $ lethargy --option-parsing-for-simple-apps▏

<p align="center">
  <a href="https://pypi.org/project/lethargy">
    <img src="https://img.shields.io/pypi/v/lethargy?color=blue" alt="Latest version on PyPI">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/lethargy" alt="Supported Python versions">
  <a href="https://github.com/SeparateRecords/lethargy/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/lethargy" alt="MIT License">
  </a>
  <a href="https://github.com/SeparateRecords/lethargy/blob/master/lethargy.py">
    <img src="https://img.shields.io/github/size/separaterecords/lethargy/lethargy.py" alt="Library size">
  </a>
</p>

*Simple scripts don't need the complexity of a full CLI framework*. Lethargy is a small and minimal library that makes it easy to only take the arguments you need, as you need them, and use the remaining arguments for whatever you want.

This library does not try to compete with other CLI libraries, but instead allow scripts and prototypes to be iterated on faster by implementing basic command line paradigms.

**You should not use Lethargy if you are building a program that has functionality centered around the command line**. Libraries such as [Click](https://click.palletsprojects.com/en/7.x/) or [Argparse](https://docs.python.org/3/library/argparse.html) are better for implementing large applicatons.

Features:

* Makes implementing basic CLI functionality fast
* Lightweight (small codebase, only depends on standard library)
* Simple, boilerplate-free and Pythonic syntax
* Support for long and short options
* Treat an option as a flag, or accept arguments
* Allows a defined or undefined number of arguments

What it doesn't do:

* Short-option group expansion (eg. `-xyz` -> `-x -y -z`)
* `=` arguments (eg. `--quotes=always`)

## Example

The program below takes an optional --debug flag, and --exclude which will greedily take every argument provided afterwards.

```python
#!/usr/bin/env python3
from lethargy import Opt, argv

DEBUG = Opt("debug").take_flag(argv)

EXCLUDED = set(Opt("exclude").takes(...).take_args(argv))

# Will only print if DEBUG is set to True
dprint = print if DEBUG else lambda *_, **__: None

# We've removed the two options this program takes, process the remaining args
# Exclude the name of the script by starting from index 1
for name in argv[1:]:
    if name not in EXCLUDED:
        dprint(name)
```

```sh
$ ./script.py --debug a b c d e f --exclude d e
script.py
a
b
c
f
```

Manually parsing the options, it's neither easily readable or maintainable, nor is it easy to make guarantees about the safety of mutating the arg list.

## Installation

Lethargy is on PyPI. Use your package manager of choice to install `lethargy`.

```sh
pip install lethargy
```

## Table of Contents

Contents

* [Usage](#usage)
  * [Creating an option](#creating)
  * [Using `str` and `repr`](#str)
  * [Taking a flag](#flags)
  * [Taking a single argument](#single-arg)
  * [Taking multiple arguments](#multiple-arg)
  * [Taking any number of arguments ("greediness")](#greedy-options)
  * [Raising instead of defaulting](#raising)
* [Recipe book](#recipes)
  * [Mandatory option with helpful error](#mandatory)

<a name="usage"></a>

## Usage

<a name="creating"></a>

### Creating an option

The `Opt` constructor takes any amount of names. These names will all be converted to --skewered-kebab-case (though it preserves capitalisation), or be prefixed with a single dash (`-`) if the name is just a single character.

```python
from lethargy import Opt

# -x or --example
Opt("x", "example")

# --option-parsing-for-simple-apps
Opt("option parsing for simple appes")
```

If the option takes arguments, use the `takes` method to set the number of arguments. This will be discussed further in the "taking arguments" sections below.

---

<a name="str"></a>

### Using `str` and `repr`

`Opt` instances have a helpful `str` and `repr`.

Converting it to a string will show its names and the number of values it takes in an easily readable way.

```python
from lethargy import Opt
print(Opt('name'))
# --name
print(Opt('f', 'files').takes(2))
# -f|--files <value> <value>
```

---

<a name="flags"></a>

### Taking a flag

A very common pattern is to extract a debug or verbose flag from the list of arguments. It's not uncommon that this may be the only option that the script accepts.

Use the `take_flag` method to remove the option from the argument list.

```python
from lethargy import Opt, argv

args = ['--debug', 'other', 'values']

DEBUG = Opt('debug').take_flag(argv)

print(DEBUG)
# True

print(args)
# ['other', 'values']
```

In this case, if --debug was present in the list, it would have been removed and the method would return True. Otherwise, it would return False and make no changes to the list.

---

<a name="single-arg"></a>

### Taking a single argument

An option that takes a single argument will return a single value.

```python
from lethargy import Opt

args = ['--example', 'value', 'floating']
val = Opt('example').takes(1).take_args(args)
no_val = Opt('abc').takes(1).take_args(args)

print(val)
# value

print(no_val)
# None

print(args)
# ['floating']

```

If an option that takes arguments is given fewer than expected, `lethargy.ArgsError` is raised. No mutation will occur.

```python
from lethargy import Opt, ArgsError

# --example is given, but the option is expecting 1 argument.
bad = ['--example']
try:
    Opt('example').takes(1).take_args(bad)
except ArgsError:
    pass

print(bad)
# ['--example']
```

---

<a name="multiple-arg"></a>

### Taking multiple arguments

When taking more than 1 argument, a list of arguments is returned.

```python
from lethargy import Opt

args = ['-', '--name', 'separate', 'records']

first, last = Opt('name').takes(2).take_args(args)

print(first, last)
# separate records

print(args)
# ['-']
```

If the option is not provided, it returns a list of None that has the correct length. This guarantees that multiple assignment is safe.

```python
from lethargy import Opt

first, last = Opt('name').takes(2).take_args([])

print(first, last)
# None None
```

If the default is specified using the `default` parameter (eg. `take_args(args, default=''`), it will be returned as-is.

---

<a name="greedy-options"></a>

### Taking any number of arguments ("greediness")

If the number of arguments the option takes is `...`, the option will greedily consume each argument remaining in the list after the option name.

```python
from lethargy import Opt

args = ['script.py', '-f', 'a', 'b', 'c', '--files', 'd']

values = Opt('f', 'files').takes(...).take_args(args)
print(values)
# ['a', 'b', 'c', '--files', 'd']

print(args)
# ['script.py']
```

These options should be taken last to avoid accidentally eating another option.

By default, an empty list is returned if there are no arguments provided.

```python
values = Opt('x').takes(...).take_args([])
print(values)
# []
```

---

<a name="raising"></a>

### Raising instead of defaulting

By setting `raises=True` in the `take_args` method call, `lethargy.MissingOption` will be raised instead of returning the default.

<a name="recipes"></a>

## Recipe book

Some common patterns used for basic CLI scripts. Anything more complex than these could be done better using Click or Argparse.

---

<a name="mandatory"></a>

### Mandatory option with helpful error

This example shows how you would combine raising instead of defaulting and the string formatting of an `Opt` instance.

```python
from lethargy import Opt, argv, MissingOption

opt = Opt('my option').takes(2)

try:
    args = opt.take_args(argv, raises=True)
except MissingOption:
    print(f'Missing required option: {opt}')
    exit(1)
```
