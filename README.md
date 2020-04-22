# Lethargy: Good option parsing for your scripts

[![Size]][Size URL]

[Size]: https://img.shields.io/badge/size-14%20kB-blue
[Size URL]: https://github.com/SeparateRecords/lethargy/tree/master/lethargy
<!-- Size correct as at e4db57f (March 16, 2020) -->

It's not a full argument parser. If you're building a complete CLI, you're better off using the amazing library **[Click]**. Click has different design goals more suited for that use.

Lethargy is yet another small library for extracting options from a list of command-line arguments. It's specifically **_designed for use in your scripts_** as a maintainable and _good_ alternative to manually extracting options (flags and values) from `sys.argv`.

Lethargy uses its own copy of the arguments (`lethargy.argv`) and mutates that, unless you explicitly tell it not to.

[Click]: https://click.palletsprojects.com/en/7.x/

## Installation

You can use pip to install lethargy. It's tiny and only depends on the standard library.

```console
pip install lethargy
```

## Usage

```python
import lethargy

# --bytes <int>
n_bytes = lethargy.take('bytes', 1, int) or 8

# After removing --bytes and its value from argv, the dir should be first.
directory = lethargy.argv[1]

...
```

That's an excerpt from a script I wrote for my job.

<details>
<summary>Show this example done manually</summary>
<br>

Done manually, there's a lot of detail that's not relevant to the actual script.
* What happens if the option isn't present?
* What happens if it is but has no value?
* What about if that value isn't an int?
* How do you communicate what went wrong?

All these implementation details increase the maintenance and complexity. This shouldn't be handled by _you_.

```python
import sys

try:
    index = sys.argv.index("--bytes")
    try:
        n_bytes = int(sys.argv[index + 1])
    except IndexError:
        sys.exit(1)
    del sys.argv[index : index + 2]
except ValueError:
    n_bytes = 8

# After removing --bytes and its value from argv, the dir should be first.
directory = sys.argv[1]

...
```

<hr>
</details>

<details>
<summary>Show this example using Click</summary>
<br>

Click _forces you into a specific style_ that just isn't great for some scripts. It requires a lot of boilerplate, and while you get a lot for free from that, it's also more to maintain and detracts from the script's _actual_ logic.

```python
import click

@click.command()
@click.option('--bytes', default=8)
@click.argument('directory')
def cli(bytes, directory):
    ...

if __name__ == '__main__':
    cli()
```

<hr>
</details>

## Getting Started

For simplicity, all examples assume you've got `import lethargy` at the top.

<br>

**Options can be flags.** `True` if present, `False` if not.

```python
# --debug
debug = lethargy.take('debug')

print(debug)
```

```console
$ python example.py --debug
True
$ python example.py
False
```

<br>

**Options can have more than one name.** Instead of a string, use a list or tuple. Names are case-sensitive.

```python
# -v|--verbose
verbose = lethargy.take(['v', 'verbose'])

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
enabled = lethargy.take('-Enable')
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

**Options can take arguments, too.** They can take any amount.

```python
# -o|--output <value>
output = lethargy.take(['o', 'output'], 1)

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
lethargy.errors.ArgsError: expected 1 argument for '-o|--output <value>', found none
```

<hr>
</details>

**Options can be variadic (greedy).** Use `...` instead of a number to take every value following the option.

```python
# -i|--ignore [value]...
ignored = lethargy.take(['i', 'ignore'], ...)

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

**Unpack multiple values into separate variables.** If the option wasn't present, they'll all be `None`.

```python
# --name <value> <value> <value>
first, middle, last = lethargy.take('name', 3)

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
# -h|--set-hours <value> <value>
start, finish = lethargy.take(['set hours', 'h'], 2) or "9AM", "5PM"

print(f'Employee now works {start} to {finish}')
```

```console
$ python example.py
Employee works 9AM to 5PM
$ python example.py --set-hours 8AM 4PM
Employee works 8AM to 4PM
```

<br>

**Convert your option's values.** Use a function or type as the final argument. Defaults aren't converted.

```python
# --date-ymd <int> <int> <int>
y, m, d = lethargy.take('date ymd', 3, int) or 1970, 1, 1

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

**Give clear error messages.** Lucky for you, lethargy's errors are great by default. Just add 1 extra line!

```python
with lethargy.show_errors():
    n_bytes = lethargy.take('bytes', 1, int) or 8
    start, end = lethargy.take(['r', 'range'], 2, int) or 0, 10
    files = lethargy.argv[1:]
```

<details>
<summary align="right">Learn more about error handling</summary>
<br>

Lethargy provides two context managers for easy error handling. These share similar behaviour, but are separate to make the intent more clear.

> <i>with</i> <code><i>lethargy.</i><b>show_errors()</b></code>

Shows any errors in option parsing to the user and exits with code 1.

> <i>with</i> <code><i>lethargy.</i><b>fail_on(</b><i>*errors</i><b>)</b></code>

Fails on the first raise of one of the given errors, printing it to stderr and exiting with code 1.

These context managers can be used together. Here's the example from [Usage](#usage), but with just 1 extra line for better error handling.

```python
with lethargy.show_errors(), lethargy.fail_on(IndexError, ValueError):
    n_bytes = lethargy.take('bytes', 1, int) or 8
    directory = lethargy.argv[1]
```

<hr>
</details>

## Contributing

Any and all contributions are absolutely welcome. Feel free to open an issue or just jump straight to a PR. Let's discuss and make this the best it can be! 😄

## License

Lethargy is released under the [MIT license](https://github.com/SeparateRecords/lethargy/blob/master/LICENSE).
