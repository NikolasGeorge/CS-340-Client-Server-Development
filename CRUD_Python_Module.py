"""CRUD operations for the Austin Animal Center collection in MongoDB.

This module provides create, read, update, and delete access to the animals
collection in the aac database. It is written so that other Python scripts
can import it and reuse the same database access code rather than repeating
connection and query logic.
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter(object):
    """CRUD operations for the animals collection in the aac database."""

    def __init__(self, username, password,
                 host='localhost', port=27017,
                 db='aac', collection='animals', auth_source='admin'):
        """Connect to MongoDB and hold a handle to the target collection.

        The username and password are supplied by the calling script rather
        than hard coded here, so that credentials are not stored in the module.
        auth_source is the database the user account was created in, which is
        admin, even though the account's role applies to aac.
        """
        try:
            self.client = MongoClient(
                'mongodb://%s:%s@%s:%d/?authSource=%s'
                % (username, password, host, port, auth_source))
            self.database = self.client[db]
            self.collection = self.database[collection]

            # Force an immediate round trip so that bad credentials or an
            # unreachable server fail here rather than on the first query.
            self.client.admin.command('ping')
        except PyMongoError as error:
            raise Exception('Failed to connect to MongoDB: %s' % error)

    def create(self, data):
        """Insert a single document into the collection.

        Args:
            data: a dictionary of key/value pairs to insert.

        Returns:
            True if the insert succeeded, otherwise False.
        """
        # Reject anything that is not a populated dictionary before touching
        # the database, since insert_one would raise on None.
        if not isinstance(data, dict) or not data:
            print('create: data must be a non-empty dictionary')
            return False

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except PyMongoError as error:
            print('create: insert failed: %s' % error)
            return False

    def read(self, query):
        """Query the collection and return every matching document.

        Args:
            query: a dictionary of key/value pairs used as the find filter.
                An empty dictionary returns all documents.

        Returns:
            A list of matching documents, or an empty list if the query
            failed or matched nothing.
        """
        if not isinstance(query, dict):
            print('read: query must be a dictionary')
            return []

        try:
            # find() returns a cursor rather than the documents themselves,
            # so it is converted to a list before being returned.
            cursor = self.collection.find(query)
            return list(cursor)
        except PyMongoError as error:
            print('read: query failed: %s' % error)
            return []

    def update(self, query, new_values):
        """Change every document that matches the query.

        Args:
            query: a dictionary of key/value pairs used as the filter.
            new_values: the changes to apply, in the form update_many
                accepts, such as {"$set": {"name": "Max"}}. A plain
                dictionary with no update operators is treated as a $set.

        Returns:
            The number of documents modified, or 0 if nothing matched or
            the update failed.
        """
        if not isinstance(query, dict) or not query:
            # An empty filter matches every document in the collection, so
            # it is refused rather than allowed to rewrite the whole data set.
            print('update: query must be a non-empty dictionary')
            return 0
        if not isinstance(new_values, dict) or not new_values:
            print('update: new_values must be a non-empty dictionary')
            return 0

        # update_many requires update operators such as $set. If the caller
        # passed bare field values, wrap them in $set so they are applied as
        # field changes instead of being rejected by the driver.
        if not any(key.startswith('$') for key in new_values):
            new_values = {'$set': new_values}

        try:
            result = self.collection.update_many(query, new_values)
            return result.modified_count
        except PyMongoError as error:
            print('update: update failed: %s' % error)
            return 0

    def delete(self, query):
        """Remove every document that matches the query.

        Args:
            query: a dictionary of key/value pairs used as the filter.

        Returns:
            The number of documents removed, or 0 if nothing matched or the
            delete failed.
        """
        if not isinstance(query, dict) or not query:
            # As with update, an empty filter would remove every document,
            # so it is refused.
            print('delete: query must be a non-empty dictionary')
            return 0

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as error:
            print('delete: delete failed: %s' % error)
            return 0
