python-elasticsearch
====================

Python module for simplified interaction with Elasticsearch service.

**Supported parameters:**
* url            : An endpoint address for Elasticsearch cluster
* user           : Name of the user for HTTP plain authentication
* secret:        : The user's secret (password)


**Class methods:**
- log(self): - _Returns logging client handler._
- client(self): - _Returns Elasticsearch client handler._
- indices(self): - _Returns Elasticsearch indices handler._
- ping(self): - _Polls the Elasticsearch connection._
- check_index(self, name: str): - _Returns True if an Elasticsearch index exists; False otherwise._
- create_index(self, name: str, settings: dict, mappings: dict): - _Creates an Elasticsearch index._
- empty_index(self, name: str): - _Empties Elasticsearch index._
- delete_index(self, name: str): - _Deletes Elasticsearch index._
- query(self, index: str, query: dict, raw=False, size=10000): - _Runs a search by the index._
- store(self, index: str, body: dict): - _Saves data in index._
- setup(self): - _This routine does a basic setup._
- get(self, query=None): - _Retrieves data from the index._
- put(self, body: dict): - _Puts data to the index._

## Examples

```
from ElasticSearch import ElasticSearch
es = ElasticSearch(url='https://my.es.cluster:9200', user='admin', secret='password')
es.query(index='data', query={ "match": { "id": { "query": 1000 } } })
```


## Author
Dmitrii Ageev <dmitrii@opsworks.ru>
