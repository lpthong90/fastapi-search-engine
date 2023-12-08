# Search Engine - FastAPI
The project is a simple microservice which populates the employee search directory for a HR company.

![Web UI](https://github.com/lpthong90/fastapi-search-engine/blob/91bfd9c7a76425e177136a7df3dfc68c05b2bb92/images/ui.png)

The following is filter options for the Search API:
![Filter Options](...)

**Source Code**: <a  href="https://github.com/lpthong90/fastapi-search-engine"  target="_blank">https://github.com/lpthong90/fastapi-search-engine</a>

## Features:

Following are all functional and non-functional requirements which are allowed in this project.

**Functional requirements:**

-  [x] Only implement the search api.
-  [x] The service is containerized .
-  [x] The API information is sharable in an **OPEN API** format
-  [x] The API is unit tested
-  [x] No external library is used for rate-limiting .
-  [x] Authentication is included to make sure data not be leaked in the API.
-  [x] The project is implemented with Python/FastAPI.

**Non-functional requirements**

- [x] You may not use any external dependencies or libraries (only standard library is allowed)
- [x] You may use external testing libraries if you choose to write tests
- [x] The application should execute correctly in a Linux (or UNIX-like) environment

## Assumption

We have a list of assumptions:
- User is from an Organization.
- User has an Access-Token to authenticate when request to private api endpoints.
- Organization want to customize a list of columns to display.
- User from an organization can not search any employee of another organization.

As initialized configuration, we have 3 users as following:

|           |Username|Organization|Access-Token|Display Columns |
|-----------|--------|------------|------------|------------|
|User A     |`user_a`|`org-a`     |`token_a`   |`contact_info` `department` `location` `position`
|User B     |`user_b`|`org-b`     |`token_b`   |`department` `location` `position`
|User C     |`user_c`|`org-c`     |`token_c`   |`position`


## Requirements

docker 24.0.6+

docker-compose 3.7+

## Test

> $ docker build -t  test-search-engine -f Dockerfile.test .
>
> $ docker run --rm test-search-engine

## Installation

### Run it

> $ docker-compose up --build -d

### Initialize data

Run migration:
> $ docker exec app_1 /bin/sh -c ./migrate.sh

Generate data:
> $ export DB_URL=postgresql://username:password@app_db/dev_db
> 
> $ docker exec -i app_db_1 psql -d DB_URL < generate_data.sql

### Check it

Open your browser at  [http://127.0.0.1:8000](http://127.0.0.1:8000).

You will see the JSON response as:
```
{"Hello":"World"}
```

On the other hand, you can test search employee feature as following:
```
curl -X 'GET' \
  'http://localhost:8000/search?status=active&status=terminated&limit=10&page=1' \
  -H 'accept: application/json' \
  -H 'Access-Token: token_a'
``` 
You will see the JSON response as:
```
{
  "limit": 10,
  "has_next_page": true,
  "has_previous_page": false,
  "employees": [
    {
      "id": 5,
      "first_name": "first_name-45c48",
      "last_name": "last_name-cfcd2",
      "contact_info": "contact_info-c9f0f",
      "organization": "org-a",
      "department": "department-6",
      "position": "position-71",
      "location": "location-09",
      "status": "active"
    }
    ...
  ]
}
```

You can check with 3 access-tokens which are belong to 3 users respectively: `token_a`, `token_b`, `token_c`


### Interactive API docs

Now go to  [](http://127.0.0.1:8000/docs)[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see the automatic interactive API documentation:

![Api Docs](https://github.com/lpthong90/fastapi-search-engine/blob/main/images/docs.png)

### Sharable OpenAPI JSON file

Open your browser at  [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

You will see OpenAPI json format file:

![OpenAPI Json File](https://github.com/lpthong90/fastapi-search-engine/blob/eea59139290fee1971526354c94b7cff0d839374/images/openapi.png)
