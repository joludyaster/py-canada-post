# Py-Canada-Post
Python written library to interact with Canada Post API Rest. Contributions are open.

## How to run?
To run this project, first create a repository:
```commandline
git clone https://github.com/joludyaster/py-canada-post.git
```

Create a virtual environment and activate it:
```commandline
python -m venv .venv
source ./.venv/bin/activate
```

Install uv:
```commandline
pip install uv
```

Sync with the packages:
```commandline
uv sync
```

Run tests:
```commandline
pytest
```
Or just Right Click on the file and hit "Run test_rates"

## Where to get credentials?
To test this app, you will need some test credentials. You can get them [here](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/fundamentals.jsf)

Put them in your `.env` files afterwards:

```python
CUSTOMER_NUMBER=12345667
CONTRACT_ID=12344556
API_KEY_SANDBOX=ewfghui34hto34ghui34g:ewghui234h23oih34uigh423
```