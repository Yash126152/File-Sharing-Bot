import pymongo

# Define the MongoDB URI and database name
DB_URI = "mongodb+srv://yash13:Yash24@cluster0.bafbji3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Airdrop_db"

# Print DB_URI to verify its content
print(f"DB_URI: {DB_URI}")

try:
    # Initialize MongoDB client
    dbclient = pymongo.MongoClient(DB_URI)
    database_secondary = dbclient[DB_NAME]
    user_data_secondary = database_secondary['users']
except pymongo.errors.ConfigurationError as e:
    print(f"Error initializing MongoClient: {e}")
    # Handle the error gracefully, such as logging and terminating the application or retrying the connection

async def secondary_present_user(user_id: int):
    found = user_data_secondary.find_one({'_id': user_id})
    return bool(found)

async def secondary_add_user(user_id: int):
    user_data_secondary.insert_one({'_id': user_id})
    return

async def secondary_full_userbase():
    user_docs = user_data_secondary.find()
    user_ids = [doc['_id'] for doc in user_docs]
    return user_ids

async def secondary_del_user(user_id: int):
    user_data_secondary.delete_one({'_id': user_id})
    return