# El Froggo — Offering Requirement Schemas

## trading_signals ($0.50)

```json
{
  "type": "object",
  "properties": {
    "chain": {"type": "string", "default": "base"},
    "max_results": {"type": "number", "default": 5},
    "risk_filter": {"enum": ["all","low","medium","high"], "default": "all"},
    "min_liquidity": {"type": "number", "default": 10000},
    "min_volume_24h": {"type": "number", "default": 5000}
  }
}
```

## risk_scanner ($0.30)

```json
{
  "type": "object",
  "required": ["token_address"],
  "properties": {
    "token_address": {"type": "string", "description": "0x... on Base"},
    "depth": {"enum": ["quick","full"], "default": "full"}
  }
}
```

## market_intelligence ($0.20)

```json
{
  "type": "object",
  "properties": {
    "chain": {"type": "string", "default": "base"},
    "category": {"enum": ["trending","new_pairs","volume_leaders","all"], "default": "all"},
    "max_results": {"type": "number", "default": 10}
  }
}
```

## token_comparison ($0.40)

```json
{
  "type": "object",
  "required": ["token_addresses"],
  "properties": {
    "token_addresses": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 2,
      "maxItems": 5
    }
  }
}
```
