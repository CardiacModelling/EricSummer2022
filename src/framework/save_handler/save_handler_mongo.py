from ..result import Result
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from ..config import MONGODB_URI, logger
from .save_handler import SaveHandler


class SaveHandlerMongo(SaveHandler):
    def __init__(self, database='test'):
        # Create a new client and connect to the server
        self.client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            logger.info(
                f"Pinged your deployment at {MONGODB_URI}.\nYou successfully connected to MongoDB!")
        except Exception as e:
            logger.debug(MONGODB_URI)
            logger.exception(e)
        self.db = self.client[database]
        self.res_collection = self.db['results']
        self.database = database

    def drop_database(self):
        # self.client.drop_database(self.database)
        self.res_collection.drop()

    def save_result(self, result, partial=True):
        if None in list(result.info.values()):
            logger.warning('Saving a result with incomplete info!')
        result_dict = result.to_dict(partial=partial)
        self.res_collection.update_one(
            result.info, {"$set": result_dict}, upsert=True)

    def find_results(self, query, partial=True):
        projection = {"_id": 0}
        if partial:
            projection['points'] = 0
            projection['end_of_iterations'] = 0
        docs = self.res_collection.find(query, projection)
        return [Result(**doc) for doc in docs]

    def find_instances(self, query):
        pipeline = [
            {
                "$match": query
            },
            {
                "$group": {
                    "_id": {
                        "algorithm_name": "$algorithm_name",
                        "algorithm_version": "$algorithm_version",
                        "instance_index": "$instance_index"
                    },
                    "count": {"$sum": 1},
                }
            },
            {
                "$replaceRoot": {
                    "newRoot": {
                        "algorithm_name": "$_id.algorithm_name",
                        "algorithm_version": "$_id.algorithm_version",
                        "instance_index": "$_id.instance_index",
                        "results_count": "$count",
                    }
                }
            }
        ]

        return list(self.res_collection.aggregate(pipeline))
