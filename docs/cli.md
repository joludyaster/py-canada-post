# CLI

Here there will be overviews of available CLI commands.

## Rating

Here there will be overviews of the CLI commands that are combined in 
the [rating](https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/services/rating/default.jsf) block on Canada Post API.

### Get rates CLI

If you want to know meaning if each command, visit [here](https://py-canada-post.readthedocs.io/en/latest/usage/#py_canada_post.services.rating.operations.get_rates.GetRates.get_rates).

#### Usage

```commandline
py-canada-post rating get-rates \
    -o E4M8S3 \
    -d.domestic.postal_code T3Z1C8 \
    -p GH34SAD \
    -q commercial \
    -m 2026-04-18 \
    -O SO 13.4 COV 14.5 \
    -c.weight 14.5 \
    -c.dimensions.length 20 \
    -c.dimensions.width 20 \
    -c.dimensions.height 20 \
    -u \
    -t \
    -z \
    -s DOM.RP DOM.EP
```

#### Parameters

| Parameter                        | Type                    | Default      |
|----------------------------------|-------------------------|--------------|
| `--origin-postal-code`, `-o`     | `str`                   | *required*   |
| `--destination`, `-d`            | `Destination`           | *required*   |
| `--promo-code`, `-p`             | `str`                   | `None`       |
| `--quote-type`, `-q`             | `commercial/counter`    | `commercial` |
| `--expected-mailing-date`, `-m`  | `datetime`              | `None`       |
| `--options`, `-O`                | `list[Option]`          | `None`       |
| `--parcel-characteristics`, `-c` | `ParcelCharacteristics` | `None`       |
| `--unpackaged`, `-u`             | `bool`                  | `False`      |
| `--mailing-tube`, `-t`           | `bool`                  | `False`      |
| `--oversized`, `-z`              | `bool`                  | `False`      |          
| `--services`, `-s`               | `list[Service]`         | `None`       |

#### Examples


Output (rates change all the time, you might see different rates when you perform the command):

```commandline
py-canada-post rating get-rates \
    -o E4M8S3 \
    -d.domestic.postal_code T3Z1C8 \
    -p GH34SAD \
    -q commercial \
    -O SO 13.4 COV 14.5 \    
    -c.weight 14.5 \         
    -c.dimensions.length 20 \
    -c.dimensions.width 20 \ 
    -c.dimensions.height 20 \
    -s DOM.RP DOM.EP
```

```bash
[
    Rate(
        base=41.61,
        due=63.97,
        adjustments=[Adjustment(code='FUELSC', cost=14.56, name='Fuel surcharge', percentage_rate=35)],
        options=[
            OptionDetails(code='COV', name='Coverage', price=2.75, included=None),
            OptionDetails(code='SO', name='Signature option', price=2, included=None),
            OptionDetails(code='DC', name='Delivery confirmation', price=0, included=True)
        ],
        taxes=Tax(gst=TaxDetails(price=3.05, percentage_rate=5), hst=TaxDetails(price=0, percentage_rate=0), pst=TaxDetails(price=0, percentage_rate=0)),
        service=Service(code='DOM.RP', name='Regular Parcel', am_delivery=False, expected_delivery_date=datetime.datetime(2026, 5, 22, 0, 0), expected_transit_time=8, guaranteed_delivery=False)
    ),
    Rate(
        base=41.61,
        due=61.08,
        adjustments=[Adjustment(code='FUELSC', cost=14.56, name='Fuel surcharge', percentage_rate=35)],
        options=[
            OptionDetails(code='COV', name='Coverage', price=0, included=True),
            OptionDetails(code='SO', name='Signature option', price=2, included=None),
            OptionDetails(code='DC', name='Delivery confirmation', price=0, included=True)
        ],
        taxes=Tax(gst=TaxDetails(price=2.91, percentage_rate=5), hst=TaxDetails(price=0, percentage_rate=0), pst=TaxDetails(price=0, percentage_rate=0)),
        service=Service(code='DOM.EP', name='Expedited Parcel', am_delivery=False, expected_delivery_date=datetime.datetime(2026, 5, 20, 0, 0), expected_transit_time=6, guaranteed_delivery=True)
    )
]
```

### Discover services CLI

If you want to know meaning if each command, visit [here](https://py-canada-post.readthedocs.io/en/latest/usage/#py_canada_post.services.rating.operations.discover_services.DiscoverServices.discover_services).

#### Usage:

```commandline
py-canada-post rating discover-services \
    -c CA
    -o E4M8S3
    -d T3Z1C8
```

| Parameter                         | Type                    | Default    |
|-----------------------------------|-------------------------|------------|
| `--country-code`, `-c`            | `str`                   | *required* |
| `--origin-postal-code`, `-o`      | `str`                   | `None`     |
| `--destination-postal-code`, `-d` | `str`                   | `None`     |

#### Examples:

Output (services etc. change all the time, you might see different services when you perform the command):

```commandline
py-canada-post rating discover services \
    -c CA
    -o E4M8S3
    -d T3Z1C8
```

```bash
[
    Service(code='DOM.EP', name='Expedited Parcel', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None),
    Service(code='DOM.EP.EPLUS', name='Expedited Parcel Plus', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None),
    Service(code='DOM.RP', name='Regular Parcel', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None),
    Service(code='DOM.PC', name='Priority', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None),
    Service(code='DOM.XP', name='Xpresspost', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None),
    Service(code='DOM.XP.CERT', name='Xpresspost Certified', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None),
    Service(code='DOM.LIB', name='Library Materials', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None)
]
```

```commandline
py-canada-post rating discover services -c JP
```

```bash
[
    Service(code='INT.XP', name='Xpresspost International', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None),
    Service(code='INT.IP.SURF', name='International Parcel Surface', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None),
    Service(code='INT.TP', name='Tracked Packet - International', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None),
    Service(code='INT.SP.SURF', name='Small Packet International Surface', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None),
    Service(code='INT.SP.AIR', name='Small Packet International Air', am_delivery=None, expected_delivery_date=None, expected_transit_time=None, guaranteed_delivery=None)
]
```

### Get service CLI

If you want to know meaning if each command, visit [here](https://py-canada-post.readthedocs.io/en/latest/usage/#py_canada_post.services.rating.operations.get_service.GetService.get_service).

#### Usage:

```commandline
py-canada-post rating get-service \
    -s INT.XP
    -c JP
```

| Parameter                         | Type                    | Default    |
|-----------------------------------|-------------------------|------------|
| `--service-code`, `-s`            | `str`                   | *required* |
| `--country-code`, `-c`            | `str`                   | `None`     |

#### Examples:

Output (service data etc. change all the time, you might see different service data when you perform the command):

```commandline
py-canada-post rating get-service \
    -s INT.XP
    -c JP
```

```bash
Service(
    service_code='INT.XP',
    service_name='Xpresspost International',
    am_delivery=None,
    expected_delivery_date=None,
    expected_transit_time=None,
    guaranteed_delivery=None,
    comment=None,
    options=[
        Option(option_code='COV', option_amount=None, price=None, included=None, option_name='Coverage', mandatory=False, qualifier_required=True, qualifier_max=5000),
        Option(option_code='SO', option_amount=None, price=None, included=None, option_name='Signature option', mandatory=True, qualifier_required=False, qualifier_max=None),
        Option(option_code='DC', option_amount=None, price=None, included=None, option_name='Delivery confirmation', mandatory=True, qualifier_required=False, qualifier_max=None),
        Option(option_code='RASE', option_amount=None, price=None, included=None, option_name="Return at sender's expense", mandatory=True, qualifier_required=False, qualifier_max=None),
        Option(option_code='ABAN', option_amount=None, price=None, included=None, option_name='Abandon', mandatory=True, qualifier_required=False, qualifier_max=None)
    ],
    restrictions=Restrictions(
        weight_restriction=AttributeRestriction(min_value=0, max_value=30000),
        dimensional_restrictions=DimensionalRestrictions(
            length=AttributeRestriction(min_value=None, max_value=150),
            width=AttributeRestriction(min_value=None, max_value=150),
            height=AttributeRestriction(min_value=None, max_value=150),
            length_plus_girth_max=300,
            length_height_width_sum_max=None,
            oversize_limit=100
        ),
        density_factor=5000,
        can_ship_in_mailing_tube=True,
        can_ship_unpackaged=False,
        allowed_as_return_service=False
    )
)
```