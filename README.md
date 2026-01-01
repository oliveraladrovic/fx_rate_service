# FX Rate Service

Asynchronous FastAPI service for fetching, storing, and serving foreign exchange rates.

The service integrates with an external FX API (Frankfurter), stores exchange rates in an SQLite database using async SQLAlchemy, and exposes REST endpoints for querying the data.

---

## Features

- Fetches FX rates from a public external API
- Parallel async data collection using `asyncio.gather`
- Stores rates in SQLite via async SQLAlchemy
- Composite primary key (`base_currency`, `quote_currency`)
- REST API for querying exchange rates
- Fully asynchronous (FastAPI + httpx + aiosqlite)

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy (async)
- SQLite
- httpx
- asyncio

---

## API Endpoints

### Update FX rates
Fetches latest rates from the external API and inserts or updates them in the database.
```
POST /rates
```

Response example:
```
{
  "inserted": 120,
  "updated": 0,
  "total": 120
}
```
### Get all rates for base currency
```
GET /rates/{base_currency}
```
Example:
```
GET /rates/EUR
```
### Get specific currency pair
```
GET /rates/{base_currency}/{quote_currency}
```
Example:
```
GET /rates/EUR/USD
```
## Database Design
The `fx_rates` table uses a composite primary key:

- base_currency
- quote_currency

This guarantees uniqueness per currency pair and allows efficient updates instead of duplicating rows.

## Running the Project
```
uvicorn app:app --reload
```
The SQLite database file will be created automatically if it does not exist.

## Notes
- This project demonstrates real-world async backend patterns.
- Parallel API fetching significantly improves performance compared to sequential calls.
- Designed as a portfolio-ready backend service.