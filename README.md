# $ lethargy --option-parsing-for-simple-apps▏

```python
#!/usr/bin/env python3
from lethargy import Opt, argv

your_app = Opt('option parsing for simple apps').takes(1).take_args(argv)
```

A little library that provides you with the tools to make CLI option parsing easy.

**Features:**

* Focuses on smaller abstractions and utilities
* Lightweight (small codebase, only depends on standard library)
* Simple, boilerplate-free and Pythonic syntax

## Installation

Use your package manager of choice to install `lethargy`.

```sh
pip install lethargy
```
