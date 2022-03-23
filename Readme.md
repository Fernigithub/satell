

# Run

```properties
$ docker-compose up --build
```

# Try me

SAVE 

```properties
curl --location --request POST 'http://localhost:8008/save' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name":"satellocccgic_5",
    "date":"2020-01-03",
    "area":"POLYGON((1 1,3 1,3 3,1 3,1 1))",
    "properties":{"name":"satellogic2"}
}'
```
DELETE

```properties
curl --location --request DELETE 'http://localhost:8008/delete/satellogic_1'
```
RETRIEVE BY NAME
```properties
curl --location --request GET 'http://localhost:8008/retrieve/name/satellogic_1'
```
RETTRIEVE BY INTERSECTED AREA
```properties
curl --location --request GET 'http://localhost:8008/retrieve/area/POLYGON((2 2,3 2,3 3,2 3,2 2))'
```
RETRIEVE INTERSECTION
```properties
curl --location --request GET 'http://localhost:8008/retrieve/inter/POLYGON((0 0,1 0,1 1,0 1,0 0))'
```

RETRIEVE BY PROPERTIES
```properties
curl --location -g --request GET 'http://localhost:8008/retrieve/prop/{"name": "satellogic2","crop":"wheat"}'
```

# Utils


<code> <i>DataBase</i> </code>

```properties
$ docker-compose exec db psql --username=fastapi_satellogic --dbname=fastapi_satellogic
\l
```

<code> <i>Kill Port</i> </code>

```properties
$ sudo lsof -t -i tcp:8000 | xargs kill -9
```