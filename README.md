# mm-jinja

Pre-configured Jinja2 environment with useful filters and globals.

## Usage

```python
from jinja2 import FileSystemLoader
from mm_jinja import init_jinja

env = init_jinja(loader=FileSystemLoader("templates/"))
template = env.get_template("example.html")
result = template.render(data={"count": 1500, "created": datetime.now()})
```

With custom filters/globals and async support:

```python
env = init_jinja(
    loader=FileSystemLoader("templates/"),
    custom_filters={"my_filter": my_filter_func},
    custom_globals={"my_var": my_value},
    enable_async=True,
)
```

## Built-in Filters

| Filter | Alias | Description |
|--------|-------|-------------|
| `timestamp` | `dt` | Format datetime or unix timestamp |
| `nformat` | `n` | Format numbers with prefix, suffix, separators |
| `yes_no` | - | Format boolean as colored HTML |
| `empty` | - | Return empty string for None/empty values |
| `to_json` | - | Encode dict as JSON string |

## Built-in Globals

| Global | Description |
|--------|-------------|
| `utc()` | Current UTC datetime |
| `raise(msg)` | Raise RuntimeError from template |
