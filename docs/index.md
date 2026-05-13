![py-canada-post logo](assets/logo.png)

# Py-canada-post
Python written wrapper to interact with Canada Post API.

## Why was it created?
There is no public Python library/wrapper to interact with Canada Post API, so an idea was born and brought to life.

## Getting started

```python
from py_canada_post.client import PyCanadaPost
from py_canada_post.services.rating import Destination, DomesticDestination

def main():
    py_canada_post_client = PyCanadaPost.from_env()
    rates = py_canada_post_client.rating.rates.get_rates(
        "E4M8S3",
        Destination(
            domestic=DomesticDestination("T3Z1C8")
        )
    )
    print(rates)

if __name__ == "__main__":
    main()
```

See the [how to use](https://py-canada-post.readthedocs.io/en/latest/how-to-use/) guide to learn more.

## CLI

```commandline
Usage:
    py-canada-post [-v] [-h]
    py-canada-post rating get-rates ORIGIN-POSTAL-CODE [ARGS]
    py-canada-post rating discover-services COUNTRY-CODE [ARGS]
    
    more to come...
    
Options:
    rating          Command to contain all rating-related commands (e.g. get_rates, discover_services etc.).                                                                                                                     │
    --help (-h)     Display this message and exit.                                                                                                                                                                               │
    --version (-v)  Display application version.
```

See the [CLI documentation](https://py-canada-post.readthedocs.io/en/latest/cli/) to learn more.