import os
from qdrant_client import QdrantClient
from qdrant_client.http import models

# from dotenv import load_dotenv
from uuid import uuid4


# load_dotenv()

COLLECTION_NAME = os.getenv("COLLECTION_NAME")
COLLECTION_SIZE = os.getenv("COLLECTION_SIZE")
QDRANT_PORT = os.getenv("QDRANT_PORT")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


class QdrantManager:
    """
    A class for managing collectionsget_collection_info in the Qdrant database.

    Args:
        collection_name (str): The name of the collection to manage.
        collection_size (int): The maximum number of documents in the collection.
        port (int): The port number for the Qdrant API.
        host (str): The hostname or IP address for the Qdrant server.
        api_key (str): The API key for authenticating with the Qdrant server.
        recreate_collection (bool): Whether to recreate the collection if it already exists.

    Attributes:
        client (qdrant_client.QdrantClient): The Qdrant client object for interacting with the API.
    """

    def __init__(
        self,
        collection_name=COLLECTION_NAME,
        collection_size: int = COLLECTION_SIZE,
        port: int = QDRANT_PORT,
        host=QDRANT_HOST,
        api_key=QDRANT_API_KEY,
        recreate_collection: bool = False,
    ):
        self.collection_name = collection_name
        self.collection_size = collection_size
        self.host = host
        self.port = port
        self.api_key = api_key

        self.client = QdrantClient(host=host, port=port, api_key=api_key)
        self.setup_collection(collection_size, recreate_collection)

    def setup_collection(self, collection_size: int, recreate_collection: bool):
        if recreate_collection:
            self.recreate_collection()

        try:
            collection_info = self.get_collection_info()
            current_collection_size = collection_info["vector_size"]

            if current_collection_size != int(collection_size):
                raise ValueError(
                    f"""
                    Existing collection {self.collection_name} has different collection size
                    To use the new collection configuration, you need to recreate the collection as it already exists with a different configuration.
                    use recreate_collection = True.
                    """
                )

        except Exception as e:
            self.recreate_collection()
            print(e)

    def recreate_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.collection_size, distance=models.Distance.COSINE
            ),
        )

    def get_collection_info(self):
        collection_info = self.client.get_collection(
            collection_name=self.collection_name
        )

        return {
            "points_count": int(collection_info.points_count),
            "vectors_count": int(collection_info.vectors_count),
            "indexed_vectors_count": int(collection_info.indexed_vectors_count),
            "vector_size": int(collection_info.config.params.vectors.size),
        }

    def upsert_point(self, id, payload, embedding):
        response = self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=id,
                    payload=payload,
                    vector=embedding,
                ),
            ],
        )

        return response

    def upsert_points(self, ids, payloads, embeddings):
        response = self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(
                ids=ids,
                payloads=payloads,
                vectors=embeddings,
            ),
        )

        return response

    def search_point(self, query_vector, user_id, document_id, limit):
        response = self.client.search(
            collection_name=self.collection_name,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="user_id",
                        match=models.MatchValue(
                            value=user_id,
                        ),
                    ),
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id),
                    ),
                ]
            ),
            query_vector=query_vector,
            limit=limit,
        )

        return response

    def delete_collection(self):
        response = self.client.delete_collection(collection_name=self.collection_name)

        return response


qdrant_manager = QdrantManager()
