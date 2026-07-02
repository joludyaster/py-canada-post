![py-canada-post logo](https://raw.githubusercontent.com/joludyaster/py-canada-post/main/docs/assets/logo.png)

# Py-canada-post
Python written wrapper to interact with Canada Post API.

## Table of contents

- [Why was it created?](#why-was-it-created)
- [How to use?](#how-to-use)
    - [Essential steps](#essential-steps)
    - [Quick start](#quick-start)
        - [Install from PyPi](#install-from-pypi)
        - [Install from source](#install-from-source)
        - [Getting started](#getting-started)
- [CLI](#cli)
- [Roadmap](#roadmap)

## Why was it created?
There is no public Python library/wrapper to interact with Canada Post API, so an idea was born and brought to life.

## How to use?

### Essential steps:
Before you start using this wrapper, you should perform these essential steps:

1. Create a virtual environment:

    - Using python:

      ```bash
      python -m venv .venv
      source .venv/bin/activate
      ```

    - Using uv:

      ```bash
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

### Quick start

To use this wrapper, you will need 3.11+ python version and pip.

#### Install from PyPi

```commandline
pip install py-canada-post
```
or
```commandline
uv add py-canada-post
```

#### Install from source

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

#### Getting started

You could define the client object yourself:

```python
import os

from py_canada_post.client import PyCanadaPost
from py_canada_post.services.rating import Destination, DomesticDestination, ParcelCharacteristics
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
        origin_postal_code="E4M8S3",
        destination=Destination(
            domestic=DomesticDestination("T3Z1C8")
        ),
        parcel_characteristics=ParcelCharacteristics(
            weight=13.2
        )
    )
    print(rates)

if __name__ == "__main__":
    main()
```

Or you could use a shortcut:

```python
from py_canada_post.client import PyCanadaPost
from py_canada_post.services.rating import Destination, DomesticDestination, ParcelCharacteristics

def main():
    py_canada_post_client = PyCanadaPost.from_env()
    rates = py_canada_post_client.rating.rates.get_rates(
        origin_postal_code="E4M8S3",
        destination=Destination(
            domestic=DomesticDestination("T3Z1C8")
        ),
        parcel_characteristics=ParcelCharacteristics(
            weight=13.2
        )
    )
    print(rates)

if __name__ == "__main__":
    main()
```

See the [documentation](https://py-canada-post.readthedocs.io/en/latest/) to learn more.

## CLI

```commandline
Usage:
    py-canada-post [-v] [-h]
    py-canada-post rating get-rates ORIGIN-POSTAL-CODE [ARGS]
    py-canada-post rating discover-services COUNTRY-CODE [ARGS]
    py-canada-post rating get-service SERVICE-CODE [ARGS]
    
    more to come...
    
Options:
    rating          Command to contain all rating-related commands (e.g. get_rates, discover_services etc.).                                                                                                                     │
    --help (-h)     Display this message and exit.                                                                                                                                                                               │
    --version (-v)  Display application version.
```

See the [CLI documentation](https://py-canada-post.readthedocs.io/en/latest/cli/) to learn more.

## Roadmap

- [ ] [Rating](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/rating/default.jsf)
    - [x] [Get rates](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/rating/getrates/default.jsf)
    - [x] [Discover services](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/rating/getrates/discoverservices.jsf)
    - [x] [Get service](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/rating/getrates/getservices.jsf)
    - [ ] [Get option](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/rating/getrates/getoption.jsf)

- [ ] [Contract shipping](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/default.jsf)

    - [ ] Shipping service
        - [ ] [Create shipment](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/createshipment.jsf)
        - [ ] [Get shipment](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/shipment.jsf)
        - [ ] [Get artifact](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/shipmentartifact.jsf)
        - [ ] [Get shipment price](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/shipmentprice.jsf)
        - [ ] [Get shipment receipt](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/shipmentreceipt.jsf)
        - [ ] [Get shipment details](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/shipmentdetails.jsf)
        - [ ] [Get shipment public key info](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/publickeyinfo.jsf)
        - [ ] [Get groups](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/groups.jsf)
        - [ ] [Get shipments](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/shipments.jsf)
        - [ ] [Void shipment](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/voidshipment.jsf)
        - [ ] [Request shipment refund](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/shipmentrefund.jsf)

    - [ ] Manifest service
        - [ ] [Transmit shipments](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/transmitshipments.jsf)
        - [ ] [Get manifest](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/manifest.jsf)
        - [ ] [Get artifact](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/shipmentartifact.jsf)
        - [ ] [Get manifest details](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/manifestdetails.jsf)
        - [ ] [Get manifests](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/manifests.jsf)

    - [ ] Customer information services
        - [ ] [Get customer information](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/creditstatus.jsf)
        - [ ] [Get MOBO customer information](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/mobocreditstatus.jsf)

- [ ] [Non-contract shipping](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/onestepshipping/default.jsf)
    - [ ] [Create non-contract shipping](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/onestepshipping/createshipment.jsf)
    - [ ] [Get artifact](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/shipmentartifact.jsf)
    - [ ] [Get non-contract shipment receipt](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/onestepshipping/shipmentreceipt.jsf)
    - [ ] [Get non-contract shipment details](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/onestepshipping/shipmentdetails.jsf)
    - [ ] [Get non-contract shipment public key info](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/onestepshipping/publickeyinfo.jsf)
    - [ ] [Get non-contract shipments](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/onestepshipping/onestepshipments.jsf)
    - [ ] [Get non-contract shipment](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/onestepshipping/onestepshipment.jsf)
    - [ ] [Request non-contract shipment refund](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/onestepshipping/shipmentrefund.jsf)

- [ ] [Tracking](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/tracking/default.jsf)
    - [ ] [Get tracking summary](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/tracking/trackingsummary.jsf)
    - [ ] [Get tracking details](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/tracking/trackingdetails.jsf)
    - [x] [Get signature image](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/tracking/signatureimage.jsf) no longer available
    - [ ] [Get delivery confirmation certificate](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/tracking/deliveryconfirmation.jsf)

- [ ] [Find a post office](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/findpostoffice/default.jsf)
    - [ ] [Get nearest post office](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/findpostoffice/nearestpostoffice.jsf)
    - [ ] [Get post office detail](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/findpostoffice/postofficedetail.jsf)

- [ ] [Pickup](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/parcelpickup/default.jsf)
    - [ ] [Get pickup availability](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/parcelpickup/availability.jsf)
    - [ ] [Get pickup price](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/parcelpickup/pickupprice.jsf)
    - [ ] [Create pickup request](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/parcelpickup/createpickup.jsf)
    - [ ] [Get pickup request details](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/parcelpickup/pickupdetails.jsf)
    - [ ] [Update pickup request](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/parcelpickup/updatepickup.jsf)
    - [ ] [Cancel pickup request](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/parcelpickup/cancelpickup.jsf)
    - [ ] [Get pickup requests](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/parcelpickup/getpickup.jsf)

- [ ] [Returns](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/default.jsf)

    - [ ] Authorized returns
        - [ ] [Create authorized return](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/createreturn.jsf)
        - [ ] [Get artifact](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/shippingmanifest/shipmentartifact.jsf)

    - [ ] Open returns
        - [ ] [Create open return template](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/createopenreturn.jsf)
        - [ ] [Retrieve next open return artifact](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/retopenreturnartifact.jsf)
        - [ ] [Get open return template](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/getopenreturntemplate.jsf)
        - [ ] [Get open return template details](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/getopenreturntempdetails.jsf)
        - [ ] [Get open return template](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/deleteopenreturntemp.jsf)
        - [ ] [Delete open return template](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/deleteopenreturntemp.jsf)
        - [ ] [Get open return templates](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/returns/getopenreturntemplates.jsf)

