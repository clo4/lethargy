# Lethargy: Terse & tiny command-line option library

**Lethargy was born out of frustration**. It gets out of your way as soon as possible to let you get on with the actual logic. No bullshit, no magic, no objects to understand, you just call a function.

I write a lot of small scripts to get my job done faster, and manually working with options is a pain. Existing libraries are extremely verbose or just don't feel good to use. _Lethargy is designed to make writing scripts easier and faster, and to reduce effort needed to maintain them_.

<!-- Note that the spaces here are U+2000 (' ') EN QUAD -->
<!--                 v                                  -->
- **No boilerplate.** Headaches are directly proportional to lines of code.
- **No bloat.** Small API surface area, very little to learn.
- **No ambiguity.** Lethargy raises exceptions instead of getting your code into bad state.
- **Clear errors.** Great error messages and context managers for dealing with them.
- **Flexible.** You're not locked in to any styles or paradigms.

Lethargy is completely imperative and is **not** a framework. If you _are_ building a complete CLI or want automatic help commands, you're better off using **[Click]** — a fantastic, declarative CLI framework.

[Click]: https://click.palletsprojects.com/en/7.x/

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

# Now the option and value have been removed from lethargy.argv
with lethargy.expect(IndexError, reason='Missing required argument: [DIR]'):
    directory = lethargy.argv[1]

...
```

## Getting Started

This is both a tutorial and the documentation. All examples assume you've got `import lethargy` at the top.

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

**Options can have more than one name.** Instead of a string, use a list of strings. Names are case-sensitive.

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

<table><tbody><tr><td>💡</td><td>
<!-- <tip> -->
Names are created automatically (POSIX style) if the given names start with a letter or number. Names like <code>'-test'</code> and <code>'/f'</code> are treated as literal because of the first character.
<!-- </tip> -->
</td></tr></tbody></table><br>

###### ARGUMENTS

**Options can take arguments, too.** They can take any amount, and values are **always** space-separated.

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

<table><tbody><tr><td>💡</td><td>
<!-- <tip> -->
If there are fewer values than what the option takes, it'll raise <code>lethargy.ArgsError</code>. See <a href="#error-handling">Error Handling</a> for how to present error messages nicely.
<!-- </tip> -->
</td></tr></tbody></table><br>

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

<table><tbody><tr><td>💡</td><td>
<!-- <tip> -->
Variadic options are greedy and will take <b>every</b> argument that follows them, including values that look like other options. You should always try and take these last (<i>after</i> taking the fixed-count options).
<!-- </tip> -->
</td></tr></tbody></table><br>

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
start, finish = lethargy.take_opt(['set hours', 'h'], 2) or '9AM', '5PM'

print(f'Employee now works {start} to {finish}')
```

```console
$ python example.py
Employee works 9AM to 5PM
$ python example.py --set-hours 8AM 4PM
Employee works 8AM to 4PM
```

<table><tbody><tr><td>💡</td><td>
<!-- <tip> -->
You should use defaults unless your option explicitly sets <code>required=True</code>. You'll thank yourself when you need to change something 6 months from now!
<!-- </tip> -->
</td></tr></tbody></table><br>

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

**Give clear error messages.** Lethargy makes this easy with simple context managers.

```python
with lethargy.show_errors():
    x, y = lethargy.take_opt(['p', 'pos'], 2, int) or 0, 0
```

```console
$ python example.py --pos 20
Expected 2 arguments for option '-p|--pos <int> <int>', but found 1 ('20')
$ python example.py -p 20, 0
Option '-p|--pos <int> <int>' received an invalid value: '20,'
```

<details>
<summary align="right">Learn more about handling errors</summary>
<br>

Use `fail()` to exit with status code 1. You can optionally give it a message.

Lethargy provides two context managers for easier error handling. These share similar behaviour, but are separate to make intent clearer.

> <i>with</i> <code><i>lethargy.</i><b>expect(</b><i>*errors: Exception, reason: Optional[str] = None</i><b>)</b></code>

When one of the given exceptions is raised, it calls `fail()` to exit and print the message.

> <i>with</i> <code><i>lethargy.</i><b>show_errors()</b></code>

Same behaviour as `expect`, but specifically for handling options. Exceptions raised during value conversions will also be caught by `show_errors()`, with a useful message.

<table><tbody><tr><td>💡</td><td>
<!-- <tip> -->
You can access the original exception that caused a <code>TransformError</code> with the <code>__cause__</code> attribute (see the Python <a href="https://docs.python.org/3/library/exceptions.html">Built-in Exceptions</a> docs).
<!-- </tip> -->
</td></tr></tbody></table>

<hr>
</details>

## Contributing

Any and all contributions are absolutely welcome. Feel free to open an issue or just jump straight to a PR. Let's discuss and make this the best it can be! 😄

## License

Lethargy is released under the [MIT license](https://github.com/SeparateRecords/lethargy/blob/master/LICENSE).
