import pymongo
from pymongo.errors import ConnectionFailure, PyMongoError
from flask import redirect, url_for, session
import datetime
from dotenv import load_dotenv
import os

# Database class to handle DB connection and errors

class Database:
    def __init__(self, uri=None, database_name="your_db_name"):

        # Define the collections in the database
        self.PROJECTS_COLLECTION = "projects"
        self.USERS_COLLECTION = "users"

        # Load the environment variables from the .env file
        load_dotenv()

        # Load the environment variables
        if uri is None:
            uri = os.getenv("MONGO_URI")

        # Set connections 2 none to set up DB connection check
        self.client = None
        self.db = None

        # Timeout variable to control how long DB attempts to connect
        timeout = 10

        # Retry connection 3 times. This will help to handle any connection errors and break out of loop upon
        # successful connection.
        for attempt in range(3):
            try:
                self.client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=timeout * 1000)

                # The ismaster is used to check if DB connection was successful
                self.client.admin.command('ismaster')

                # If connection is successful, assign the database to the db variable
                self.db = self.client[database_name]

                # If connection is successful, break out of the loop
                break

            except ConnectionFailure:
                # If connection fails, continue to the next iteration of the loop
                continue

            except RuntimeError:
                # Redirect to error page
                error_message = "Could not connect to the database. Please try again later."
                raise Exception(f"Database error: {str(error_message)}")

            except Exception as e:
                # Redirect to error page
                error_message = "An error occurred while connecting to the database. Please try again later."
                raise Exception(f"Database error: {str(error_message)}")

        # If connection still fails after 3 attempts
        if self.client is None or self.db is None:
            # Clear the session and redirect to the error page
            session.clear()
            error_message = "Could not connect to the database. Please try again later."
            raise Exception(f"Database error: {str(error_message)}")


    def get_collection(self, collection_name):
        try:
            # Return the collection from the database
            return self.db[collection_name]

        except PyMongoError as exception:
            # Redirect to the error page if an error occurs
            raise Exception(f"Database error: {str(exception)}")

    def find_one(self, collection_name, query):
        collection = self.get_collection(collection_name)

        # Try to find one document in the collection
        # If an error occurs, redirect to the error page
        try:
            return collection.find_one(query)
        except PyMongoError as exception:
            raise Exception(f"Database error: {str(exception)}")

    # I use *args and **kwargs to pass any number of arguments to the find method, similar to how it works
    # in the PyMongo library
    def find(self, collection_name, *args, **kwargs):
        collection = self.get_collection(collection_name)

        # Try to find all documents in the collection according to specific criteria
        # If an error occurs, redirect to the error page
        try:
            return collection.find(*args, **kwargs)
        except PyMongoError as exception:
            raise Exception(f"Database error: {str(exception)}")

    def insert_one(self, collection_name, document):
        collection = self.get_collection(collection_name)

        # Try to insert one document in the collection
        # If an error occurs, redirect to the error page
        try:
            return collection.insert_one(document)
        except PyMongoError as exception:
            raise Exception(f"Database error: {str(exception)}")

    def update_one(self, collection_name, query, new_values):
        collection = self.get_collection(collection_name)

        # Try to update one document in the collection
        # If an error occurs, redirect to the error page
        try:
            return collection.update_one(query, new_values)
        except PyMongoError as exception:
            raise Exception(f"Database error: {str(exception)}")


    def delete_one(self, collection_name, query):
        collection = self.get_collection(collection_name)

        # Try to delete one document in the collection
        # If an error occurs, redirect to the error page
        try:
            return collection.delete_one(query)
        except PyMongoError as exception:
            raise Exception(f"Database error: {str(exception)}")

    def get_projects(self, username):
        try:
            # Retrieve the user by username
            users_collection = self.get_collection(self.USERS_COLLECTION)
            user = users_collection.find_one({"username": username})

            if not user:
                raise Exception("User not found")

            # Extract project IDs from the user document
            project_ids = user.get("projects", [])

            # Query the projects collection using the project IDs
            projects_collection = self.get_collection(self.PROJECTS_COLLECTION)
            projects = list(projects_collection.find({"_id": {"$in": project_ids}}))

            # Convert ObjectId to string for JSON serialization
            for project in projects:
                project["_id"] = str(project["_id"])

            return projects

        except PyMongoError as exception:
            raise Exception(f"Database error: {str(exception)}")


    # Custom methods for the project tracking application
    def create_project(self, project_id, project_name, username, description=None):
        collection = self.get_collection("projects")
        document = {
            "_id": project_id,
            "name": project_name,
            "username": username,
            "description": description,
            "created_at": datetime.utcnow(),
            "metrics": []
        }
        try:
            return collection.insert_one(document)
        except PyMongoError as exception:
            raise Exception(f"Database error: {str(exception)}")

    def get_project_metrics(self, project_id):
        collection = self.get_collection("projects")
        try:
            project = collection.find_one({"_id": project_id}, {"metrics": 1, "_id": 0})
            if not project:
                raise Exception("Project not found")
            return project.get("metrics", [])
        except PyMongoError as exception:
            raise Exception(f"Database error: {str(exception)}")