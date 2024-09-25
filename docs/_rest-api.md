# RESTful API

## Get System Maintenance Status (Public)

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/system_info
`

For fetch system status to check if system is down or under maintenance.

> **Response**

```js

{ 
    // functioning properly
    "success":true,
    "data":
        {
            "status":0,
            "msg":"System is functioning properly."
        },
    "timestamp":1676335013700
}
{   
    // trading maintenance
    "success":true,
    "data":
        {
            "status":1,
            "msg":"Under trading maintenance."
        },
    "timestamp":1676335013700
}

{   
    // system maintenance
    "success":true,
    "data":
        {
            "status":2,
            "msg":"Under system maintenance."
        },
    "timestamp":1676335013700
}
```

**Parameters**

None

## Exchange Information

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/info/:symbol
`

Get send order requirement by symbol, there are some rules need to be fullfilled in order to successfully send order, which are defined as follows:

Price filter

- `price` >= `quote_min`
- `price` <= `quote_max`
- `(price - quote_min) % quote_tick` should equal to zero
- `price` <= `asks[0].price * (1 + price_range)` when BUY
- `price` >= `bids[0].price * (1 - price_range)` when SELL

Size filter

- `base_min` <= `quantity` <= `base_max`
- `(quantity - base_min) % base_tick` should equal to zero

Min Notional filter

- `price * quantity` should greater than `min_notional`

Risk Exposure filer

- For margin trading, the margin rate should exceed a certain threshold as per leverage. For spot trading, the order size should be within the holding threshold. See [account_info](#get-account-information)

> **Response**

```js
{
    "success":true,
    "info":{
        "symbol":"PERP_ETH_USDT",
        "quote_min":0,
        "quote_max":10000,
        "quote_tick":0.01,
        "base_min":0.001,
        "base_max":4000,
        "base_tick":0.001,
        "min_notional":0,
        "price_range":0.03,
        "price_scope":0.4,
        "created_time":"1647838759.000",
        "updated_time":"1693437961.000",
        "is_stable":0,
        "is_trading":1,
        "precisions":[1,10,50,100,1000,10000],
        "is_prediction":0,
        "base_mmr":0.012,
        "base_imr":0.02
    }
}
```

**Parameters**

| Name   | Type   | Required | Description |
| ------ | ------ | -------- | ----------- |
| symbol | string | Y        |             |


## Available Symbols (Public)

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/info
`

Get the available symbols that WOO X supports, and also send order rules for each symbol. The definition of rules can be found at [Exchange Infomation](#exchange-information)

> **Response**

```js
{
  "success": true,
  "rows": [
    {
      "created_time": "1575441595.65", // Unix epoch time in seconds
      "updated_time": "1575441595.65", // Unix epoch time in seconds
      "symbol": "SPOT_BTC_USDT",
      "quote_min": 100,
      "quote_max": 100000,
      "quote_tick": 0.01,
      "base_min": 0.0001,
      "base_max": 20,
      "base_tick": 0.0001,
      "min_notional": 0.02,
      "price_range": 0.99,
      "price_scope": 0.01,
      "precisions":[1,10,100,500,1000,10000]
    },
    // ...
  ]
}
```

**Parameters**

None


## Market Trades (Public)

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/market_trades
`

Get latest market trades. The response output "source" 1=internal (trade on WOO X), 0=external (trade from aggregrated sources)

> **Response**

```js
{
    "success": true,
    "rows": [
        {
            "symbol": "SPOT_ETH_USDT",
            "side": "BUY",
            "source": 0,
            "executed_price": 202,
            "executed_quantity": 0.00025,
            "executed_timestamp": "1567411795.000" // Unix epoch time in seconds
        },
        {
            "symbol": "SPOT_ETH_USDT",
            "side": "BUY",
            "source": 1,
            "executed_price": 202,
            "executed_quantity": 0.00025,
            "executed_timestamp": "1567411795.000" // Unix epoch time in seconds
        }
    ]
}
```

**Parameters**

| Name   | Type   | Required        | Description                      |
| ------ | ------ | --------------- | -------------------------------- |
| symbol | string | Y               |                                  |
| limit  | number | N (default: 10) | Numbers of trades you want to query. |

## Market Trades History(Public)

**Limit: 1 requests per 1 second per IP address**

`
GET https://api-pub.woo.org/v1/hist/trade
`

Get historical market trades data. The response output "source" 1=internal (trade on WOO X), 0=external (trade from aggregrated sources)

> **Response**

```js
{
    "success": true,
    "data":{
        "rows": [
            {
                "symbol": "SPOT_ETH_USDT",
                "side": "BUY",
                "source": 0,
                "executed_price": 202,
                "executed_quantity": 0.00025,
                "executed_timestamp": "1567411795.000" // Unix epoch time in seconds
            },
            {
                "symbol": "SPOT_ETH_USDT",
                "side": "BUY",
                "source": 1,
                "executed_price": 202,
                "executed_quantity": 0.00025,
                "executed_timestamp": "1567411795.000" // Unix epoch time in seconds
            }
        ],
        "meta":{
            "total":10911159,
            "records_per_page":100,
            "current_page":1
        }
    },
    "timestamp":1669072422897
}
```

**Parameters**

| Name   | Type   | Required        | Description                      |
| ------ | ------ | --------------- | -------------------------------- |
| page   | number | N (default: 1)  |                                  |
| size   | number | N (default: 25)  |                                  |
| start_time | number | Y             | start range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| symbol | string | Y               |                                  |







## Orderbook snapshot (Public)

**Limit: 10 requests per 1 second**

`
GET /v1/public/orderbook/:symbol
`

SNAPSHOT of current orderbook. Price of asks/bids are in descending order.
Note: The original endpoint `GET /v1/orderbook/:symbol` can still be used.



> **Response**

```js
{
    "success": true,
    "asks": [
        {
            "price": 10669.4,
            "quantity": 1.56263218
        },
        {
            "price": 10670.3,
            "quantity": 0.36466977
        },
        {
            "price": 10670.4,
            "quantity": 0.06738009
        }
    ],
    "bids": [
        {
            "price": 10669.3,
            "quantity": 0.88159988
        },
        {
            "price": 10669.2,
            "quantity": 0.5
        },
        {
            "price": 10668.9,
            "quantity": 0.00488286
        }
    ],
    "timestamp": 1564710591905   // Unix epoch time in milliseconds
}
```

**Parameters**


| Name      | Type   | Required         | Description                           |
| --------- | ------ | ---------------- | ------------------------------------- |
| max_level | number | N (default: 100) | the levels you wish to show on both sides. |


## Kline (Public)

**Limit: 10 requests per 1 second**

`
GET /v1/public/kline
`

The latest klines of the trading pairs.
Note: The original endpoint `GET /v1/kline` can still be used.


> **Response**

```js
{
    "success": true,
    "rows": [
        {
            "open": 66166.23,
            "close": 66124.56,
            "low": 66038.06,
            "high": 66176.97,
            "volume": 23.45528526,
            "amount": 1550436.21725288,
            "symbol": "SPOT_BTC_USDT",
            "type": "1m",
            "start_timestamp": 1636388220000, // Unix epoch time in milliseconds
            "end_timestamp": 1636388280000
        },
        {
            "open": 66145.13,
            "close": 66166.24,
            "low": 66124.62,
            "high": 66178.60,
            "volume": 15.50705000,
            "amount": 1025863.18892610,
            "symbol": "SPOT_BTC_USDT",
            "type": "1m",
            "start_timestamp": 1636388160000,
            "end_timestamp": 1636388220000
        },
        // ...skip
    ]
}
```

**Parameters**

| Name    | Type   | Required         | Description                                                 |
| ------- | ------ | ---------------- | ----------------------------------------------------------- |
| symbol  | string | Y                |                                                             |
| type    | enum   | Y                | `1m`/`5m`/`15m`/`30m`/`1h`/`4h`/`12h`/`1d`/`1w`/`1mon`/`1y` |
| limit   | number | N (default: 100) | Numbers of klines. Maximum of 1000 klines.                  |

## Kline - Historical Data (Public)

**Limit: 1 request per 1 second per IP**

`
GET https://api-pub.woo.org/v1/hist/kline 
`

The historical klines of the trading pairs. Note that the endpoint is different with other APIs.

> **Response**

```js
{
    "success": true,
    "data": {
        "rows": [
            {
                "open": 66166.23,
                "close": 66124.56,
                "low": 66038.06,
                "high": 66176.97,
                "volume": 23.45528526,
                "amount": 1550436.21725288,
                "symbol": "SPOT_BTC_USDT",
                "type": "1m",
                "start_timestamp": 1636388220000, // Unix epoch time in milliseconds
                "end_timestamp": 1636388280000
            },
            {
                "open": 66145.13,
                "close": 66166.24,
                "low": 66124.62,
                "high": 66178.60,
                "volume": 15.50705000,
                "amount": 1025863.18892610,
                "symbol": "SPOT_BTC_USDT",
                "type": "1m",
                "start_timestamp": 1636388160000,
                "end_timestamp": 1636388220000
            },
            // ...skip
        ],
        "meta":{
            "total":67377,
            "records_per_page":100,
            "current_page":1
        }
    },
    "timestamp": 1636388280000
}
```

**Parameters**

| Name    | Type   | Required         | Description                                                 |
| ------- | ------ | ---------------- | ----------------------------------------------------------- |
| symbol  | string | Y                |                                                             |
| type    | enum   | Y                | `1m`/`5m`/`15m`/`30m`/`1h`/`4h`/`12h`/`1d`/`1w`/`1mon`      |
| start_time | number | Y             | start range that you wish to query, noted that the time stamp is a 13-digits timestamp. |

## Available Token (Public)

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/token
`

Get the available tokens that WOO X supports, it need to use when you call get deposit address or withdraw api.

> **Response**

```js
{
    "success": true,
    "rows": [
        {
            "created_time": "1579399877.02", // Unix epoch time in seconds
            "updated_time": "1579399877.02", // Unix epoch time in seconds
            "token": "BTC",
            "delisted": false,
            "balance_token": "BTC",
            "fullname": "Bitcoin",
            "network": "BTC",
            "decimals": 8,
            "can_collateral":true,
            "can_short":true
        }
        
    ]
}
```

**Parameters**

None

## Token Network (Public)

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/token_network
`

Get the available networks for each token as well as the deposit/withdrawal information.

> **Response**

```js
{
    "success": true,
    "rows": [
        {
            "protocol": "BTC",
            "token": "BTC",
            "name": "Bitcoin",
            "minimum_withdrawal": 0.01,
            "withdrawal_fee": 0.05,
            "allow_deposit": 1,
            "allow_withdraw": 1
        },
        {
            "protocol": "ERC20",
            "token": "ETH",
            "name": "Ethereum",
            "minimum_withdrawal": 0.03,
            "withdrawal_fee": 0.06,
            "allow_deposit": 1,
            "allow_withdraw": 1
        },
        {
            "protocol": "ERC20",
            "token": "WOO",
            "name": "Ethereum",
            "minimum_withdrawal": 30,
            "withdrawal_fee": 20,
            "allow_deposit": 1,
            "allow_withdraw": 1
        },
        {
            "protocol": "BEP20",
            "token": "WOO",
            "name": "Binance Smart Chain",
            "minimum_withdrawal": 30,
            "withdrawal_fee": 3,
            "allow_deposit": 1,
            "allow_withdraw": 1
        },
        // ...
    ]
}
```

**Parameters**

None



## Get Predicted Funding Rate for All Markets (Public)

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/funding_rates
`

Get predicted funding rate and the latest funding rate for all the markets.

> **Response**

```js
{
    "success":true,
    "rows": [
        {
            "symbol":"PERP_BTC_USDT",
            "est_funding_rate":-0.00001392,
            "est_funding_rate_timestamp":1681069199002,
            "last_funding_rate":-0.00001666,
            "last_funding_rate_timestamp":1681066800000,
            "next_funding_time":1681070400000,
            "last_funding_rate_interval":1,
            "est_funding_rate_interval":1
        },
        {
            "symbol":"PERP_ETH_USDT",
            "est_funding_rate":-0.00001394,
            "est_funding_rate_timestamp":1681069319011,
            "last_funding_rate":-0.00001661,
            "last_funding_rate_timestamp":1681066800000,
            "next_funding_time":1681070400000,
            "last_funding_rate_interval":1,
            "est_funding_rate_interval":1
        }
    ],
    "timestamp":1681069222726, // Unix epoch time in milliseconds
}
```

## Get Predicted Funding Rate for One Market (Public)

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/funding_rate/:symbol
`

Get predicted funding rate and the latest funding rate for one market.

**Parameters**

| Name   | Type   | Required | Description |
| :----- | :----- | :------- | :---------- |
| symbol | string | Y        |             |

> **Response**

```js
{
    "success":true,
    "timestamp":1681069222726,
    "symbol":"PERP_BTC_USDT",
    "est_funding_rate":-0.00001392,
    "est_funding_rate_timestamp":1681069199002,
    "last_funding_rate":-0.00001666,
    "last_funding_rate_timestamp":1681066800000, // use rate to end calculating funding fee time
    "next_funding_time":1681070400000,
    "last_funding_rate_interval":1,
    "est_funding_rate_interval":1
}
```

## Get Funding Rate History for One Market (Public)

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/funding_rate_history
`

Get funding rate for one market.

**Parameters**

| Name    | Type      | Required       | Description                                                  |
| :------ | :-------- | :------------- | :----------------------------------------------------------- |
| symbol  | string    | Y              |                                                              |
| start_t | timestamp | N              | start time range that you wish to query, noted that the time stamp is a 13-digits timestamp. If start_t and end_t are not filled, the newest funding rate will be returned. |
| end_t   | timestamp | N              | end time range that you wish to query, noted that the time stamp is a 13-digits timestamp. If start_t and end_t are not filled, the newest funding rate will be returned. |
| page    | number    | N (default: 1) | the page you wish to query.                                      |
| size   | number | N (default: 25)  |                                  |

> **Response**

```js
{
    "success": true,
    "meta": {
        "total": 670,
        "records_per_page": 25,
        "current_page": 1
    },
    "rows": [
    	{
    		"symbol": "PERP_BTC_USDT",
    		"funding_rate": 0.12345689,
    		"funding_rate_timestamp": 1567411795000, // use rate to end calculating funding fee time
    		"next_funding_time": 1567411995000
    	},
    	{
    		"symbol": "PERP_BTC_USDT",
    		"funding_rate": 0.12345689,                                                 
    		"funding_rate_timestamp": "1567411795.000", // use rate to end calculating funding fee time
    		"next_funding_time": 1567411995000
    	}
    ],
    "timestamp": 1564710591905 // Unix epoch time in milliseconds
}
```

## Get Futures Info for All Markets (Public)

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/futures
`

Get basic futures information for all the markets.

> **Response**

```js
{
    "success": true,
    "rows": [
        {
          "symbol": "PERP_BTC_USDT",
		     	"index_price": 56727.31344564,
    			"mark_price": 56727.31344564,
    			"est_funding_rate": 0.12345689,
    			"last_funding_rate": 0.12345689,
    			"next_funding_time": 1567411795000,
    			"open_interest": 0.12345689,
    			"24h_open": 0.16112,
        		"24h_close": 0.32206,
        		"24h_high": 0.33000,
        		"24h_low": 0.14251,
        		"24h_volume": 89040821.98,
        		"24h_amount": 22493062.21
        },
        {
           	"symbol": "PERP_ETH_USDT",
            	"index_price": 6727.31344564,
    			"mark_price": 6727.31344564,
    			"est_funding_rate": 0.12345689,
    			"last_funding_rate": 0.12345689,
    			"next_funding_time": 1567411795000,
    			"open_interest": 0.12345689,
    			"24h_open": 0.16112,
        		"24h_close": 0.32206,
        		"24h_high": 0.33000,
        		"24h_low": 0.14251,
        		"24h_volume": 89040821.98,
        		"24h_amount": 22493062.21
        }
    ],
    "timestamp": 1564710591905 // Unix epoch time in milliseconds
}
```

## Get Futures for One Market (Public)

**Limit: 10 requests per 1 second per IP address**

`
GET /v1/public/futures/:symbol
`

Get basic futures information for one market.

**Parameters**

| Name   | Type   | Required | Description |
| :----- | :----- | :------- | :---------- |
| symbol | string | Y        |             |

> **Response**

```js
{
    "success": true,
    "info":{
    	"symbol": "PERP_BTC_USDT",
    	"index_price": 56727.31344564,
    	"mark_price": 56727.31344564,
    	"est_funding_rate": 0.12345689,
    	"last_funding_rate": 0.12345689,
    	"next_funding_time": 1567411795000,
    	"open_interest": 0.12345689,
    	"24h_open": 0.16112,
       "24h_close": 0.32206,
       "24h_high": 0.33000,
       "24h_low": 0.14251,
       "24h_volume": 89040821.98,
       "24h_amount": 22493062.21
    },
    "timestamp": 1564710591905 // Unix epoch time in milliseconds
}
```

## Token Config

**Limit: 10 requests per 1 second**

`
GET /v1/client/token
`

Get the configuration (collateral ratio, margin ratio factor etc) of the token.

> **Response**

```js
{
    "success": true,
    "rows": [
        {
            "token": "BTC",
            "collateral_ratio": 0.85,
            "margin_factor": 2.3e-8,
            "futures_margin_factor": 2.3e-8,
            "collateral": true,        // if the token is now used as collateral
            "can_collateral": true,    // if the token can be used as collateral
            "can_short": true,         // if the token supports short selling
            "stable": false,            // if the token is stable coin or not
            'margin_max_leverage': 5, 
            'futures_max_leverage': 20, 
            'margin_max_position': 100000000000,
            'futures_max_position': 100000000000
        },
        {
            "token": "ETH",
            "collateral_ratio": 0.85,
            "margin_factor": 2.5e-8,
            "futures_margin_factor": 2.3e-8,
            "collateral": true,
            "can_collateral": true,
            "can_short": true,
            "stable": false, 
            'margin_max_leverage': 5, 
            'futures_max_leverage': 20, 
            'margin_max_position': 100000000000,
            'futures_max_position': 100000000000
        },
        {
            "token": "ASD",
            "collateral_ratio": 1,
            "margin_factor": 0,
            "futures_margin_factor": 0,
            "collateral": false,
            "can_collateral": false,
            "can_short": false,
            "stable": false, 
            'margin_max_leverage': 5, 
            'futures_max_leverage': 20, 
            'margin_max_position': 100000000000,
            'futures_max_position': 100000000000
        }
    ]
}
```

**Parameters**

None


## Send Order

**Limit: 10 requests per 1 symbol per 1 second**

`
POST /v1/order
`

Place order maker/taker, the order executed information will be updated from websocket stream.
will respond immediately with an order created message.

`MARKET` type order behavior: it matches until all size is executed. If the size is too large (larger than the whole book) or the matching price exceeds the price limit (refer to `price_range`), then the remaining quantity will be cancelled.

`IOC` type order behavior: it matches as much as possible at the order_price. If not fully executed, then remaining quantity will be cancelled.

`FOK` type order behavior: if the order can be fully executed at the order_price then the order gets fully executed otherwise it would be cancelled without any execution.

`ASK` type order behavior: the order price is guaranteed to be the best ask price of the orderbook if it gets accepted.

`BID` type order behavior: the order price is guaranteed to be the best bid price of the orderbook if it gets accepted.

`visible_quantity` behavior: it sets the maximum quantity to be shown on orderbook. By default, it is equal to order_quantity, negative number and number larger than `order_quantity` is not allowed.
     If it sets to 0, the order would be hidden from the orderbook.
     It doesn't work for `MARKET`/`IOC`/`FOK` orders since orders with these types would be executed and cancelled immediately and not be shown on orderbook.
     For `LIMIT`/`POST_ONLY` order, as long as it's not complete, `visible_quantity` is the maximum quantity that is shown on the orderbook.

`order_amount` behavior: for `MARKET`/`BID`/`ASK` order, order can be placed by `order_amount` instead of `order_quantity`. It's the size of the order in terms of the quote currency instead of the base currency. The order would be rejected if  both `order_amount` and `order_quantity` are provided. The precision of the number should be within 8 digits.

`client_order_id` behavior: customized order_id, a unique id among open orders. Orders with the same `client_order_id` can be accepted only when the previous one if completed, otherwise the order will be rejected.

For `MARKET`/`BID`/`ASK` order, if margin trading is disabled, `order_amount` is not supported when placing SELL order while `order_quantity` is not supported when placing BUY order.

For `Long`/ `Short` order, It is supported when position mode is HEDGE_MODE and the trading involves futures.

`reduce_only` behavior: only applicable to perpetual symbols.  When reduce only is set to true, the system ensures that the order will reduce the position size rather than increasing it.  To facilitate this, the system must group related orders to accurately manage the reduce only calculations.  There is a cap of 50 orders that can be grouped together and if the limit is exceeded, the system will reject the incoming order.


> **Response**

```js
{
  "success": true,
  "order_id": 13,
  "client_order_id": 0,
  "order_type": "LIMIT",
  "order_price": 100.12,
  "order_quantity": 0.987654,
  "order_amount": null,
  "reduce_only": false,
  "timestamp": "1639980423.855" // Unix epoch time in seconds
}
```

**Parameters**

| Name             | Type   | Required | Description                                                                              |
| ---------------- | ------ | -------- | --------------------------------------------------------------------------------------   |
| symbol           | string | Y        |                                                                                          |
| client_order_id  | number | N        | number for scope : from 0 to 9223372036854775807. (default: 0)                           |
| margin_mode      | enum   | N        | `CROSS`/`ISOLATED`, defualt will be `CROSS`. The `ISOLATED` option only applicable to perp symbols, will be rejected if passed in for spot symbols <font color=#0000FF></font>|
| order_tag        | string | N        | An optional tag for this order. (default: `default`)                                     |
| order_type       | enum   | Y        | `LIMIT`/`MARKET`/`IOC`/`FOK`/`POST_ONLY`/`ASK`/`BID`                                     |
| order_price      | number | N        | If order_type is `MARKET`, then is not required, otherwise this parameter is required.   |
| order_quantity   | number | N        | For `MARKET`/`ASK`/`BID` order, if `order_amount` is given, it is not required.          |
| order_amount     | number | N        | For `MARKET`/`ASK`/`BID` order, the order size in terms of quote currency                |
| reduce_only      | boolean | N       | true or false, default false,If the user's RO order message contains 50 pending orders,the order can be created successfully placed.                                                           |
| visible_quantity | number | N        | The order quantity shown on orderbook. (default: equal to `order_quantity`)              |
| side             | enum   | Y        | `SELL`/`BUY`                                                                             |
| position_side    | enum   | N        | `SHORT`/`LONG`, If position mode is HEDGE_MODE and the trading involves futures,then is required, otherwise this parameter is not required.|


## Cancel all after

**Limit: 10 requests per 1 second**  

`
POST  v1/order/cancel_all_after
`

Provide a dead man switch to ensure user orders are canceled in case of an outage. If called repeatedly, the new timeout offset will replace the existing one if already set.When count down hits 0, all of the user’s ordinary and algo orders will be canceled.This API is only available to VIP users.Please reach out to customer service for more information.

> **Response**

```js

{
    "success": true,
    "data": {
        "expected_trigger_time": 1711534302938
    },
    "timestamp": 1711534302943
}
```

**Parameters**


| Name     | Type   | Required | Description                        |
| -------- | ------ | -------- | ---------------------------------- |
| trigger_after | integer | Y        | Timeout in ms.  Max timeout can be set to 900000.  To cancel this timer, set timeout to 0.|

<!-- ## Cancel all after_V3

**Limit: 5 requests per 1 second**  

`
POST  v3/trade/order/cancelAllAfter
`

Provide a dead man switch to ensure user orders are canceled in case of an outage. If called repeatedly, the new timeout offset will replace the existing one if already set.When count down hits 0, all of the user’s ordinary and algo orders will be canceled.

> **Response**

```js

{
    "success": true,
    "data": {
        "expectedTriggerTime": 1711534302938
    },
    "timestamp": 1711534302943
}
```

**Parameters**


| Name     | Type   | Required | Description                        |
| -------- | ------ | -------- | ---------------------------------- |
| TriggerAfter | integer | Y        | Timeout in ms.  Max timeout can be set to 900000.  To cancel this timer, set timeout to 0.|

 -->


## Cancel Order

**Limit: 10 requests per 1 second** shared with [cancel_order_by_client_order_id](#cancel-order-by-client_order_id)

`
DELETE /v1/order
`

Cancel order by order id. The order cancelled information will be updated from websocket stream.
note that we give an immediate response with an order cancel sent message, and will update the cancel event via the websocket channel.

> **Response**

```js
{
  "success": true,
  "status": "CANCEL_SENT"
}
```

**Parameters**


| Name     | Type   | Required | Description                        |
| -------- | ------ | -------- | ---------------------------------- |
| order_id | number | Y        | The `order_id` that you wish tocancel |
| symbol   | string | Y        |                                    |


## Cancel Order by client_order_id

**Limit: 10 requests per 1 second** shared with [cancel_order](#cancel-order)

`
DELETE /v1/client/order
`

Cancel order by client order id. The order cancelled information will be updated from websocket stream.
note that we give an immediate response with an order cancel sent message, and will update the cancel event via the websocket channel.

Only the latest order with the `symbol` and `client_order_id` would be canceled.

> **Response**

```js
{
  "success": true,
  "status": "CANCEL_SENT"
}
```

**Parameters**


| Name            | Type   | Required | Description                               |
| --------------- | ------ | -------- | ----------------------------------------- |
| client_order_id | number | Y        | The `client_order_id` that you wish tocancel |
| symbol          | string | Y        |                                           |


## Cancel Orders

**Limit: 10 requests per 1 second**

`
DELETE /v1/orders
`

Cancel orders by symbol.

> **Response**

```js
{
  "success": true,
  "status": "CANCEL_ALL_SENT"
}
```

**Parameters**


| Name     | Type   | Required | Description                        |
| -------- | ------ | -------- | ---------------------------------- |
| symbol   | string | Y        |                                    |
| page      | number    | N (default: 1) | the page you wish to query.         |
| size   | number | N (default: 25)  |                                  |

## Cancel All Pending Orders

**Limit: 10 requests per 1 second**

`
DELETE /v3/orders/pending
`

Cancel all pending ordinary orders.

> **Response**

```js
// success response
{
    "success": true,
    "status": "CANCEL_ALL_SENT"
}

// Failed response
{
    "success": false,
    "code": -1002,
    "message": "The request is unauthorized."
}
```


## Get Order

**Limit: 10 requests per 1 second** shared with [get_order_by_client_order_id](#get-order-by-client-order-id)

`
GET /v1/order/:oid
`

Get specific order details by `order_id`.
The `realized_pnl` field in response will only present the settled amount for futures orders.

> **Response**

```js
{
    "success": true,
    "created_time": "1577349119.33", // Unix epoch time in seconds
    "side": "SELL",
    "status": "FILLED",
    "symbol": "PERP_BTC_USDT",
    "client_order_id": 0,
    "reduce_only": false,
    "order_id": 1,
    "order_tag": "default",
    "type": "LIMIT",
    "price": 123,
    "quantity": 0.1,
    "amount": null,
    "visible": 0.1,
    "executed": 0.1,
    "total_fee": 0.00123,  // represents the cumulative fees for the entire order
    "fee_asset": "USDT",
    "average_executed_price": 123,
    "realized_pnl":null,
    'total_rebate': 0,   // indicates the aggregate rebates for the entire order
    'rebate_asset': null, 
    "position_side":'SHORT',
    'margin_mode':'CROSS', 
    'leverage':20, 
    
    // Detail transactions of this order
    "Transactions": [
        {
            "id": 2,
            "symbol": "PERP_BTC_USDT",
            "fee": 0.0001,   // fee for a single transaction
            "fee_asset": "usdt", // fee. use Base (BTC) as unit when BUY, use Quote (USDT) as unit when SELL
            "side": "BUY",
            "order_id": 1,
            "executed_price": 123,
            "executed_quantity": 0.05,
            "executed_timestamp": "1567382401.000", // Unix epoch time in seconds
            "is_maker": 1
        }]
}
```

**Parameters**


| Name | Type   | Required | Description                           |
| ---- | ------ | -------- | ------------------------------------- |
| oid  | number | Y        | The order_id `oid` that you wish to query |


<!-- 
## Get Order_V3


**Limit: 10 requests per 1 second**  

`
GET /v3/trade/order
`

Get specific order details by `orderId` or `clientOrderId`.


> **Response**

```js
{
    "success": true,
    "data": {
        "symbol": "SPOT_BTC_USDT",
        "status": "FILLED",
        "side": "SELL",
        "positionSide": "BOTH",
        "createdTime": 1578565539808,
        "orderId": 13,
        "orderTag": "default",
        "price": 123,
        "type": "LIMIT",
        "quantity": 0.1,
        "amount": null,
        "visible": 0.1,
        "executed": 0.1,
        "totalFee": 0.00123,
        "feeAsset": "USDT",
        "totalRebate":0,
        "rebateAsset":"",
        "clientOrderId": 0,
        "reduceOnly": false,
        "realizedPnl":null,
        "averageExecutedPrice": 123,
    }
}
```

**Parameters**


| Name     | Type   | Required | Description                        |
| -------- | ------ | -------- | ---------------------------------- |
| order_id | integer | Conditional        | Id of the order; Either `orderId` or `clientOrderId` is required. If both are passed, `orderId` will be used. |
| clientOrderId   | integer | Conditional        |   Client order Id as assigned by the user; Either `orderId` or `clientOrderId` is required. If both are passed, `orderId` will be used                                 |
 -->

## Get Order by client_order_id

**Limit: 10 requests per 1 seconds** shared with [get_order](#get-order)

`
GET /v1/client/order/:client_order_id
`

Get specific order details by `client_order_id`. If there is more than one order with the same `client_order_id`, return the latest one.
The `realized_pnl` field in response will only present the settled amount for futures orders.

> **Response**

```js
{
    "success": true,
    "created_time": "1577349119.33", // Unix epoch time in seconds
    "side": "SELL",
    "status": "FILLED",
    "symbol": "SPOT_BTC_USDT",
    "client_order_id": 123,
    "reduce_only": false,
    "order_id": 1,
    "order_tag": "default",
    "type": "LIMIT",
    "price": 123,
    "quantity": 0.1,
    "amount": null,
    "visible": 0.1,
    "executed": 0.1,
    "total_fee": 0.00123,   // represents the cumulative fees for the entire order
    "fee_asset": "USDT",
    "average_executed_price": 123,
    "realized_pnl":null,
    'total_rebate': 0,    // indicates the aggregate rebates for the entire order
    'rebate_asset': null,
    'margin_mode':'CROSS', 
    'leverage':20, 

    // Detail transactions of this order
    "Transactions": [
        {
            "id": 2,
            "symbol": "SPOT_BTC_USDT",
            "fee": 0.0001,    // fee for a single transaction
            "fee_asset": "BTC", // fee. use Base (BTC) as unit when BUY, use Quote (USDT) as unit when SELL
            "side": "BUY",
            "order_id": 1,
            "executed_price": 123,
            "executed_quantity": 0.05,
            "executed_timestamp": "1567382401.000", // Unix epoch time in seconds
            "is_maker": 1
        }]

}
```

**Parameters**

| Name             | Type      | Required       | Description                                                              |
| ---------------- | --------- | -------------- | ------------------------------------------------------------------------ |
| client_order_id  | number    | Y              | customized order_id when placing order                                   |


## Get Orders

**Limit: 10 requests per 1 second**

`
GET /v1/orders
`

Get orders by customize conditions.  
- `INCOMPLETE` = `NEW` + `PARTIAL_FILLED`  
- `COMPLETED` = `CANCELLED` + `FILLED` + `REJECTED`
The `realized_pnl` field in response will only present the settled amount for futures orders. The return value default is null unless the input parameter `realized_pnl` set to `true`


> **Response**

```js
{
    "success": true,
    "meta": {
        "total": 31,
        "records_per_page": 25,
        "current_page": 1
    },
    "rows": [
        {
            "side": "SELL",
            "status": "CANCELLED",
            "symbol": "SPOT_BCHABC_USDT",
            "client_order_id": 123,
            "reduce_only": false,
            "order_id": 8197,
            "order_tag": "default",
            "type": "LIMIT",
            "price": 308.51,
            "quantity": 0.0019,
            "amount": null,
            "visible": 0.0019,
            "executed": 0,
            "total_fee": 0,
            "fee_asset": null,
            'total_rebate': 0,
            'rebate_asset': null,
            "created_time": "1575014255.089", // Unix epoch time in seconds
            "updated_time": "1575014255.910", // Unix epoch time in seconds
            "average_executed_price": null,
            "position_side": "LONG",  
            "realized_pnl":null,
            'margin_mode':'CROSS', 
            'leverage':20, 
        },
        // ....skip (total 25 items in one page)
    ]
}
```

**Parameters**


| Name      | Type      | Required       | Description                                                                       |
| --------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| symbol    | string    | N              |                                                                                   |
| side      | string    | N              | `BUY`/`SELL`                                                                      |
| size      | number    | N              | The page size, default 100, max 500.                                              |
| order_type| string    | N              | `LIMIT`/`MARKET`/`IOC`/`FOK`/`POST_ONLY`/`LIQUIDATE`                              |
| order_tag | string    | N              | An optional tag for this order.                                                   |
| realized_pnl| boolean | N              | Decide if return data calculate realized pnl value for the futures order.         |
| status    | enum      | N              | `NEW`/`CANCELLED`/`PARTIAL_FILLED`/`FILLED`/`REJECTED`/`INCOMPLETE`/`COMPLETED`   |
| start_t   | timestamp | N              | start time range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| end_t     | timestamp | N              | end time range that you wish to query, noted that the time stamp is a 13-digits timestamp.   |
| page      | number    | N (default: 1) | the page you wish to query.                                                           |


<!-- ## Get Orders_V3
**Limit: 10 requests per 1 second**  

`
GET /v3/trade/orders
`

Get orders by customizable conditions.  For filtering by status, one can reference special bundled statuses below for ease of access of open (i.e. INCOMPLETE) orders or COMPLETED orders.

`INCOMPLETE = NEW + PARTIAL_FILLED`

`COMPLETED = CANCELLED + FILLED + REJECTED`

> **Response**

```js
{
    "success": true,
    "data": {
        "meta": {
            "total": 31,
            "recordsPerPage": 25,
            "currentPage": 1
        },
        "rows": [
            {
                "symbol": "PERP_BTC_USDT",
                "status": "FILLED",
                "side": "SELL",
                "positionSide": "BOTH",
                "createdTime": 1578565539808,
                "orderId": 135,
                "orderTag": "default",
                "price": 123,
                "type": "LIMIT",
                "quantity": 0.1,
                "amount": null,
                "visible": 0.1,
                "executed": 0.1,
                "totalFee": 0.00123,
                "feeAsset": "USDT",
                "clientOrderId": 0,
                "totalRebate":0,
                "rebateAsset":"",
                "reduceOnly": false,
                "realizedPnl": 2,
                "averageExecutedPrice": 123,
            },
            ...
        ]
    }
}
```

**Parameters**


| Name            | Type   | Required | Description                               |
| --------------- | ------ | -------- | ----------------------------------------- |
| symbol          | string | 	No (default: all symbols) | Symbol name                                          |
| side          | string |  No (default: both `BUY` and `SELL`)        |    `BUY/SELL`                                      |
| positionSide          | string | No (default: all position sides)        |  `BOTH` for one way mode; `LONG` or `SHORT` for hedge mode;  Only applicable to perpetual instruments                                         |
| type          | string | No (default: all order types)        |  `LIMIT`/`MARKET`/`IOC`/`FOK`/`POST_ONLY`/LIQUIDATE                                         |
| orderTag          | string |   No    |  Order tag                                         |
| realizedPnl          | boolean |     No (default: `false`)   |    Whether to return order’s realized pnl                                       |
| status          | string | No (default: all statuses)       |    `NEW`/`CANCELLED`/`PARTIAL_FILLED`/`FILLED`/`REJECTED`/`INCOMPLETE`/`COMPLETED`                                       |
| startTime          | integer | No       |  Start timestamp in Unix timestamp format in milliseconds                                         |
| endTime          | integer | No        |     End timestamp in Unix timestamp format in milliseconds                                      |
| page          | integer | No (default: 1)        |   Page number                                        |
| size          | integer | No (default: 100)        |       Data size per page, max 500                                    |
 -->

## Edit Order 

**Limit: 5 requests per 1 second**

`
PUT /v3/order/:order_id
`

***Note that for v3 API with json body POST method, please follow the instruction in [authentication](#authentication) section for `v3` API to generate the signature.
***Please use `string` type for value input field to remain data accurancy.

The API allow you to edit the price and the quantity of the selected order. You must input at least one of it in the request body.



> **Response**

```js
// Success response
{
    "success": true,
    "data": {
        "success": true,
        "status": "EDIT_SENT"
    },
    "timestamp": 1673842319229
}

// Failed response
{
    "success": false,
    "code": -1103,
    "message": "The order does not meet the price filter requirement."
}
```
> **Request**

```js
{
    "price": "10.5",
    "quantity": "1.4"
}
```



**Parameters**


| Name             | Type   | Required | Description                                                                            |
| ---------------- | ------ | -------- | -------------------------------------------------------------------------------------- |
| order_id         | number | Y        | The `order_id` that you wish to query         |
| price            | string | N        | New price of the order.                       |
| quantity         | string | N        | New quantity of the order.                    |

## Edit Order by client_order_id

**Limit: 5 requests per 1 second**

`
PUT /v3/order/client/:client_order_id
`

***Note that for v3 API with json body POST method, please follow the instruction in [authentication](#authentication) section for `v3` API to generate the signature.
***Please use `string` type for value input field to remain data accurancy.

The API allow you to edit the price and the quantity of the selected order. You must input at least one of it in the request body.



> **Response**

```js
// Success response
{
    "success": true,
    "data": {
        "success": true,
        "status": "EDIT_SENT"
    },
    "timestamp": 1673842319229
}

// Failed response
{
    "success": false,
    "code": -1103,
    "message": "The order does not meet the price filter requirement."
}
```
> **Request**

```js
{
    "price": "10.5",
    "quantity": "1.4"
}
```



**Parameters**


| Name             | Type   | Required | Description                                                                            |
| ---------------- | ------ | -------- | -------------------------------------------------------------------------------------- |
| client_order_id  | number | Y        | customized order_id when placing order                                                 |
| price            | string | N        | New price of the order.                                                                |
| quantity         | string | N        | New quantity of the order.                                                             |


## Send Algo Order

**Limit: 2 requests per 1 second per symbol**

`
POST /v3/algo/order
`

***Note that for v3 API, please follow the instruction in [authentication](#authentication) section for `v3` API to generate the signature.
***Please use `string` type for value input field to remain data accurancy.

Place algo order maker/taker, the order executed information will be updated from websocket stream.
will respond immediately with an order created message.

To place `Stop Market` order, please use 'STOP' as `algoType` and 'MARKET' as `type`. Please input the trigger price in `triggerPrice` field.

To place `Stop Limit` order, please use 'STOP' as `algoType` and 'LIMIT' as `type`. Please input the trigger price in `triggerPrice` field.

To place `Trailing Stop` order, please use 'TRAILING_STOP' as `algoType` and 'MARKET' as `type`. Please also input your trailing rate setting in `callbackRate` field.

To place `OCO` order, the input fields is 2 layer and includes an array of the objects named `childOrder`. The second order of OCO order should be a STOP_LIMIT or STOP MARKET order object in the array. please use 'OCO' as `algoType` in outter parameters, 'STOP' as `algoType` in `childOrder` object, and 'LIMIT' or 'MARKET' as type.

To place `Positional TP/SL` order, the input fields is 2 layer and includes an array of the objects named `childOrder`. The take-profit or stop-loss order should be the objects in the array. For the sub-order in `childOrder`, please input 'CLOSE_POSITION' as `type`, and 'TAKE_PROFIT' or 'STOP_LOSS' in `algoType` field.




`visible_quantity` behavior: it sets the maximum quantity to be shown on orderbook. By default, it is equal to order_quantity, negative number and number larger than `order_quantity` is not allowed. The visibility of the childOrder will inherit the parent order's visibility setting. 
     If it sets to 0, the order would be hidden from the orderbook.
     It doesn't work for `MARKET` orders since orders with these types would be executed and cancelled immediately and not be shown on orderbook.
     For `LIMIT` order, as long as it's not complete, `visible_quantity` is the maximum quantity that is shown on the orderbook.

`client_order_id` behavior: customized order_id, a unique id among open orders. Orders with the same `client_order_id` can be accepted only when the previous one if completed, otherwise the order will be rejected.

For `Long`/ `Short` order, It is supported when position mode is HEDGE_MODE and the trading involves futures.

`reduce_only` behavior: only applicable to perpetual symbols.  When reduce only is set to true, the system ensures that the order will reduce the position size rather than increasing it.  To facilitate this, the system must group related orders to accurately manage the reduce only calculations.  There is a cap of 50 orders that can be grouped together and if the limit is exceeded, the system will reject the incoming order.  For algo orders, the check happens when the order gets triggered.




> **Response**

```js
{
  "code": 0,
  "data": {
    "rows": [
      {
        "algoType": "string",
        "clientOrderId": 0,
        "orderId": 0,
        "quantity": 0
      }
    ]
  },
  "message": "string",
  "success": true,
  "timestamp": 0
}

// bracket order response

{
    "success": true,
    "data": {
        "rows": [
            {
                "orderId": 432132,
                "clientOrderId": 0,
                "algoType": "TAKE_PROFIT",
                "quantity": 0
            },
            {
                "orderId": 432133,
                "clientOrderId": 0,
                "algoType": "STOP_LOSS",
                "quantity": 0
            },
            {
                "orderId": 432131,
                "clientOrderId": 0,
                "algoType": "POSITIONAL_TP_SL",
                "quantity": 0
            },
            {
                "orderId": 432130,
                "clientOrderId": 0,
                "algoType": "BRACKET",
                "quantity": 10
            }
        ]
    },
    "timestamp": 1676283560233
}

```
> **Request**


```js
// stop market order

{
    "symbol":"PERP_BTC_USDT",
    "side":"BUY",
    "orderCombinationType":"STOP_MARKET",
    "algoType":"STOP",
    "triggerPrice":"1000",
    "type":"MARKET",
    "quantity":"0.01"
}

//stop market limit

{
    "symbol":"PERP_BTC_USDT",
    "side":"BUY",
    "orderCombinationType":"STOP_LIMIT",
    "algoType":"STOP",
    "triggerPrice":"1000",
    "type":"LIMIT",
    "quantity":"0.01",
    "price":1000
}

//OCO 

{
    "symbol": "PERP_ETH_USDT",
    "side": "BUY",
    "reduceOnly": false,
    "type": "LIMIT",
    "quantity": "1",
    "algoType": "OCO",
    "price": "1000",
    "childOrders": [
        {
            "side": "BUY",
            "algoType": "STOP",
            "triggerPrice": "1600",
            "type": "MARKET"
        }
    ]
}

//Positional TP/SL

{
    "symbol": "SPOT_BAL_USDT",
    "reduceOnly": false,
    "algoType": "POSITIONAL_TP_SL",
    "childOrders": [
        {
            "algoType": "TAKE_PROFIT",
            "type": "CLOSE_POSITION",
            "side": "BUY",
            "reduceOnly": true,
            "triggerPrice": "72"
        },
        {
            "algoType": "STOP_LOSS",
            "type": "CLOSE_POSITION",
            "side": "BUY",
            "reduceOnly": true,
            "triggerPrice": "74"
        }
    ]
}

// Bracket order

{
    "symbol": "SPOT_BAL_USDT",
    "side": "BUY",
    "reduceOnly": false,
    "type": "LIMIT",
    "quantity": "1",
    "algoType": "BRACKET",
    "price": "69",
    "childOrders": [
        {
            "symbol": "SPOT_BAL_USDT",
            "reduceOnly": false,
            "algoType": "POSITIONAL_TP_SL",
            "childOrders": [
                {
                    "algoType": "TAKE_PROFIT",
                    "type": "CLOSE_POSITION",
                    "side": "SELL",
                    "reduceOnly": true,
                    "triggerPrice": "76"
                },
                {
                    "algoType": "STOP_LOSS",
                    "type": "CLOSE_POSITION",
                    "side": "SELL",
                    "reduceOnly": true,
                    "triggerPrice": "50"
                }
            ]
        }
    ]
}
```




**Parameters - Parent**


| Name             | Type   | Required | Description                                                                            |
| ---------------- | ------ | -------- | -------------------------------------------------------------------------------------- |
| activatedPrice   | string | N        | activated price for algoType=TRAILING_STOP                                               |
| algoType         | string | Y        | `STOP/OCO/TRAILING_STOP/BRACKET`|`POSITIONAL_TP_SL`                              |
| marginMode      | enum   | N        | `CROSS`/`ISOLATED`, defualt will be `CROSS`. The `ISOLATED` option only applicable to perp symbols, will be rejected if passed in for spot symbols <font color=#0000FF></font>|
| callbackRate     | string | N        | callback rate, only for algoType=TRAILING_STOP, i.e. the value = 0.1 represent to 10%. |
| callbackValue    | string | N        | callback value, only for algoType=TRAILING_STOP, i.e. the value = 100                  |
| childOrders       | child  | N        | Child orders for algoType=`POSITIONAL_TP_SL`|`BRACKET`                                       |
| symbol           | string | Y        |                                                                                        |
| clientOrderId     | number | N        | Client order id defined by client,number for scope : from 0 to 9223372036854775807. (default: 0), duplicated client order id on opening order is not allowed.   |
| orderTag         | string | N        | An optional tag for this order. (default: `default`)                                    |
| price            | string | N        | order price                                                                             |
| quantity         | string | N        | Order quantity, only optional for algoType=`POSITIONAL_TP_SL`                           |
| reduceOnly       | boolean | N       | true or false, default false.If the user's RO order message contains 50 pending orders,the order can be created successfully placed.                                                             |
| triggerPrice     | string | N       | trigger price, if algoType=TRAILING_STOP, you need to provide 'activatedPrice'          |
| triggerPriceType | string | N       | trigger price, default `MARKET_PRICE`, enum: `MARKET_PRICE`|`MARK_PRICE`                |
| type             | string   | Y        | `LIMIT`/`MARKET`                                                                     |
| visibleQuantity | number | N        | The order quantity shown on orderbook. (default: equal to `orderQuantity`)              |
| side             | enum   | Y        | `SELL`/`BUY`                                                                           |
| positionSide             | enum   | N        |`SHORT`/`LONG`, If position mode is HEDGE_MODE and the trading involves futures,then is required, otherwise this parameter is not required.|

**Parameters - Child**

| Name             | Type   | Required | Description                                                                            |
| ---------------- | ------ | -------- | -------------------------------------------------------------------------------------- |
| symbol           | string | Y        |                                                                                        |
| algoType         | string | Y   | `STOP`/`OCO`/`TRAILING_STOP`/`BRACKET`/`POSITIONAL_TP_SL`  ｜
| side             | enum   | Y        | `SELL`/`BUY`                                                                           |
| type             | string   | Y       | `LIMIT`/`MARKET`|`CLOSE_POSITION`                                                    |
| triggerPrice     | string | N       | trigger price, if algoType=TRAILING_STOP, you need to provide 'activatedPrice'          |
| price            | string | N        | order price                                                                            |
| reduceOnly       | boolean | N       | true or false, default false,If the user's RO order message contains 50 pending orders,the order can be created successfully placed.                                                           |
| childOrders       | child  | N        | Child orders for algoType=`POSITIONAL_TP_SL`|`BRACKET`                                |



## Cancel Algo Order

**Limit: 10 requests per 1 second** shared with [cancel_algo_order_by_client_order_id](#cancel-algo-order-by-client_order_id)

`
DELETE /v3/algo/order/:order_id
`

***Note: This v3 API using query string to pass parameter, please follow the instruction in [authentication](#authentication) section for `v3` API to generate the signature.
Cancel order by order id. The order cancelled information will be updated from websocket stream.
note that we give an immediate response with an order cancel sent message, and will update the cancel event via the websocket channel.

> **Response**

```js
// Success response
{
    "success": true,
    "status": "CANCEL_SENT"
}

// Failed response
    "success": false,
    "code": -1006,
    "message": "Your order and symbol are not valid or already canceled."
}
```

**Parameters**


| Name     | Type   | Required | Description                        |
| -------- | ------ | -------- | ---------------------------------- |
| order_id | number | Y        | The `order_id` that youwish to cancel |



## Cancel All Pending Algo Orders

**Limit: 10 requests per 1 second**

`
DELETE /v3/algo/orders/pending
`

***Note: This v3 API using query string to pass parameter, please follow the instruction in [authentication](#authentication) section for `v3` API to generate the signature.
Cancel all pending algo orders.

> **Response**

```js
// Success response
{
    "success": true,
    "status": "CANCEL_SENT"
}

// Failed response
    "success": false,
    "code": -1006,
    "message": "Your order and symbol are not valid or already canceled."
}
```



## Cancel Pending Merge Orders by Symbol

**Limit: 10 requests per 1 second**

`
DELETE /v3/merge/orders/pending/:symbol
`

***Note that for v3 API, please follow the instruction in [authentication](#authentication) section for `v3` API to generate the signature.
Cancel both ordinary and algo orders by symbol.

> **Response**

```js
{
  "success": true,
  "status": "CANCEL_ALL_SENT"
}
```

**Parameters**


| Name     | Type   | Required | Description                        |
| -------- | ------ | -------- | ---------------------------------- |
| side     | string | N (default: cancel both sides)       | BUY or SELL                        |
| symbol   | string | Y        |                                    |
| marginMode   | string | N (default:CROSS)        |     CROSS or ISOLATED                               |


## Get Algo Order

**Limit: 10 requests per 1 second** shared with [get_algo_order_by_client_order_id](#get-algo-order-by-client-order-id)

`
GET /v3/algo/order/:oid
`
***Note: This v3 API using query string to pass parameter, please follow the instruction in [authentication](#authentication) section for `v3` API to generate the signature.

Get specific order details by Algo order's `oid`.


> **Response**

```js
// Success response
{
    "success": true,
    "data": {
        "algoOrderId": 431601,
        "clientOrderId": 0,
        "rootAlgoOrderId": 431601,
        "parentAlgoOrderId": 0,
        "symbol": "SPOT_ADA_USDT",
        "orderTag": "default",
        "algoType": "BRACKET",
        "side": "BUY",
        "quantity": 11,
        "isTriggered": false,
        "triggerStatus": "SUCCESS",
        "type": "LIMIT",
        "status": "FILLED",
        "rootAlgoStatus": "FILLED",
        "algoStatus": "FILLED",
        "triggerPriceType": "MARKET_PRICE",
        "price": 0.33,
        "triggerTime": "0",
        "totalExecutedQuantity": 11,
        "averageExecutedPrice": 0.33,
        "totalFee": 0.0033,
        "feeAsset": "ADA",
        "totalRebate":0,
        "rebateAsset":"",
        "reduceOnly": false,
        "createdTime": "1676277825.917",
        "updatedTime": "1676280901.229",
        "positionSide":"LONG",
        'marginMode':'CROSS', 
        'leverage':20, 
        
    },
    "timestamp": 1676281474630
}

// Failed response
{
    "success": false,
    "code": -1006,
    "message": "The order can not be found."
}
```

**Parameters**


| Name | Type   | Required | Description                           |
| ---- | ------ | -------- | ------------------------------------- |
| oid  | number | Y        | The Algo order's order_id `oid` that you wish to query |


<!-- ## Get algo order_V3

**Limit: 10 requests per 1 second**  

`
GET /v3/trade/algoOrder
`

Get algo order details by `algoOrderId` or `clientAlgoOrderId`.



> **Response**

```js
{
    "success": true,
    "data": {
        "algoOrderId": 792420,
        "clientAlgoOrderId": 0,
        "rootAlgoOrderId": 792420,
        "parentAlgoOrderId": 0,
        "symbol": "SPOT_WOO_USDT",
        "orderTag": "default",
        "algoType": "TRAILING_STOP",
        "side": "SELL",
        "positionSide": "BOTH",
        "quantity": 1,
        "isTriggered": false,
        "triggerStatus": "USELESS",
        "type": "MARKET",
        "rootAlgoStatus": "NEW",
        "algoStatus": "NEW",
        "triggerPriceType": "MARKET_PRICE",
        "triggerTime": "0",
        "totalExecutedQuantity": 0,
        "averageExecutedPrice": 0,
        "totalFee": 0,
        "feeAsset": "",
        "totalRebate":0,
        "rebateAsset":"",
        "reduceOnly": false,
        "createdTime": 1696595230885,
        "updatedTime": 1696595230885,
        "isActivated": false,
        "callbackRate": 0.03,
        "activatedPrice": 0.21
    },
    "timestamp": 1676283560233
}
```

**Parameters**


| Name | Type   | Required | Description                           |
| ---- | ------ | -------- | ------------------------------------- |
| algoOrderId  | integer | Conditional      | Id of the algo order; Either `algoOrderId` or `clientOrderId` is required. If both are passed, `algoOrderId` will be used.|
|clientAlgoOrderId  | integer | Conditional      | Client algo order Id as assigned by the user; Either `algoOrderId` or `clientAlgoOrderId` is required. If both are passed, `algoOrderId` will be used.| -->


## Get Algo Orders

**Limit: 10 requests per 1 second**

`
GET /v3/algo/orders
`

***Note: This v3 API using query string to pass parameter, please follow the instruction in [authentication](#authentication) section for `v3` API to generate the signature.
Get orders by customize conditions.  
- `INCOMPLETE` = `NEW` + `PARTIAL_FILLED`  
- `COMPLETED` = `CANCELLED` + `FILLED` + `REJECTED`
The `realizedPnl` field in response will only present the settled amount for futures orders. The return value default is null unless the input parameter `realizedPnl` set to `true`

> **Response**

```js
{
  "success": true,
  "data": {
    "rows": [
      {
        "leverage": 10,
        "algoOrderId": 2081697,
        "clientOrderId": 0,
        "rootAlgoOrderId": 2081697,
        "parentAlgoOrderId": 0,
        "symbol": "PERP_WOO_USDT",
        "orderTag": "default",
        "algoType": "POSITIONAL_TP_SL",
        "side": "BUY",
        "quantity": 0,
        "isTriggered": false,
        "triggerStatus": "NEW",
        "rootAlgoStatus": "NEW",
        "algoStatus": "NEW",
        "triggerPriceType": "USELESS",
        "triggerTime": "0",
        "totalExecutedQuantity": 0,
        "visibleQuantity": 0,
        "averageExecutedPrice": 0,
        "totalFee": 0,
        "feeAsset": "",
        "totalRebate": 0,
        "rebateAsset": "",
        "reduceOnly": false,
        "createdTime": "1720589170.566",
        "updatedTime": "1720589616.276",
        "isActivated": true,
        "childOrders": [
          {
            "leverage": 10,
            "algoOrderId": 2081698,
            "clientOrderId": 0,
            "rootAlgoOrderId": 2081697,
            "parentAlgoOrderId": 2081697,
            "symbol": "PERP_WOO_USDT",
            "orderTag": "default",
            "algoType": "TAKE_PROFIT",
            "side": "BUY",
            "quantity": 0,
            "isTriggered": false,
            "triggerPrice": 0.14977,
            "triggerStatus": "USELESS",
            "type": "CLOSE_POSITION",
            "rootAlgoStatus": "NEW",
            "algoStatus": "NEW",
            "triggerPriceType": "MARK_PRICE",
            "triggerTime": "0",
            "totalExecutedQuantity": 0,
            "visibleQuantity": 0,
            "averageExecutedPrice": 0,
            "totalFee": 0,
            "feeAsset": "",
            "totalRebate": 0,
            "rebateAsset": "",
            "reduceOnly": true,
            "createdTime": "1720589170.561",
            "updatedTime": "1720589616.268",
            "isActivated": true,
            "positionSide": "SHORT",
            "marginMode": "ISOLATED"
          },
          {
            "leverage": 10,
            "algoOrderId": 2081699,
            "clientOrderId": 0,
            "rootAlgoOrderId": 2081697,
            "parentAlgoOrderId": 2081697,
            "symbol": "PERP_WOO_USDT",
            "orderTag": "default",
            "algoType": "STOP_LOSS",
            "side": "BUY",
            "quantity": 0,
            "isTriggered": false,
            "triggerPrice": 0.22465,
            "triggerStatus": "USELESS",
            "type": "CLOSE_POSITION",
            "rootAlgoStatus": "NEW",
            "algoStatus": "NEW",
            "triggerPriceType": "MARK_PRICE",
            "triggerTime": "0",
            "totalExecutedQuantity": 0,
            "visibleQuantity": 0,
            "averageExecutedPrice": 0,
            "totalFee": 0,
            "feeAsset": "",
            "totalRebate": 0,
            "rebateAsset": "",
            "reduceOnly": true,
            "createdTime": "1720589170.564",
            "updatedTime": "1720589616.270",
            "isActivated": true,
            "positionSide": "SHORT",
            "marginMode": "ISOLATED"
          }
        ],
        "positionSide": "SHORT",
        "marginMode": "ISOLATED"
      }
    ],
    "meta": {
      "total": 3,
      "records_per_page": 25,
      "current_page": 1
    }
  },
  "timestamp": 1720589635338
}

```

**Parameters**


| Name      | Type      | Required       | Description                                                                       |
| --------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| algoType         | string | Y        | `STOP/OCO/TRAILING_STOP/BRACKET`|`POSITIONAL_TP_SL`                              |
| createdTimeEnd   | timestamp | N              | end time range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| createdTimeStart     | timestamp | N              | start time range that you wish to query, noted that the time stamp is a 13-digits timestamp.   |
| isTriggered | boolean | N              | true or false                                                                     |
| orderTag | string    | N              | An optional tag for this order.                                                   |
| page      | number    | N (default: 1) | pag of query pagination                                                           |
| realizedPnl| boolean | N              | Decide if return data calculate realized pnl value for the futures order.         |
| side      | string    | N              | `BUY`/`SELL`                                                                      |
| size      | number    | N (default: 25)             | size for query pagination                                                         |
| status    | enum      | N              | `NEW`/`CANCELLED`/`PARTIAL_FILLED`/`FILLED`/`REJECTED`/`INCOMPLETE`/`COMPLETED`   |
| symbol    | string    | N              |                                                                                   |
| orderType| string    | N              | `LIMIT`/`MARKET`                          |



<!-- ## Get algo orders_V3

**Limit: 10 requests per 1 second**  


`
GET /v3/trade/algoOrders
`

Get orders by customizable conditions.  For filtering by status, one can reference special bundled statuses below for ease of access of open (i.e. INCOMPLETE) orders or COMPLETED orders.

`INCOMPLETE` = `NEW` + `PARTIAL_FILLED`

`COMPLETED` = `CANCELLED` + `FILLED` + `REJECTED`


> **Response**

```js
{
    "success": true,
    "data": {
        "meta": {
            "total": 2,
            "recordsPerPage": 25,
            "currentPage": 1
        },
        "rows": [
            {
                "algoOrderId": 792419,
                "clientAlgoOrderId": 0,
                "rootAlgoOrderId": 792419,
                "parentAlgoOrderId": 0,
                "symbol": "SPOT_WOO_USDT",
                "algoOrderTag": "default",
                "algoType": "TRAILING_STOP",
                "side": "SELL",
                "positionSide": "BOTH",
                "quantity": 1,
                "isTriggered": false,
                "triggerStatus": "USELESS",
                "type": "MARKET",
                "rootAlgoStatus": "NEW",
                "algoStatus": "NEW",
                "triggerPriceType": "MARKET_PRICE",
                "triggerTime": "0",
                "totalExecutedQuantity": 0,
                "averageExecutedPrice": 0,
                "totalFee": 0,
                "feeAsset": "",
                "totalRebate":0,
                "rebateAsset":"",
                "reduceOnly": false,
                "createdTime": 1696595221136,
                "updatedTime": 1696595221136,
                "isActivated": false,
                "callbackRate": 0.03,
                "activatedPrice": 0.21
            },
            {
                "algoOrderId": 792407,
                "clientAlgoOrderId": 0,
                "rootAlgoOrderId": 792407,
                "parentAlgoOrderId": 0,
                "symbol": "SPOT_WOO_USDT",
                "algoOrderTag": "default",
                "algoType": "BRACKET",
                "side": "BUY",
                "quantity": 100,
                "isTriggered": false,
                "triggerStatus": "SUCCESS",
                "type": "LIMIT",
                "positionSide": "BOTH",
                "status": "NEW",
                "rootAlgoStatus": "NEW",
                "algoStatus": "NEW",
                "triggerPriceType": "MARKET_PRICE",
                "price": 0.15,
                "triggerTime": "0",
                "totalExecutedQuantity": 0,
                "averageExecutedPrice": 0,
                "totalFee": 0,
                "totalRebate":0,
                "rebateAsset":"",
                "feeAsset": "WOO",
                "reduceOnly": false,
                "createdTime": 1696589756133,
                "updatedTime": 1696589756247,
                "childOrders": [
                    {
                        "algoOrderId": 792408,
                        "clientAlgoOrderId": 0,
                        "rootAlgoOrderId": 792407,
                        "parentAlgoOrderId": 792407,
                        "symbol": "SPOT_WOO_USDT",
                        "algoOrderTag": "default",
                        "algoType": "TP_SL",
                        "side": "SELL",
                        "positionSide": "BOTH",
                        "quantity": 0,
                        "isTriggered": false,
                        "triggerStatus": "USELESS",
                        "rootAlgoStatus": "NEW",
                        "algoStatus": "NEW",
                        "triggerPriceType": "MARKET_PRICE",
                        "triggerTime": "0",
                        "totalExecutedQuantity": 0,
                        "visibleQuantity": 0,
                        "averageExecutedPrice": 0,
                        "totalFee": 0,
                        "feeAsset": "",
                        "totalRebate":0,
                        "rebateAsset":"",
                        "reduceOnly": false,
                        "createdTime": 1696589756128,
                        "updatedTime": 1696589756128,
                        "isActivated": false,
                        "childOrders": [
                            {
                                "algoOrderId": 792409,
                                "clientAlgoOrderId": 0,
                                "rootAlgoOrderId": 792407,
                                "parentAlgoOrderId": 792408,
                                "symbol": "SPOT_WOO_USDT",
                                "algoOrderTag": "default",
                                "algoType": "TAKE_PROFIT",
                                "side": "SELL",
                                "positionSide": "BOTH",
                                "quantity": 0,
                                "isTriggered": false,
                                "triggerPrice": 0.3,
                                "triggerStatus": "USELESS",
                                "type": "MARKET",
                                "rootAlgoStatus": "NEW",
                                "algoStatus": "NEW",
                                "triggerPriceType": "MARKET_PRICE",
                                "triggerTime": "0",
                                "totalExecutedQuantity": 0,
                                "visibleQuantity": 0,
                                "averageExecutedPrice": 0,
                                "totalFee": 0,
                                "feeAsset": "",
                                "totalRebate":0,
                                "rebateAsset":"",
                                "reduceOnly": true,
                                "createdTime": 1696589756118,
                                "updatedTime": 1696589756118,
                                "isActivated": false
                            },
                            {
                                "algoOrderId": 792410,
                                "clientAlgoOrderId": 0,
                                "rootAlgoOrderId": 792407,
                                "parentAlgoOrderId": 792408,
                                "symbol": "SPOT_WOO_USDT",
                                "algoOrderTag": "default",
                                "algoType": "STOP_LOSS",
                                "side": "SELL",
                                "positionSide": "BOTH",
                                "quantity": 0,
                                "isTriggered": false,
                                "triggerPrice": 0.1,
                                "triggerStatus": "USELESS",
                                "type": "MARKET",
                                "rootAlgoStatus": "NEW",
                                "algoStatus": "NEW",
                                "triggerPriceType": "MARKET_PRICE",
                                "triggerTime": "0",
                                "totalExecutedQuantity": 0,
                                "visibleQuantity": 0,
                                "averageExecutedPrice": 0,
                                "totalFee": 0,
                                "feeAsset": "",
                                "totalRebate":0,
                                "rebateAsset":"",
                                "reduceOnly": true,
                                "createdTime": 1696589756123,
                                "updatedTime": 1696589756123,
                                "isActivated": false
                            }
                        ]
                    }
                ]
            },
            ...
        ]
    },
    "timestamp": 1696598461952
}
```

**Parameters**


| Name | Type   | Required | Description                           |
| ---- | ------ | -------- | ------------------------------------- |
|symbol|string|No (default: all symbols)|Symbol name|
|side|string|No (default: both BUY and SELL)|BUY/SELL|
|positionSide|string|No (default: all position sides)|BOTH for one way mode; LONG or SHORT for hedge mode; Only applicable to perpetual instruments|
|algoType|string|No (default: all algo order types)|STOP/OCO/TRAILING\_STOP/POSITIONAL\_TP\_SL/TP\_SL/BRACKET/STOP\_BRACKET|
|orderType|string|No (default: all order types)|LIMIT/MARKET|
|isTriggered|string|No (default: both triggered and not triggered)|true/false|
|algoOrderTag|string|No|Order tag|
|realizedPnl|boolean|No (default: false)|Whether to return order’s realized pnl|
|status|string|No (default: all statuses)|NEW/CANCELLED/PARTIAL\_FILLED/FILLED/REJECTED/INCOMPLETE/COMPLETED|
|startTime|integer|No|Start timestamp in Unix timestamp format in milliseconds|
|endTime|integer|No|End timestamp in Unix timestamp format in milliseconds|
|page|integer|No (default: 1)|Page number|
|size|integer|No (default: 25)|Data size per page|
 -->


## Edit Algo Order 

**Limit: 5 requests per 1 second**

`
PUT /v3/algo/order/:order_id
`

***Note that for v3 API with json body POST method, please follow the instruction in [authentication](#authentication) section for `v3` API to generate the signature.
***Please use `string` type for value input field to remain data accurancy.

The API allow you to edit the trigger price and the quantity of the selected algo order. You must input at least one of it in the request body.



> **Response**

```js
{
    "success": true,
    "data": {
        "success": true,
        "status": "EDIT_SENT"
    },
    "timestamp": 1676277871935
}
```
> **Request**

```js
{
  "activatedPrice": "200",
  "callbackRate": "200",
  "callbackValue": "200",
  "childOrders": [
    {
      "algoOrderId": 123456,
      "price": "1000",
      "quantity": "1000",
      "triggerPrice": "1000"
    }
  ],
  "price": "1000",
  "quantity": "1000",
  "triggerPrice": "1000"
}

```



**Parameters**

| Name             | Type   | Required | Description                                                                            |
| ---------------- | ------ | -------- | -------------------------------------------------------------------------------------- |
| oid              | number | Y        | The order_id `oid` that you wish to query                                              |
| activatedPrice   | string | N        | activated price for algoType=TRAILING_STOP                                               |
| callbackRate     | string | N        | new callback rate, only for algoType=TRAILING_STOP, i.e. the value = 0.1 represent to 10%. |
| callbackValue    | string | N        | new callback value, only for algoType=TRAILING_STOP, i.e. the value = 100                  |
| childOrders      | array  | N        | The array list of the child orders, only for algoType=POSITIONAL_TP_SL or TP_SL        |
| price            | number | N        | New price of the algo order.                                                           |
| quantity         | number | N        | New quantity of the algo order.                                                             |
| triggerPrice    | number | N        | New trigger price of the algo order.                                                         |

## Edit Algo Order by client_order_id

**Limit: 5 requests per 1 second**

`
PUT /v3/algo/order/client/:client_order_id
`

***Note that for v3 API with json body POST method, please follow the instruction in [authentication](#authentication) section for `v3` API to generate the signature.
***Please use `string` type for value input field to remain data accurancy.

The API allow you to edit the price and the quantity of the selected algo order. You must input at least one of it in the request body.




> **Response**

```js
{
  "code": 0,
  "data": {
    "status": "string",
    "success": true
  },
  "message": "string",
  "success": true,
  "timestamp": 0
}
```
> **Request**

```js
{
  "activatedPrice": "200",
  "callbackRate": "200",
  "callbackValue": "200",
  "childOrders": [
    {
      "algoOrderId": 123456,
      "price": "1000",
      "quantity": "1000",
      "triggerPrice": "1000"
    }
  ],
  "price": "1000",
  "quantity": "1000",
  "triggerPrice": "1000"
}

```



**Parameters**

| Name             | Type   | Required | Description                                                                            |
| ---------------- | ------ | -------- | -------------------------------------------------------------------------------------- |
| oid              | number | Y        | The order_id `oid` that you wish to query                                              |
| activatedPrice   | string | N        | activated price for algoType=TRAILING_STOP                                               |
| callbackRate     | string | N        | new callback rate, only for algoType=TRAILING_STOP, i.e. the value = 0.1 represent to 10%. |
| callbackValue    | string | N        | new callback value, only for algoType=TRAILING_STOP, i.e. the value = 100                  |
| childOrders      | array  | N        | The array list of the child orders, only for algoType=POSITIONAL_TP_SL or TP_SL        |
| price            | number | N        | New price of the algo order.                                                           |
| quantity         | number | N        | New quantity of the algo order.                                                             |
| triggerPrice    | number | N        | New trigger price of the algo order.                                                         |



## Get Trade

**Limit: 10 requests per 1 second**

`
GET /v1/client/trade/:tid
`

Get specific transaction detail by `id`.
(The data fetch from this API only contains past 3 months data, if you need the data more than 3 months, please submit the ticket in the support center).


> **Response**

```js
{
    "success": true,
    "id": 1,
    "symbol": "SPOT_BTC_USDT",
    "fee": 0.0001,
    "fee_asset": "BTC", // fee. use Base (BTC) as unit when BUY, use Quote (USDT) as unit when SELL
    "side": "BUY",
    "order_id": 2,
    "executed_price": 123,
    "executed_quantity": 0.05,
    "is_maker": 0,
    "executed_timestamp": "1567382400.000"  // Unix epoch time in seconds
}
```

**Parameters**

| Name | Type   | Required | Description                                 |
| ---- | ------ | -------- | ------------------------------------------- |
| tid  | number | Y        | The transaction id `tid` that you wish to query |


## Get Trades

**Limit: 10 requests per 1 second**

`
GET /v1/order/:oid/trades
`

Get trades by `order_id`

> **Response**

```js
{
    "success": true,
    "rows": [
        {
            "id": 5, // transaction id
            "symbol": "SPOT_BTC_USDT",
            "order_id": 211,
            "order_tag": "default",
            "executed_price": 10892.84,
            "executed_quantity": 0.002,
            "is_maker": 0,
            "side": "SELL",
            "fee": 0,
            "fee_asset": "USDT", // use Base (BTC) as unit when BUY, use Quote (USDT) as unit when SELL
            "executed_timestamp": "1566264290.250"  // Unix epoch time in seconds
        }
    ]
}
```

**Parameters**


| Name     | Type   | Required | Description                           |
| -------- | ------ | -------- | ------------------------------------- |
| oid      | number | Y        | The order id `oid` that you wish to query |


## Get Trade History

**Limit: 10 requests per 1 second**

`
GET /v1/client/trades
`

Return client’s trade history in a range of time. 
(The data fetch from this API only contains past 3 months data, if you need the data more than 3 months, please user [Get Archived Trade History](#get-archived-trade-history)).

> **Response**

```js
{
    "success": true,
    "meta": {
        "total": 31,
        "records_per_page": 25,
        "current_page": 1
    },
    "rows": [
        {
            "id": 5, // transaction id
            "symbol": "SPOT_BTC_USDT",
            "order_id": 211,
            "order_tag": "default",
            "executed_price": 10892.84,
            "executed_quantity": 0.002,
            "is_maker": 0,
            "side": "SELL",
            "fee": 0,
            "fee_asset": "USDT", // use Base (BTC) as unit when BUY, use Quote (USDT) as unit when SELL
            "executed_timestamp": "1566264290.250"  // Unix epoch time in seconds
        },
        // ....skip (total 25 items in one page)
    ]
}
```

**Parameters**

| Name      | Type      | Required       | Description                                                                       |
| --------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| symbol    | string    | N              |                                                                                   |
| order_tag | string    | N              | An optional tag for this order.                                                   |
| start_t   | timestamp | N              | start time range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| end_t     | timestamp | N              | end time range that you wish to query, noted that the time stamp is a 13-digits timestamp.   |
| page      | number    | N (default: 1) | the page you wish to query.                                                           |
| size   | number | N (default: 25)  |                                  |


## Get Archived Trade History 

**Limit: 1 requests per 1 second**

`
GET /v1/client/hist_trades
`

Return client’s trade history in a range of time.
(The data fetch from this API contains all time historical data).

> **Response**

```js
{
    "success": true,
    "data": [
        {
            "id": 217714629, // transaction id
            "symbol": "SPOT_BTC_USDT",
            "order_id": 211,
            "order_tag": "default",
            "executed_price": 10892.84,
            "executed_quantity": 0.002,
            "is_maker": 0,
            "side": "SELL",
            "fee": 0,
            "fee_asset": "USDT", // use Base (BTC) as unit when BUY, use Quote (USDT) as unit when SELL
            "executed_timestamp": "1566264290.250"  // Unix epoch time in seconds
        },
        // ....skip (total 25 items in one page)
    ]
}
```

**Parameters**

| Name      | Type      | Required       | Description                                                                       |
| --------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| symbol    | string    | N              |                                                                                   |
| start_t   | timestamp | Y              | start time range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| end_t     | timestamp | Y              | end time range that you wish to query, noted that the time stamp is a 13-digits timestamp.   |
| fromId      | number    | N (default: 1) | fromId is the trade id of the the record. It should be use as a cursor, so searching for trades starting with that trade id query.          |
| limit   | number | N (default: 25)  |                                  |


## Get Staking Yield History

**Limit: 10 requests per 1 second**

`
GET /v1/staking/yield_history
`

Return client’s staking yield history

> **Response**

```js
{
  "rows": [
    {
      "id": 53173,
      "token": "WOO",
      "user_id": 10174,
      "staking_size": 30100.00000000,
      "annual_reward": "0.24294%",
      "yield_amount": 0.20034259,
      "yield_time": "1673481600.000"
    },
    {
      "id": 53029,
      "token": "WOO",
      "user_id": 10174,
      "staking_size": 30100.00000000,
      "annual_reward": "0.24294%",
      "yield_amount": 0.20034259,
      "yield_time": "1673395200.000"
    },
    {
      "id": 52885,
      "token": "WOO",
      "user_id": 10174,
      "staking_size": 30100.00000000,
      "annual_reward": "0.24294%",
      "yield_amount": 0.20034259,
      "yield_time": "1673308800.000"
    },
    {
      "id": 52741,
      "token": "WOO",
      "user_id": 10174,
      "staking_size": 30100.00000000,
      "annual_reward": "0.242572%",
      "yield_amount": 0.20003858,
      "yield_time": "1673222400.000"
    },
    {
      "id": 52597,
      "token": "WOO",
      "user_id": 10174,
      "staking_size": 30100.00000000,
      "annual_reward": "0.242572%",
      "yield_amount": 0.20003858,
      "yield_time": "1673136000.000"
    }
  ],
  "meta": {
    "total": 582,
    "records_per_page": 5,
    "current_page": 1
  },
  "success": true
}
```

**Parameters**

| Name      | Type      | Required       | Description                                                                       |
| --------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| page      | number    | N (default: 1) | the page you wish to query.                                                       |
| size      | number    | N (default: 25) | the page size you wish to query, default = 25, 1000 at max.                        |
| token     | string    | Y              | i.e: WOO                                                                          |

## Get Current Holding

**Limit: 10 requests per 1 seconds**

`
GET /v1/client/holding
`

Holding summary of the client. Note that the number in holding could be negative, it means how much the client owes to WOO X.


> **Response**

```js
{
    "success": true,
    "holding": {
        "BTC": 1.014,
        "USDT": -26333.207589999998,
        "BCHABC": 2
    }
}
```

**Parameters**

None


## Get Current Holding v2

**Limit: 10 requests per 1 seconds**

`
GET /v2/client/holding
`

<font color=#0000FF>** Note: This API will be deprecated at the end of 2023 Q1, please find the replacement API in </font> [Get Current Holding Get Balance - New](#get-current-holding-get-balance-new)
Holding summary of client. Note that the number in holding could be negative, it means how much client owed to WOO X.



> **Response**

```js
{
    "holding":[
        {
            "token":"BTC",
            "holding":0.00590139,
            "frozen":0.0,
            "interest":0.0,
            "outstanding_holding":-0.00080,
            "pending_exposure":0.0,
            "opening_cost":-126.36839957,
            "holding_cost":-125.69703515,
            "realised_pnl":73572.86125165,
            "settled_pnl":73573.5326161,
            "fee_24_h":0.01432411,
            "settled_pnl_24_h":0.67528081,
            "updated_time":"1675220398"
        },{
            "token":"UNI",
            "holding":0.00000000,
            "frozen":0.00000000,
            "interest":0.00000000,
            "outstanding_holding":0.00000000,
            "pending_exposure":0.00000000,
            "opening_cost":0,
            "holding_cost":0,
            "realised_pnl":0,
            "settled_pnl":0,
            "fee_24_h":0,
            "settled_pnl_24_h":0,
            "updated_time":"1655269545"
        }   
    ],
    "success":true
}
```

**Parameters**

| Name | Type | Required | Description                                                                    |
| ---- | ---- | -------- | ------------------------------------------------------------------------------ |
| all  | enum | N        | `true`/`false`. If `true` then will return all tokens even if balance is empty. |

## Get Current Holding (Get Balance) - New

**Limit: 100 requests per 1 mins**

`
GET /v3/balances
`

<!-- <font color=#0000FF>** Note: This API will be released with WOO X New Margin Ratio Program in Jan 2023, currently on available in staging environment </font> -->
Holding summary of client. Note that the number in holding could be negative, it means how much client owed to WOO X.
The API is design to replace the legacy API [Get Current Holding](#get-current-holding) and [Get Current Holding v2](#get-current-holding-v2)

> **Response**

```js
{
  "success": true,
  "data": {
    "holding": [
      {
        "token": "WOO",
        "holding": 169684.96645139,
        "frozen": 0.0,
        "staked": 1304330.65079109,
        "unbonding": 0.0,
        "vault": 0.0,
        "interest": 0.0,
        "pendingShortQty": 0.0,
        "pendingLongQty": 0.0,
        "availableBalance": 169684.96645139,
        "averageOpenPrice": 0.0,
        "markPrice": 0.22446,
        "launchpadVault": 0.0,
        "earn": 0.0,
        "pnl24H": 0.0,
        "fee24H": 0.0,
        "updatedTime": 1715126422.125
      }
    ],
    "userId": 11446,
    "applicationId": "1ca13dff-f2d6-4fa4-a382-5ce1a79b2bc0"
  },
  "timestamp": 1715197222107
}
```

**Parameters**


**Parameters**

| Name          | Type      | Required       | Description                                                                       |
| ----------    | --------- | -------------- | --------------------------------------------------------------------------------- |
| token         | string    | N              | Use the parameter in query string format (i.e. /v3/balance?token=WOO). If the parameter is empty (or not passed) it will return all token's holding.           |




## Get Account Information

**Limit: 10 requests per 60 seconds**

`
GET /v1/client/info
`

<font color=#0000FF>** Note: This API will be deprecated at the end of 2023 Q1, please find the replacement API in </font> [Get Account Information - New](#get-account-information-new)
Get account information such as account name, leverage, current exposure ... etc.


> **Response**

```js
{
    
    "success": true,
    "application": {
        "application_id": "8935820a-6600-4c2c-9bc3-f017d89aa173",
        "account": "CLIENT_ACCOUNT_01",
        "alias": "CLIENT_ACCOUNT_01",
        "account_mode":"FUTURES" //account mode
        "leverage": 5,
        "taker_fee_rate": 0,
        "maker_fee_rate": 0,
        "futures_leverage": 5,
        "futures_taker_fee_rate": 0,
        "futures_maker_fee_rate": 0,
        "otpauth": false
    },
    "margin_rate": 1000
}
```

**Parameters**

None

## Get Account Information - New 

**Limit: 10 requests per 60 seconds**

`
GET /v3/accountinfo
`

<!-- <font color=#0000FF>** Note: This API will be released with WOO X New Margin Ratio Program in Jan 2023, currently on available in staging environment. </font> -->
Get account information such as account name, leverage, current exposure ... etc.
The API is design to replace the legacy API [Get Account Information](#get-account-information)

The `referrerID` in the response represent the referral code that the user used to sign up, subaccount would pass main account referrerID.
The `accountType` in the response represent the account type is `Main` account or `Subaccount` 

> **Response**

```js
{
    "success": true,
    "data": {
        "applicationId": "f5f485c7-6ca5-4189-8efe-e842cdc50498",
        "account": "",
        "alias": "",
        "accountMode": "FUTURES",
        "positionMode": "HEDGE",
        "leverage": null, 
        "takerFeeRate": 0,
        "makerFeeRate": 0,
        "interestRate": 1,
        "futuresTakerFeeRate": 0,
        "futuresMakerFeeRate": 0,
        "otpauth": true,
        "marginRatio": 7739.3757,
        "openMarginRatio": 7739.3757,
        "initialMarginRatio": 1.0006,
        "maintenanceMarginRatio": 0.0126,
        "totalCollateral": 1146085.27376211,
        "freeCollateral": 1145937.09993548,
        "totalAccountValue": 1924716.18982933, // include isolated frozen and unrealized pnl
        "totalVaultValue": 778216.06557667,
        "totalStakingValue": 0,
        "referrerID": "",
        "accountType": "Main",
        "totalLaunchpadVaultValue": 0,
        "totalEarnValue": 0
    },
    "timestamp": 1714284212689
}
```

**Parameters**

None

## Get Token History 

**Limit: 10 requests per 60 seconds**

`
GET /v1/client/transaction_history
`

Get account token balance change history, including `YIELD_TO_BALANCE`, `TRADING_FEE`, `REALIZED_PNL`, `SPOT_TRADING`, `FUTURES_TRADING`, `FUNDING_FEE` 

> **Response**

```js
{
    "success": true,
    "data": {
        "rows": [
            {
                "id": 1606724,
                "type": "YIELD_TO_BALANCE",
                "token": "WOO",
                "amount": 0.30029155,
                "timestamp": 1686528091385
            },
            {
                "id": 310949247,
                "type": "TRADING_FEE",
                "token": "USDT",
                "amount": -0.174587,
                "timestamp": 1686401821520
            },
            {
                "id": 1686355200000,
                "type": "REALIZED_PNL",
                "token": "USDT",
                "symbol": "PERP_WOO_USDT",
                "amount": -24.64824179,
                "timestamp": 1686355200000
            },
            {
                "id": 7284139,
                "type": "FUNDING_FEE",
                "token": "USDT",
                "amount": 0.02661496,
                "timestamp": 1686009921667
            },
            ...
        ],
        "meta": {
            "total": 65,
            "records_per_page": 25,
            "current_page": 1
        }
    },
    "timestamp": 1686544732777
}
```

**Parameters**

| Name          | Type      | Required       | Description                                                                       |
| ----------    | --------- | -------------- | --------------------------------------------------------------------------------- |
| type          | string    | N              | `WITHDRAW`/`DEPOSIT`/`FIAT_WITHDRAW`/`FIAT_DEPOSIT`/`EARN`/`VAULT_WITHDRAW`/`VAULT_DEPOSIT`/`YIELD_TO_BALANCE`/`CREDIT`/`DISTRIBUTION`/`REFERRAL`/`SUB_ACCOUNT_TRANSFER`/`REBATE`/`LIQUIDATION`/`SPECIAL`/`STAKING`/`UNSTAKING`/`UNSTAKING_FEE`/`INTEREST`/`CONVERT`/`FUNDING_FEE`/`SPOT_TRADING`/`TRADING_FEE`/`REALIZED_PNL`/`RFQ`                                                            |
| start_t       | timestamp | N              | start time range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| end_t         | timestamp | N              | end time range that you wish to query, noted that the time stamp is a 13-digits timestamp.   |
| page          | number    | N (default: 1) | the page you wish to query.                                                           |
| size   | number | N (default: 25)  |                                  |


## Get Account API Key & Permission

**Limit: 10 requests per 60 seconds**

`
GET usercenter/api/enabled_credential
`

Get api_key list and its permissions of the account.
The response will contain your API keys’ permissions based on the credentials.


> **Response**

```js
{
    "success": true,
    "data": {
        "rows": [
            {
                "account_name": "Main",
                "user_id": 10001,
                "api_key": "+Pxxxxxxxxxxxxxxxxxxxx==",
                "permission": "Read,"
            },
            {
                "account_name": "Main",
                "user_id": 10001,
                "api_key": "Hxxxxxxxxxxxxxxxxxxxx==",
                "permission": "Read,"
            },
            {
                "account_name": "Main",
                "user_id": 10001,
                "api_key": "Cxxxxxxxxxxxxxxxxxxxx==",
                "permission": "Read,"
            },
            {
                "account_name": "testSubAccount",
                "user_id": 10001,
                "api_key": "vxxxxxxxxxxxxxxxxxxxx==",
                "permission": "Read,Enable trade,"
            }
            ...
        ],
        "meta": {
            "total": 11,
            "records_per_page": 5,
            "current_page": 1
        }
    },
    "timestamp": 1685414636917
}
```

**Parameters**

None


## Get Buy Power

**Limit: 60 requests per 60 seconds**

`
GET /v3/buypower
`

Get buying power for selected symbol.

> **Response**

```js

{
  "success": true,
  "data": [
    {
        "symbol": "SPOT_BTC_USDT",
        "availableBaseQuantity": 1.2,
        "availableQuoteQuantity": 100,
    },
  ],
  "timestamp": 1575014255
}
```

**Parameters**

| Name  | Type   | Required | Description                                                  |
| ----- | ------ | -------- | ------------------------------------------------------------ |
| symbol  | string    | Y              | symbol that you wish to query                                    |

## Get Token Deposit Address

**Limit 60 requests per 60 seconds**

`
GET /v1/asset/deposit
`

Get your unique deposit address by token

> **Response**

```js
{
    "success": true,
    "address": "0x31d64B3230f8baDD91dE1710A65DF536aF8f7cDa",
    "extra": ""
}
```

**Parameters**

| Name  | Type   | Required | Description                                                  |
| ----- | ------ | -------- | ------------------------------------------------------------ |
| token | string | Y        | token name you want to deposit (can get it by /public/token) |



## Token Withdraw

**Limit 20 requests per 60 seconds**

`
POST /v1/asset/withdraw
`

Initiate a token withdrawal request, `amount` must less than or equal to `holding`


> **Response**

```js
{
    "success": true,
    "withdraw_id": "20200119145703654"
}
```

**Parameters**

| Name    | Type   | Required | Description                                                   |
| ------- | ------ | -------- | ------------------------------------------------------------- |
| token   | string | Y        | token name you want to withdraw (can get it by /public/token) |
| address | string | Y        | the address you want to withdraw                              |
| extra   | string | N        | address extra information such as MEMO or TAG                 |
| amount  | number | Y        | amount you want to withdraw, must less or equal than holding  |


## Token Withdraw V3

**Limit 20 requests per 60 seconds**

`
POST /v3/asset/withdraw
`

Initiate a token withdrawal request, `amount` must less than or equal to `holding`


> **Response**

```js
{
    "success": true,
    "data": {
        "withdrawId": "24040901514500001"
    },
    "timestamp": 1712627507204
}

```

**Parameters**

| Name    | Type   | Required | Description                                                   |
| ------- | ------ | -------- | ------------------------------------------------------------- |
| network   | string | Y       |To be obtained from the /public/token endpoint |
| address | string | Y        | the address you want to withdraw                              |
| extra   | string | N        | address extra information such as MEMO or TAG                 |
| amount  | number | Y        | amount you want to withdraw, must less or equal than holding  |
| balanceToken  | string | Y     |To be obtained from the /public/token endpoin |


## Internal token withdraw

**Limit: 20 requests per 60 seconds**

`
POST v1/asset/internal_withdraw
`

Initiate a token withdrawal request, amount must less than or equal to holding.
When using this API, please note that it cannot be utilized if address verification is enabled.


> **Response**


```js
{
    "success": true,
    "withdraw_id": "20200119145703654"
}
```

**Parameters**

| Name      | Type      | Required       | Description                                                                       |
| --------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| target_user_id    | string    | Yes              |    withdraw target user id                    
balance_token    | string    | Yes              |    balance token is token name you want to withdraw (can get it by /public/token)                                                 
| amount    | number    | Yes              |    amount you want to withdraw, must less or equal than holding                                       



## Cancel Withdraw Request

**Limit 5 requests per 60 seconds**

`
DELETE /v1/asset/withdraw
`

Cancel withdraw request when status is `NEW`


> **Response**

```js
{
    "success": true
}
```

**Parameters**

| Name | Type   | Required | Description                        |
| ---- | ------ | -------- | ---------------------------------- |
| id   | string | Y        | the withdraw id you want to cancel |


## Get Asset History

**Limit 10 requests per 60 seconds**

`
GET /v1/asset/history
`

Get asset history, includes token deposit/withdraw and collateral deposit/withdraw.


> **Response**

```js
{
    "success": true,
    "meta": {
        "records_per_page": 25,
        "current_page": 1
    },
    "rows": [
        {
            "created_time": "1579399877.041", // Unix epoch time in seconds
            "updated_time": "1579399877.041", // Unix epoch time in seconds
            "id": "202029292829292",
            "external_id": "202029292829292",
            "application_id": null,
            "token": "ETH",
            "target_address": "0x31d64B3230f8baDD91dE1710A65DF536aF8f7cDa",
            "source_address": "0x70fd25717f769c7f9a46b319f0f9103c0d887af0",
            "confirming_threshold":12,
            "confirmed_number":12,
            "extra": "",
            "type": "BALANCE",
            "token_side": "DEPOSIT",
            "amount": 1000,
            "tx_id": "0x8a74c517bc104c8ebad0c3c3f64b1f302ed5f8bca598ae4459c63419038106b6",
            "fee_token": null,
            "fee_amount": null,
            "status": "CONFIRMING"
        },
        {
            "created_time": "1579399877.041",
            "updated_time": "1579399877.041",
            "id": "20202020202020022",
            "external_id": "20202020202020022",
            "application_id": null,
            "token": "ETH",
            "target_address": "0x31d64B3230f8baDD91dE1710A65DF536aF8f7cDa",
            "source_address": "0x70fd25717f769c7f9a46b319f0f9103c0d887af0",
            "confirming_threshold":12,
            "confirmed_number":12,
            "extra": "",
            "type": "BALANCE",
            "token_side": "DEPOSIT",
            "amount": 100,
            "tx_id": "0x7f74c517bc104c8ebad0c3c3f64b1f302ed5f8bca598ae4459c63419038106c5",
            "fee_token": null,
            "fee_amount": null,
            "status": "COMPLETED"
        }
    ]
}
```

**Parameters**

| Name          | Type      | Required       | Description                                                                             |
| ----------    | --------- | -------------- | --------------------------------------------------------------------------------------- |
| id            | string    | N              | use when query specific transaction id (the result of withdrawal or internal transfer.) |
| token         | string    | N              | token name you want to search (can get it by /public/token)                             |
| balance_token | string    | N              | balance_token name you want to search (can get it by /public/token)                     |
| type          | string    | N              | `BALANCE`/`COLLATERAL`                                                                  |
| token_side    | string    | N              | `DEPOSIT`/`WITHDRAW`                                                                    |
| status        | string    | N              | `NEW`/`CONFIRMING`/`PROCESSING`/`COMPLETED`/`CANCELED`                                  |
| start_t       | timestamp | N              | start time range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| end_t         | timestamp | N              | end time range that you wish to query, noted that the time stamp is a 13-digits timestamp.   |
| page          | number    | N (default: 1) | the page you wish to query.                                                           |
| size   | number | N (default: 25)  |                                  |


## Margin Interest Rates

**Limit 10 requests per 60 seconds**

`
GET /v1/token_interest
`

Get the margin interest rate of each token.


> **Response**

```js
{
    "success": true,
    "rows": [
        {
            "token": "MATIC",
            "current_hourly_base_rate": "0.0001%",
            "est_hourly_base_rate": "0.0001%",
            "current_annual_base_rate": "0.876%",
            "est_annual_base_rate": "0.876%",
            "est_time": "1632394800.000"          // Unix epoch time in seconds
        },
        {
            "token": "USDT",
            "current_hourly_base_rate": "0.0008%",
            "est_hourly_base_rate": "0.0008%",
            "current_annual_base_rate": "7.008%",
            "est_annual_base_rate": "7.008%",
            "est_time": "1632394800.000"          // Unix epoch time in seconds
        },
        {
            "token": "WOO",
            "current_hourly_base_rate": "0.001%",
            "est_hourly_base_rate": "0.001%",
            "current_annual_base_rate": "8.76%",
            "est_annual_base_rate": "8.76%",
            "est_time": "1632394800.000"          // Unix epoch time in seconds
        },
        // ...
    ]
}
```

**Parameters**

None

## Margin Interest Rate of Token

**Limit 10 requests per 60 seconds**

`
GET /v1/token_interest/:token
`

Get the margin interest rate of the specific token.

> **Response**

```js
{
    "success": true,
    "info": {
        "token": "BTC",
        "current_hourly_base_rate": "0.0001%",
        "est_hourly_base_rate": "0.0001%",
        "current_annual_base_rate": "0.876%",
        "est_annual_base_rate": "0.876%",
        "est_time": "1632448800.000"         // Unix epoch time in seconds
    }
}
```

**Parameters**

| Name   | Type   | Required | Description          |
| ------ | ------ | -------- | -------------------- |
| token  | string | Y        | should be upper case |


## Get Interest History

**Limit 10 requests per 60 seconds**

`
GET /v1/interest/history
`

Get margin interest history. `loan_amount` will only appear when the side is `LOAN`.

> **Response**

```js
{
    "success": true,
    "meta": {
        "total": 349,
        "records_per_page": 25,
        "current_page": 1
    },
    "rows": [
       
       {
            "created_time": "1579399877.041", // Unix epoch time in seconds
            "updated_time": "1579399877.041", // Unix epoch time in seconds
            "token": "USDT",
            "application_id": null,
            "user_id": null,
            "status": "SUCCEED",
            "quantity": 0.20768326,
            "side": "LOAN",
            "interest": 0.01,
            "hourly_rate": "0.001%",
            "annual_rate": "8.76%",
            "loan_amount": 1000
        }
    ]
}
```

**Parameters**

| Name       | Type      | Required       | Description                                                                       |
| ---------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| token      | string    | N              | interest token which you want to query                                            |
| side       | string    | N              | `LOAN`/`REPAY`/`AUTO_REPAY`                                                       |
| start_t    | timestamp | N              | start time range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| end_t      | timestamp | N              | end time range that you wish to query, noted that the time stamp is a 13-digits timestamp.   |
| page       | number    | N (default: 1) | the page you wish to query.                                                           |
| size   | number | N (default: 25)  |                                  |


## Repay Interest

**Limit 10 requests per 60 seconds**

`
POST /v1/interest/repay
`

REPAY your margin interest.

> **Response**


```js
{
    "success": true,
}
```

**Parameters**

| Name       | Type      | Required       | Description                                                                       |
| ---------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| token      | string    | Y              | interest token which you want to repay                                            |
| amount     | number    | Y              | repayment amount                                                                  |




## Get referrals summary 

**Limit: 10 requests per 60 seconds**

`
GET /v3/referrals
`

Get referral information from each user you has referred.

> **Response**

```js
// The status of the recommender includes four types：Registered; Verified identity; Deposited; Traded
{
    "success": true,
    "data": {
        "rows": [
            {
                "referralId": 12509,
                "registerTime": "1643076873.484",
                "referralCode": "OJEDSSMU",
                "tradeStatus": "Traded",
                "earnWoo": 144.78597143,
                "earnUsdt": 0,
                "email": "staking-005_mas@woo.network",
                "extraBonus": 0,
                "extraBonusToken": "WOO",
                "previousVersionCommissionSum": 10.07981438,
                "previousVersionCommissionSumToken": "WOO"
            },
            {
                "referralId": 12192,
                "registerTime": "1639365757.173",
                "referralCode": "OJEDSSMU",
                "tradeStatus": "Traded",
                "earnWoo": 5729.91597424,
                "earnUsdt": 80.39717397,
                "email": "hazel@woo.network",
                "extraBonus": 0,
                "extraBonusToken": "WOO",
                "previousVersionCommissionSum": 5726.55249830,
                "previousVersionCommissionSumToken": "WOO"
            },
            {
                "referralId": 10588,
                "registerTime": "1678349096.000",
                "referralCode": "OJEDSSMU",
                "tradeStatus": "Traded",
                "earnWoo": 2058880.44406483,
                "earnUsdt": 54128.36568263,
                "email": "ken@woo.network",
                "extraBonus": 90,
                "extraBonusToken": "WOO",
                "previousVersionCommissionSum": 20160.36080029,
                "previousVersionCommissionSumToken": "WOO"
            },
            {
                "referralId": 10492,
                "registerTime": "1623203745.173",
                "referralCode": "DIHGLR3T",
                "tradeStatus": "Traded",
                "earnWoo": 0,
                "earnUsdt": 0.76927350,
                "email": "staking-010@woo.network",
                "extraBonus": 90,
                "extraBonusToken": "WOO",
                "previousVersionCommissionSum": null,
                "previousVersionCommissionSumToken": "WOO"
            }
        ],
        "meta": {
            "total": 4,
            "records_per_page": 25,
            "current_page": 1
        }
    },
    "timestamp": 1690192103430
}
```

**Parameters**

| Name          | Type      | Required       | Description                                                                       |
| ----------    | --------- | -------------- | --------------------------------------------------------------------------------- |
| page          | number    | N (default: 1) | the page you wish to query.                                                           |
| size   | number | N (default: 25)  |    
| from   |number| N| start time range that you wish to query, noted that the time stamp is a 13-digits timestamp.|
| to     |number| N|end time range that you wish to query, noted that the time stamp is a 13-digits timestamp.


## Get referral reward history 

**Limit: 10 requests per 60 seconds**

`
GET /v3/referral_rewards
`

Get referral reward information 

> **Response**

```js
{
    "success": true,
    "data": {
        "rows": [
            {
                "trade_date": "2023/07/17",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.47000000,
                "referral_commission": 53929.73957955,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 10588
            },
            {
                "trade_date": "2023/07/17",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 2038704.30927676,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 10588
            },
            {
                "trade_date": "2023/07/12",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 0.05004760,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 10588
            },
            {
                "trade_date": "2023/07/11",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 0.44951069,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 10588
            },
            {
                "trade_date": "2023/07/11",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.47000000,
                "referral_commission": 0.04858848,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/07/11",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 3.09802285,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/07/07",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 134.61965671,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 12509
            },
            {
                "trade_date": "2023/07/06",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 15.27442949,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 10588
            },
            {
                "trade_date": "2023/07/03",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.30000000,
                "referral_commission": 0.00811566,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/07/03",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 0.26545309,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/06/30",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.30000000,
                "referral_commission": 0.00144840,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/06/30",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 0.08224395,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/06/29",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.30000000,
                "referral_commission": 0.06940520,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/06/29",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 4.34149772,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/06/28",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.30000000,
                "referral_commission": 0.01434340,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/06/28",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 0.87468814,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/06/27",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.30000000,
                "referral_commission": 0.01949850,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 10492
            },
            {
                "trade_date": "2023/06/27",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.30000000,
                "referral_commission": 0.00900000,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 10588
            },
            {
                "trade_date": "2023/06/27",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 0.90196242,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 10588
            },
            {
                "trade_date": "2023/06/27",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.30000000,
                "referral_commission": 0.05706141,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/06/27",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 3.43115031,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 12192
            },
            {
                "trade_date": "2023/06/26",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.30000000,
                "referral_commission": 0.74977500,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 10492
            },
            {
                "trade_date": "2023/06/26",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.30000000,
                "referral_commission": 0.05399999,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 10588
            },
            {
                "trade_date": "2023/06/26",
                "referral_receive_percentage": 0,
                "referrer_receive_percentage": 0,
                "referral_rate": 0.00100000,
                "referral_commission": 2.78932410,
                "status": "Credited",
                "reward_token": "WOO",
                "referral_tier": 0,
                "referral_program": "AFFILIATE",
                "referral_id": 10588
            },
            {
                "trade_date": "2023/06/26",
                "referral_receive_percentage": 0.50000000,
                "referrer_receive_percentage": 0.50000000,
                "referral_rate": 0.30000000,
                "referral_commission": 0.06862500,
                "status": "Credited",
                "reward_token": "USDT",
                "referral_tier": 5,
                "referral_program": "TIER",
                "referral_id": 12192
            }
        ],
        "meta": {
            "total": 79,
            "records_per_page": 25,
            "current_page": 1
        }
    },
    "timestamp": 1690273370109
}
```

**Parameters**

| Name          | Type      | Required       | Description                                                                       |
| ----------    | --------- | -------------- | --------------------------------------------------------------------------------- |
| page          | number    | N (default: 1) | the page you wish to query.                                                           |
| size   | number | N (default: 25)  |    
| from   |number| N| start time range that you wish to query, noted that the time stamp is a 13-digits timestamp.|
| to     |number| N|end time range that you wish to query, noted that the time stamp is a 13-digits timestamp.
                              |
                              |


## Get Subaccounts

**Limit: 10 requests per 60 seconds**

`
GET /v1/sub_account/all
`

Get subaccount list.


> **Response**

```js
{
    "rows": [
        {
            "application_id": "6b43de5c-0955-4887-9862-d84e4689f9fe",
            "account": "2",
            "created_time": "1606897264.994"
        },
        {
            "application_id": "5b0df321-3aaf-471f-a386-b922a941d17d",
            "account": "1",
            "created_time": "1606897264.994"
        },
        {
            "application_id": "de25e672-f3e8-4ddc-b264-75d243cb2b9c",
            "account": "test",
            "created_time": "1606897264.994"
        }
    ],
    "success": true
}
```
**Permission**

Main account only.

**Parameters**

None



## Get Assets of Subaccounts

**Limit: 10 requests per 60 seconds**

`
GET /v1/sub_account/assets 
`

Get assets summary of all subaccounts (including main account).

> **Response**

```js
{
    "rows": [
        {
            "application_id": "0b297f58-9d3e-4c91-95cd-863329631b79",
            "account": "Main",
            "usdt_balance": 0.0
        }
    ],
    "success": true
}
```
**Permission**

Main account only.

**Parameters**

None



## Get Asset Details from a Subaccount

**Limit: 10 requests per 60 seconds**

`
GET /v1/sub_account/asset_detail
`

Get assets details from a subaccounts.


> **Response**

```js
{
    "balances": {
        "BTC": {
            "holding": 0.0,
            "frozen": 0.0,
            "interest": 0.0,
            "staked": 0.0,
            "unbonding": 0.0,
            "vault": 0.0
        },
        "WOO": {
            "holding": 4172706.29647137,
            "frozen": 0.0,
            "interest": 0.0,
            "staked": 51370692,
            "unbonding": 0.0,
            "vault": 0.0
        },
        "BNB": {
            "holding": 0.00070154,
            "frozen": 0.0,
            "interest": 0.0,
            "staked": 0.0,
            "unbonding": 0.0,
            "vault": 0.0
        },
        "ETH": {
            "holding": 0.0,
            "frozen": 0.0,
            "interest": 0.0,
            "staked": 0.0,
            "unbonding": 0.0,
            "vault": 0.0
        },
        "USDT": {
            "holding": 14066.5839369,
            "frozen": 0.0,
            "interest": 0.0,
            "staked": 0.0,
            "unbonding": 0.0,
            "vault": 0.0
        }
    },
    "account": "test",
    "success": true,
    "application_id": "e074dd6b-4c03-49be-937f-856472f7a6cb"
}
```
**Permission**

Main or Subaccounts.

**Parameters**


| Name      | Type      | Required       | Description                                         |
| --------- | --------- | -------------- | ----------------------------------------------------|
| application_id   | string | Y        |  application id for an account, user can find it from WOO X console. |



## Get IP Restriction

**Limit: 10 requests per 10 seconds**

`
GET /v1/sub_account/ip_restriction
`

Get allowed IP list of a subaccount's API Key.


> **Response**

```js
{
    "rows": [
        {
            "ip_list": "60.248.33.61,1.2.3.4,100.100.1.1,100.100.1.2,100.100.1.3,100.100.1.4,210.64.18.77",
            "api_key": "plXHR+GwX0u8UG/GwMjLsQ==",
            "update_time": "1644553230.916",
            "restrict": true
        }
    ],
    "meta": {
        "total": 1,
        "records_per_page": 25,
        "current_page": 1
    },
    "success": true
}
```
**Permission**

Main or Subaccounts.

**Parameters**


| Name      | Type      | Required       | Description                                         |
| --------- | --------- | -------------- | ----------------------------------------------------|
| application_id   | string | N        |  from WOO X console |
| api_key          | string | N        |  created from WOO X console |


## Get Transfer History
**Limit: 20 requests per 60 seconds**

`
GET /v1/asset/main_sub_transfer_history
`

Get transfer history between main account and subaccounts.  

> **Response**

```js

{
    "success":true,
    "data":{
        "rows":[
            {
                "id":225,
                "token":"USDT",
                "amount":1000000,
                "status":"COMPLETED",
                "from_application_id":"046b5c5c-5b44-4d27-9593-ddc32c0a08ae",
                "to_application_id":"082ae5ae-e26a-4fb1-be5b-03e5b4867663",
                "from_user":"Main",
                "to_user":"av",
                "created_time":"1642660941.534",
                "updated_time":"1642660941.950"
            },
            // ....skip (total 25 items in one page)
        ],
        "meta":{
            "total":7,
            "records_per_page":5,
            "current_page":1
        }
    }
}
```
**Permission**

Main or Subaccounts.

**Parameters**


| Name      | Type      | Required       | Description                                                                       |
| --------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| start_t   | timestamp | N              | start time range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| end_t     | timestamp | N              | end time range that you wish to query, noted that the time stamp is a 13-digits timestamp.   |
| page      | number    | N (default: 1) | the page you wish to query.                                                           |
| size   | number | N (default: 25)  |                                  |




## Transfer Assets 

**Limit: 20 requests per 60 seconds**
`
POST /v1/asset/main_sub_transfer
`

Transfer asset between main account and subaccounts.  


> **Response**

```js
{
    "success": true,
    "id": 200
}
```
**Permission**

Main or Subaccounts.

**Parameters**


| Name      | Type      | Required       | Description                                                                       |
| --------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| token   | string | Y        | token name you want to transfer (can get it by /public/token) |
| amount  | number | Y        | amount you want to transfer  |
| from_application_id      | string    | Y | application id you want to transfer from                                                           |
| to_application_id      | string    | Y | application id you want to transfer to                                                           |



## Get LtV info

**Limit: 20 requests per 60 seconds**
`
POST /v1/asset/ltv
`

For credit user to know whether need to deposit more funds to the platform if I want to withdraw.


> **Response**

```js
{
    "user_id": 12136,
    "success": true,
    "ltv_threshold": 0.6,
    "wallet_total_collateral": 1890719757.24550000,
    "credit": 0.00000000,
    "staking_woo_collateral": 0,
    "ltv": 0.00000000,
    "share_credit_user_ltv_infos": [
        {
            "user_id": 12136,
            "wallet_total_collateral": 1890719757.24550000,
            "staking_woo_collateral": 0
        }
    ]
}
```

**Parameters**


| Name      | Type      | Required       | Description                                                                       |
| --------- | --------- | -------------- | --------------------------------------------------------------------------------- |
| withdraw_token   | string | N        | If input this field, the `withdraw_amount` field will be mandatory |
| withdraw_amount  | number | N        | amount you want to withdraw of the `withdraw_token`  |


## Update Account Mode

**Limit: 5 requests per 60 seconds per user**

`
POST /v1/client/account_mode
`

Choose account mode: pure spot or margin or futures

**Parameters**

| Name         | Type   | Required | Description                |
| :----------- | :----- | :------- | :------------------------- |
| account_mode | string | Y        | PURE_SPOT, MARGIN, FUTURES |



> **Response**

```js
{
    "success": true
}
```


## Update Position Mode

**Limit: 2 requests per 1 second per user**

`
POST /v1/client/position_mode
`

Choose position mode: ONE_WAY or HEDGE_MODE

**Parameters**

| Name         | Type   | Required | Description                |
| :----------- | :----- | :------- | :------------------------- |
| position_mode | string | Y        | set ONE_WAY / HEDGE_MODE to position mode|



> **Response**

```js
{
    "success": true
}
```

## Update Leverage Setting

**Limit: 5 requests per 60 seconds per user**

`
POST /v1/client/leverage
`

Choose maximum leverage for margin mode  
**Parameters**

| Name     | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| leverage | int  | Y        | for margin mode:  3, 4, 5，10 ;  |



> **Response**

```js
{
    "success": true
}
```



## Update Futures Leverage Setting

**Limit: 60 requests per 60 seconds per user**

`
POST /v1/client/futures_leverage
`

Choose maximum leverage for futures mode
 

**Parameters**

| Name     | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| symbol | string  | Y        | Perpetual symbol name. |
| margin_mode | string  | Y        | Options are `CROSS`/`ISOLATED` |
| position_side | string  | Y        | Options are `LONG`/`SHORT` in hedge mode; `BOTH` in one way mode. |
| leverage | int  | Y        | Leverage to set |



> **Response**

```js
{
    "success": true
}
```




## GET Futures Leverage Setting

**Limit: 10 requests per 60 seconds per user**

`
GET /v1/client/futures_leverage
`

 

**Parameters**

| Name     | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| symbol | string  | Y        | Perpetual symbol name. |
| margin_mode | string  | Y        | Options are `CROSS`/`ISOLATED` |
| position_mode | string  | Y        | Options are `ONE_WAY`/`HEDGE`, for `HEDGE` mode it will present for both side |
| leverage | int  | N        | Leverage to set |



> **Response**

```js
// cross margin, one way mode
{
    "success": true,
    "data": {
        "symbol": "PERP_BTC_USDT",
        "margin_mode": "CROSS",
        "position_mode": "ONE_WAY",    
        "details": [
            {
                "position_side": "BOTH",
                "leverage": "10"
            }
        ]
    },
    "timestamp": 1696663264324
}

// cross margin, hedge mode
{
    "success": true,
    "data": {
        "symbol": "PERP_BTC_USDT",
        "margin_mode": "CROSS",
        "position_mode": "HEDGE_MODE",    
        "details": [
            {
                "position_side": "LONG",
                "leverage": "10"
            },
            {
                "position_side": "SHORT",
                "leverage": "10"
            },
        ]
    },
    "timestamp": 1696663264324
}

// isolated margin, one way mode
{
    "success": true,
    "data": {
        "symbol": "PERP_BTC_USDT",
        "margin_mode": "ISOLATED",
        "position_mode": "ONE_WAY",    
        "details": [
            {
                "position_side": "BOTH",
                "leverage": "10"
            }
        ]
    },
    "timestamp": 1696663264324
}

// isolated margin, hedge mode
{
    "success": true,
    "data": {
        "symbol": "PERP_BTC_USDT",
        "margin_mode": "ISOLATED",
        "position_mode": "HEDGE_MODE",    
        "details": [
            {
                "position_side": "LONG",
                "leverage": "10"
            },
            {
                "position_side": "SHORT",
                "leverage": "20"
            },
        ]
    },
    "timestamp": 1696663264324
}
```



## Update Isolated Margin Setting

**Limit: 20 requests per 60 seconds per user**

`
POST /v1/client/isolated_margin
`


**Parameters**

| Name     | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| symbol | string  | Y        | Perpetual symbol name. |
| position_side | string  | Y        | Options are LONG/SHORT in hedge mode; BOTH in one way mode. |
| adjust_token | string  | Y        | Only USDT is supported. |
| adjust_amount | Number  | Y        | Token amount to be added or reduced. |
| action | Number  | Y        | `ADD`/`REDUCE` |



> **Response**

```js
{
    "success": true
}
```


## Get Funding Fee History

**Limit: 20 requests per 60 seconds per user**

`
GET /v1/funding_fee/history
`

Get funding fee history

**Parameters**

| Name    | Type      | Required       | Description                                                  |
| :------ | :-------- | :------------- | :----------------------------------------------------------- |
| symbol  | string    | N              | symbol that you wish to query                                    |
| start_t | timestamp | N              | start time range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| end_t   | timestamp | N              | end time range that you wish to query, noted that the time stamp is a 13-digits timestamp. |
| page    | number    | N (default: 1) | the page you wish to query.                                      |
| size   | number | N (default: 10)  | max 5000                               |



> **Response**

```js
{
    "success": true,
    "meta": {
		    "total": 670,
        "records_per_page": 25,
        "current_page": 1
    },
    "rows": [
        {
            "id": 10001,
            "symbol": "PERP_BTC_USDT",
            "funding_rate": 0.00345,
            "mark_price": 100,
            "funding_fee": 0.345,
            "payment_type": "Receive", // Receive and Pay
            "status": "COMPLETED",
            "created_time": "1575014255.089", // Unix epoch time in seconds
            "updated_time": "1575014255.910", // Unix epoch time in seconds
            "funding_rate_interval_hours": 1
        },
        // ....skip (total 25 items in one page)

}
```



## Get All Position info

**Limit: 30 requests per 10 seconds per user**

`
GET /v1/positions
`

<font color=#0000FF>** Note: This API will be deprecated at the end of 2023 Q1, please find the replacement API in </font> [Get Positions - New](#get-positions-new)

**Parameters**

> **Response**

```js
{
    "total_account_value": 1924712.88293063,
    "current_margin_ratio": 7719.4699,
    "success": true,
    "total_collateral": 1146084.70891586,
    "total_vault_value": 0.0,
    "total_staking_value": 0.0,
    "positions": [
        {
            "symbol": "PERP_WOO_USDT",
            "holding": 8.0,
            "pending_long_qty": 0.0,
            "pending_short_qty": 0.0,
            "settle_price": 0.31197093,
            "average_open_price": 0.43228,
            "timestamp": "1714247701.266",
            "opening_time": "1712542194.878",
            "mark_price": 0.31851,
            "est_liq_price": 0.0,
            "position_side": "LONG",
            "pnl_24_h": 0.0,
            "fee_24_h": 0.0,
            "margin_mode": "ISOLATED", 
            "leverage": 10, 
            "isolated_margin_token": "USDT",
            "isolated_margin_amount": 99.1,
            "isolated_frozen_long": 81.2,
            "isolated_frozen_short": 88.2
        },
        {
            "symbol": "PERP_WOO_USDT",
            "holding": 8.0,
            "pending_long_qty": 0.0,
            "pending_short_qty": 0.0,
            "settle_price": 0.31197093,
            "average_open_price": 0.43228,
            "timestamp": "1714247701.266",
            "opening_time": "1712542194.878",
            "mark_price": 0.31851,
            "est_liq_price": 0.0,
            "position_side": "LONG",
            "pnl_24_h": 0.0,
            "fee_24_h": 0.0,
            "margin_mode": "CROSS", 
            "leverage": 10, 
            "isolated_margin_token": "",
            "isolated_margin_amount": 0,
            "isolated_frozen_long": 0,
            "isolated_frozen_short": 0
        }
    ],
    "initial_margin_ratio": 1.0006,
    "free_collateral": 1145936.1530736,
    "maintenance_margin_ratio": 0.0126
}
```

## Get All Position info - New

**Limit: 30 requests per 10 seconds per user**

`
GET /v3/positions
`

<!-- <font color=#0000FF>** Note: This API will be released with WOO X New Margin Ratio Program in Jan 2023, currently on available in staging environment </font> -->
The API is design to replace the legacy API [Get Positions](#get-positions)

**Parameters**

> **Response**

```js
{
  "success": true,
  "data": {
    "positions": [
      {
        "symbol": "PERP_JTO_USDT",
        "holding": 20.0,
        "pendingLongQty": 0.0,
        "pendingShortQty": 0.0,
        "settlePrice": 2.0771,
        "averageOpenPrice": 2.0771,
        "pnl24H": 0.0,
        "fee24H": 0.0186939,
        "markPrice": 2.07460399,
        "estLiqPrice": 1.92748111,
        "timestamp": 1725916355.494,
        "adlQuantile": 1,
        "positionSide": "BOTH",
        "marginMode": "ISOLATED",
        "isolatedMarginToken": "USDT",
        "isolatedMarginAmount": 4.1604313,
        "isolatedFrozenLong": 0.0,
        "isolatedFrozenShort": 0.0,
        "leverage": 10
      },
      {
        "symbol": "PERP_W_USDT",
        "holding": -50.0,
        "pendingLongQty": 50.0,
        "pendingShortQty": 0.0,
        "settlePrice": 0.1906,
        "averageOpenPrice": 0.1906,
        "pnl24H": 0.0,
        "fee24H": 0.0,
        "markPrice": 0.2103828568089886,
        "estLiqPrice": 4.542491646808989,
        "timestamp": 1725681481.767,
        "adlQuantile": 1,
        "positionSide": "BOTH",
        "marginMode": "CROSS",
        "isolatedMarginToken": "",
        "isolatedMarginAmount": 0.0,
        "isolatedFrozenLong": 0.0,
        "isolatedFrozenShort": 0.0,
        "leverage": 20
      }
    ]
  },
  "timestamp": 1725916369913
}

```

## Get One Position info

**Limit: 30 requests per 10 seconds per user**

<font color=#0000FF>（Note that get-one-position-info will only support to response the CROSS mode position of the selected symbol.）</font>

`
GET /v1/position/:symbol
`

**Parameters**

> **Response**

```js
{
    "success": true,
    "symbol": "PERP_BTC_USDT",
    "holding": 1.23,
    "pending_long_qty": 0.5,
    "pending_short_qty": 0.23,
    "settle_price": 50000,
    "average_open_price": 49000,
    "pnl_24_h": 20,
    "fee_24_h": 0.2,
    "mark_price": 49550,
    "est_liq_price": 40000,
    "timestamp": "1575014255.089"
}
```
## GET InsuranceFund

**Limit: token filtered to USDT only**

`
GET /v3/public/insuranceFund
`

**Parameters**

| Name | Type   | Required | Description                                 |
| ---- | ------ | -------- | ------------------------------------------- |
| symbol  | string | Y        |   |

> **Response**

```js
{
   "success": true,
    "data": {
      "rows": [
        {
          "balance": 1000,
          "token": "USDT",
        }
      ]
    },
    "timestamp": 1673323685109 
}
```



