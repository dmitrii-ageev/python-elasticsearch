python-elasticsearch
====================

Python module for simplified interaction with Elasticsearch service.

**Supported parameters:**
* url            : An endpoint address for Elasticsearch cluster
* user           : Name of the user for HTTP plain authentication
* secret:        : The user's secret (password)


**Class methods:**
- log(): - _Returns logging client handler._
- client(): - _Returns Elasticsearch client handler._
- indices(): - _Returns Elasticsearch indices handler._
- ping(): - _Polls the Elasticsearch connection._
- check_index(name: str): - _Returns True if an Elasticsearch index exists; False otherwise._
- create_index(name: str, settings: dict, mappings: dict): - _Creates an Elasticsearch index._
- empty_index(name: str): - _Empties Elasticsearch index._
- delete_index(name: str): - _Deletes Elasticsearch index._
- query(index: str, query: dict, raw=False, size=10000): - _Runs a search by the index._
- store(index: str, body: dict): - _Saves data in index._
- setup(): - _This routine does a basic setup._
- get(query: dict): - _Retrieves data from the index._
- put(body: dict): - _Puts data to the index._

## Examples

```
from ElasticSearch import ElasticSearch
es = ElasticSearch(url='https://my.es.cluster:9200', user='admin', secret='password')
es.query(index='data', query={ "match": { "id": { "query": 1000 } } })
```


## Author
Dmitrii Ageev <dmitrii@opsworks.ru>
