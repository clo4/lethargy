# Lethargy: Lazy option parsing for scripts

[![Size]][Size URL]

[Size]: https://img.shields.io/badge/size-14%20kB-blue
[Size URL]: https://github.com/SeparateRecords/lethargy/tree/master/lethargy
<!-- Size correct as at e4db57f (March 16, 2020) -->

It's not a full argument parser. If you're building a complete CLI, you're better off using the amazing library **[Click]**. Click has different design goals more suited for that use.

Lethargy takes care of **_option parsing_** in your **_scripts_**, so you can handle its arguments yourself. It's concise and explicit.

Lethargy is designed around mutating a list of arguments (`lethargy.argv` by default). This leaves you free to do whatever you want with what's left, after you've taken just the options you want. It is intended as a simple and maintainable improvement to manually parsing `sys.argv`.

[Click]: https://click.palletsprojects.com/en/7.x/

## Installation

You can use pip to install lethargy. It's tiny and only depends on the standard library.

```console
pip install lethargy
```

## Getting Started

**Options can be flags.** `True` if present, `False` if not.

```python
# --debug
debug = lethargy.flag('debug')

print(debug)
```

```console
$ python example.py --debug
True
$ python example.py
False
```

<br>

**Options can have more than one name.** Instead of a string, use a list or tuple.

```python
# -v|--verbose
verbose = lethargy.flag(['v', 'verbose'])

print(verbose)
```

```console
$ python example.py -v
True
$ python example.py --verbose
True
```

<details>
<summary align="right">Learn more about option names</summary>
<br>

Option names are automatically generated. `"use headers"` becomes `--use-headers`, and `"I"` becomes `-I`.

If you provide an explicit name (starting with a non-alphanumeric character, such as `-`, `/` or `+`), the name is stripped and treated as literal.

```python
# -Enable
enabled = lethargy.flag('-Enable')
print(enabled)
```

```console
$ python example.py -Enable
True
$ python example.py
False
```

Names are _always_ case sensitive. `-Enable` ≠ `-enable`

```console
$ python example.py -enable
False
```

<hr>
</details>

**Options can take arguments, too.** They can take any amount.

```python
# -o|--output <value>
output = lethargy.args(['o', 'output'], 1)

print(output)
```

```console
$ python example.py -o out.txt
out.txt
$ python example.py
None
```

<details>
<summary align="right">Learn more about arguments</summary>
<br>

If there are fewer values for the option than the number given, `lethargy.ArgsError` will be raised.

```console
$ python example.py --output
Traceback (most recent call last):
  [...]
lethargy.errors.ArgsError: expected 1 argument for '-o|--output <value>', found 0
```

<hr>
</details>

**Options can be variadic (greedy).** Use `...` instead of a number to take every value following the option.

```python
# -i|--ignore [value]...
ignored = lethargy.args(['i', 'ignore'], ...)

for pattern in ignored:
    print(pattern)
```

```console
$ python example.py --ignore .git .vscode .DS_Store
.git
.vscode
.DS_Store
$ python example.py --ignore experiments
experiments
$ python example.py
```

<br>

**Unpack multiple values into separate variables.** If the option wasn't present, they'll all be `None`.

```python
# --name <value> <value> <value>
first, middle, last = lethargy.args('name', 3)

print(f'Hi, {first}!')
```

```console
$ python example.py --name Dwight Kurt Schrute
Hi, Dwight!
$ python example.py
Hi, None!
```

<br>

**Set sensible defaults.** Use the `or` keyword and your default value(s).

```python
# --range <value> <value>
start, stop, step = lethargy.args('range', 2) or "2000", "2020"

print(f'finding results from {start} to {stop}...')
```

```console
$ python example.py --range 2007 2016
finding results from 2007 to 2016...
$ python example.py
finding results from 2000 to 2020...
```

<br>

**Convert your option's values.** Use a function or type as the final argument. Defaults aren't converted.

```python
# --date <int> <int> <int>
y, m, d = lethargy.args('date', 3, float) or 1970, 1, 1

from datetime import datetime
date = datetime(y, m, d)
delta = datetime.today() - date
print(f'it has been {delta.days} days since {date}')
```

```console
$ python example.py --date 1999 10 9
it has been 7500 days since 1999-10-09 00:00:00
```

<br>

## Contributing

Any and all contributions are absolutely welcome. Feel free to open an issue or just jump straight to a PR.

## License

Lethargy is released under the [MIT license](https://github.com/SeparateRecords/lethargy/blob/master/LICENSE).
