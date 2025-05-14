# 🇮🇩 Reverse Geocode Indonesia

**Currently supports only Indonesia**

Reverse Geocode Indonesia is an API that takes latitude and longitude as input and returns the corresponding address in Indonesia (Kecamatan/District, Kabupaten/Regency, Provinsi/Province, and Country).
We built this because sometimes you need to geocode `at high speed (> 1 req/second)` for Indonesian locations.
This API is not perfect, but it's fast and works well for most use cases! 🚀

---

## 🛠️ Installation (Local Development)

```bash
make up
```
Then, open your browser and visit [http://localhost:8080/](http://localhost:8080/) to explore the API documentation (Swagger UI).

---

## 🎬 Demo

![Demo](./assets/demo.gif)

The demo shows how to use the API to reverse geocode a location in Indonesia with static authentication.

---

## 🗺️ Database Source

The administrative boundaries are sourced from shapefiles and imported into a SQL/PostGIS database.
To convert the shapefile to SQL, check out [`docs/database/convert.py`](docs/database/convert.py) for a step-by-step script.
![Database](./assets/database.png)

---

## To Do

- [x] Add caching
- [ ] Add CI/CD
- [ ] Add more tests
- [ ] Add more documentation
