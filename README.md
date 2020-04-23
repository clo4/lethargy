# Lethargy: Good option parsing for your scripts

Lethargy is yet another small Python library for extracting options (and associated values) from a list of command-line arguments, specifically focused on being *perfect* for writing maintainable small to medium sized scripts. It's _extremely_ concise and unambiguous, with simple rules and great error handling.

Lethargy is completely imperative and is **not** a CLI framework. If you're building a complete CLI or _need_ automatic help commands, you're better off using **[Click]**, a truly fantastic declarative CLI framework.

[Click]: https://click.palletsprojects.com/en/7.x/
[Getting Started]: #getting-started

## Installation

You can use pip to install lethargy. It's tiny and only depends on the standard library.

```console
pip install lethargy
```

## Usage

```python
import lethargy

# Accepts the option '--bytes <int>'. Show the error nicely if it goes wrong.
with lethargy.show_errors():
    n_bytes = lethargy.take_opt('bytes', 1, int) or 8

# The option and value have now been removed from lethargy.argv
with lethargy.expect(IndexError, reason="Missing required argument: [DIR]"):
    directory = lethargy.argv[1]

...
```

## Getting Started

For simplicity, all examples assume you've got `import lethargy` at the top.

###### FLAGS

**Options can be flags.** `True` if present, `False` if not.

```python
# --debug
debug = lethargy.take_opt('debug')

print(debug)
```

```console
$ python example.py --debug
True
$ python example.py
False
```

<br>

###### NAMES

**Options can have more than one name.** Instead of a string, use a list or tuple. Names are case-sensitive.

```python
# -v|--verbose
verbose = lethargy.take_opt(['v', 'verbose'])

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
enabled = lethargy.take_opt('-Enable')
print(enabled)
```

```console
$ python example.py -Enable
True
$ python example.py
False
```

Names are _always_ case sensitive. `-Enable` **≠** `-enable`

```console
$ python example.py -enable
False
```

<hr>
</details>

###### ARGUMENTS

**Options can take arguments, too.** They can take any amount.

```python
# -o|--output <value>
output = lethargy.take_opt(['o', 'output'], 1)

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

If there are fewer values for the option than the number given, `lethargy.ArgsError` will be raised. See [Error Handling](#error-handling) for how to present this nicely.

```console
$ python example.py --output
Traceback (most recent call last):
  [...]
lethargy.errors.ArgsError: expected 1 argument for '-o|--output <value>', found none
```

<hr>
</details>

###### GREEDINESS

**Options can be variadic (greedy).** Use `...` instead of a number to take every value following the option.

```python
# -i|--ignore [value]...
ignored = lethargy.take_opt(['i', 'ignore'], ...)

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
$ ▏
```

<details>
<summary align="right">Learn more about variadic options</summary>
<br>

Because variadic options will take every argument, including values that look like other options, you should try and take these last (_after_ taking the fixed-count options).

```console
$ python example.py --ignore "*.pyc" --exceptions some.pyc
*.pyc
--exceptions
some.pyc
```

<hr>
</details>

###### UNPACKING

**Unpack multiple values into separate variables.** If the option wasn't present, they'll all be `None`.

```python
# --name <value> <value> <value>
first, middle, last = lethargy.take_opt('name', 3)

print(f'Hi, {first}!')
```

```console
$ python example.py --name Dwight Kurt Schrute
Hi, Dwight!
$ python example.py
Hi, None!
```

<br>

###### DEFAULTS

**Set sensible defaults.** Use the `or` keyword and your default value(s).

```python
# -h|--set-hours <value> <value>
start, finish = lethargy.take_opt(['set hours', 'h'], 2) or "9AM", "5PM"

print(f'Employee now works {start} to {finish}')
```

```console
$ python example.py
Employee works 9AM to 5PM
$ python example.py --set-hours 8AM 4PM
Employee works 8AM to 4PM
```

<br>

###### TYPES & CONVERSION

**Convert your option's values.** Use a function or type as the final argument. Defaults aren't converted.

```python
# --date-ymd <int> <int> <int>
y, m, d = lethargy.take_opt('date ymd', 3, int) or 1970, 1, 1

from datetime import datetime
date = datetime(y, m, d)
delta = datetime.today() - date
print(f'it has been {delta.days} days since {date}')
```

```console
$ python example.py --date-ymd 1999 10 9
it has been 7500 days since 1999-10-09 00:00:00
```

<br>

###### ERROR HANDLING

**Give clear error messages.** Lucky for you, lethargy's errors are extremely descriptive.

```python
with lethargy.show_errors():
    n_bytes = lethargy.take_opt('bytes', 1, int) or 8
    start, end = lethargy.take_opt(['r', 'range'], 2, int) or 0, 10
```

```console
$ python example.py --range 20
Expected 2 arguments for option '-r|--range <int> <int>', but found 1 ('20')
$ python example.py --bytes
Expected 1 argument for option '--bytes <int>', but found none
$ python example.py --bytes wrong
Option '--bytes <int>' received an invalid value: 'wrong'
```

<details>
<summary align="right">Learn more about error handling</summary>
<br>

Calling `fail()` will exit with status code 1. You can optionally use a message.

Lethargy provides two context managers for easier error handling. These share similar behaviour, but are separate to make intent clearer.

> <i>with</i> <code><i>lethargy.</i><b>expect(</b><i>*errors: Exception</i>, <i>reason: Optional[str] = None</i><b>)</b></code>

When one of the given exceptions is raised, it calls `fail()` to exit and print the message.

> <i>with</i> <code><i>lethargy.</i><b>show_errors()</b></code>

Same behaviour as `expect`, but specifically for exceptions from lethargy.

Note that exceptions raised during value conversions will be caught by `show_errors()`.

You can access the original exception that caused a `TransformError` with the `__cause__` attribute (see the Python [Built-in Exceptions] docs).

[Built-in Exceptions]: https://docs.python.org/3/library/exceptions.html

<hr>
</details>

## Contributing

Any and all contributions are absolutely welcome. Feel free to open an issue or just jump straight to a PR. Let's discuss and make this the best it can be! 😄

## License

Lethargy is released under the [MIT license](https://github.com/SeparateRecords/lethargy/blob/master/LICENSE).
