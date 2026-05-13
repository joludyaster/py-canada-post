# How to use?

## Essential steps:
Before you start using this wrapper, you should perform these essential steps:

1. Create a virtual environment:

    - Using python:

      ```commandline
      python -m venv .venv
      source .venv/bin/activate
      ```

    - Using uv:

      ```commandline
      uv python pin 3.11
      uv init
      uv sync
      ```

2. Create .env and put your customer number, contract id and api key in there as followed:
    
    ```python
    CUSTOMER_NUMBER=12345667
    CONTRACT_ID=12344556
    API_KEY=ewfghui34hto34ghui34g:ewghui234h23oih34uigh423
    ```
   
    To test this app, you will need some test credentials. You can get
them [here](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/fundamentals.jsf).

    If you would like to obtain your own, you can register your [business](https://sso-osu.canadapost-postescanada.ca/pfe-pap/en/registration) and [join the Developer Program](https://www.canadapost-postescanada.ca/information/app/drc/home?execution=e2s1). 

## Quick start

To use this wrapper, you will need 3.11+ python version and pip.

### Install from PyPi

```commandline
pip install py-canada-post
```
or
```commandline
uv add py-canada-post
```

### Install from source

1. Clone the repository:
   
   ```commandline
   git clone https://github.com/joludyaster/py-canada-post.git
   ```

2. Run:
    
   ```commandline
   pip install .
   ```
   or
   ```commandline
   uv pip install .
   ```

### Getting started

You could define the client object yourself:

```python
import os

from py_canada_post.client import PyCanadaPost
from py_canada_post.services.rating import Destination, DomesticDestination
from dotenv import load_dotenv

load_dotenv()

customer_number = os.getenv("CUSTOMER_NUMBER", 0)
api_key = os.getenv("API_KEY", "")
contract_id = os.getenv("CONTRACT_ID", 0)

def main():
    py_canada_post_client = PyCanadaPost(
        customer_number=customer_number,
        api_key=api_key,
        contract_id=contract_id
    )
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

Or you could use a shortcut:

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

See [usage documentation](https://py-canada-post.readthedocs.io/en/latest/usage/) to learn more about the commands.