"""
 ElasticSearch.py
 Python module for asynchronous data import/export to a distributed, free and open search and analytics engine
 for all types of data (Elasticsearch).

 https://www.elastic.co/what-is/elasticsearch
 Class constructor expects to get `url`, `name`, and `secret` as input data. These parameters are mandatory!

 Supported parameters:
     url            : An endpoint address for Elasticsearch cluster
     user           : Name of the user for HTTP plain authentication
     secret:        : The user's secret (password)

 Example:
    from ElasticSearch import ElasticSearch
    es = ElasticSearch(url='https://my.es.cluster:9200', user='admin', secret='password')
    es.query(index='data', query={ "match": { "id": { "query": 1000 } } })

 Changelog:
    v0.0.1 - 2022-05-13: Initial version

 TODO:
    * Update class documentation
    * Cover-up the code with unit-tests

 Dmitrii Ageev <dmitrii@opsworks.ru>
 https://www.opsworks.ru/
"""

import ssl
import pytz
import logging
from datetime import datetime
from elasticsearch import Elasticsearch


# Constants definition
#  Note: ideally you have to add the certificate to /etc/ssl/certs/ca-certificates.crt and
#        specify ca_path='/etc/ssl/certs'
ROOT_CA = '/etc/ssl/certs'
#ROOT_CA = '/home/user/.elasticsearch/root.crt'


def to_es_timestamp(datetime_obj):
    return int(datetime_obj.timestamp() * 1000)


def from_es_timestamp(timestamp, tz=pytz.utc):
    return datetime.fromtimestamp(timestamp / 1000, tz)


class ElasticSearch:
    """ElasticSearch class handles all interaction with Elasticsearch service"""

    # >>> Private class variables:
    #   Declare a logger class variable
    __logger = logging.getLogger(__name__)

    #   Declare an Elasticsearch class object/client handler
    __es: Elasticsearch

    def __init__(self, url: str, user: str, secret: str):
        """Class constructor.
            url: Elasticsearch cluster URL;
            user: Elasticsearch user's name;
            secret:  Elasticsearch user's secret (password);
        """

        # Prepare SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(ROOT_CA)
        context.verify_mode = ssl.CERT_REQUIRED

        # Check cluster connectivity and version
        try:
            self.__es = Elasticsearch(hosts=[url],
                                      http_auth=(user, secret),
                                      ssl_context=context)
            # Here we poll the Info API call, just to ensure the connection was properly set
            info = self.__es.info()
            self.log().info(
                f"Successfully connected to Elasticsearch. Server version: {info['version']['number']}")
            # Make sure the 'data' index is on the place
            self.setup()
        except Exception as ex:
            self.log().exception(
                f"Got an exception while connecting to Elasticsearch by URL {url}: {ex}")

    def __del__(self):
        """Class destructor."""
        if self.ping():
            self.client().close()
        del self.__es
        del self.__logger

    def log(self):
        """Returns logging client handler."""
        return self.__logger

    def client(self):
        """Returns Elasticsearch client handler."""
        return self.__es

    def indices(self):
        """Returns Elasticsearch indices handler."""
        return self.client().indices

    def ping(self):
        """Polls the Elasticsearch connection."""
        return bool(self.client().ping())

    def check_index(self, name: str):
        """Returns True if an Elasticsearch index exists; False otherwise."""
        return bool(self.indices().exists(index=name))

    def create_index(self, name: str, settings: dict, mappings: dict):
        """Creates an Elasticsearch index"""
        if self.check_index(name):
            return False
        try:
            self.indices().create(index=name, settings=settings, mappings=mappings)
            return True
        except Exception as ex:
            self.log().exception(
                f"Got an error while creating the '{name}' Elasticsearch index.")
            self.log().exception(f"  Message: {ex}")
        return False

    def empty_index(self, name: str):
        """Empties Elasticsearch index."""

        match_all_query = {
            "match_all": {}
        }
        # Check cluster connectivity and version
        try:
            self.client().delete_by_query(index=name, query=match_all_query)
            self.log().info(
                f"Successfully emptied the '{name}' Elasticsearch index.")
        except Exception as ex:
            self.log().exception(
                f"Got an exception while emptying '{name}' Elasticsearch index: {ex}")
            return False
        return True

    def delete_index(self, name: str):
        """Deletes Elasticsearch index."""

        # First, verify that index actually exists
        if not self.indices().exists(index=name):
            return False

        try:
            # Delete an index, or at least give it a try
            response = self.indices().delete(index=name)
            if response["acknowledged"]:
                self.log().info(
                    f"The '{name}' Elasticsearch index was successfully deleted.")
            else:
                self.log().error(
                    f"Got an error while deleting the '{name}' Elasticsearch index!")
                return False
        except Exception as ex:
            self.log().exception(
                f"Got an exception while trying to delete '{name}' Elasticsearch index: {ex}")
            return False
        return True

    def query(self, index: str, query: dict, raw=False, size=10000):
        """Runs a search by the index."""
        try:
            body = {'query': query}
            if raw:
                return self.client().search(index=index, body=body, size=size)
            else:
                return self.client().search(index=index, body=body, size=size)["hits"]["hits"]
        except Exception as ex:
            self.log().exception(
                f"Got an exception while trying to search '{index}' Elasticsearch index: {ex}")
        return None

    def store(self, index: str, body: dict):
        """Saves data in index"""
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html
        try:
            self.client().index(index=index, body=body)
        except Exception as ex:
            self.log().exception(
                f"Got an exception while trying to store data in '{index}' Elasticsearch index: {ex}")
            return False
        return True

    def setup(self):
        """This routine does a basic setup."""
        if not self.check_index(name='data'):
            settings = {
                'number_of_shards': 2,
                'number_of_replicas': 2
            }
            mappings = {
                'properties': {
                    'id': {'type': 'long'},
                    'timestamp': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
                    }
                }
            }
            return self.create_index(name='data', settings=settings, mappings=mappings)
        return True

    def get(self, query=None):
        """Retrieves all data from the index."""
        if query is None:
            query = {}
        return self.query(index='data', query=query)

    def put(self, body: dict):
        """Puts data to the index."""
        body['timestamp'] = to_es_timestamp(datetime.now())
        return self.store(index='data', body=body)


if __name__ == '__main__':
    print("ERROR: You shouldn't try to run this module as a standalone executable!")
    exit(255)
