MongoDB To SQL Converter

A Python-based ETL (Extract, Transform, Load) tool that converts MongoDB collections into SQL tables with automatically inferred schemas and generated INSERT statements. Designed to help migrate unstructured MongoDB data into relational databases. This tool supports nested documents, arrays, ObjectIds, ISODate fields, and more — flattening complex BSON into clean SQL-compatible structures.

Features
Automatic Schema Inference
- Dynamically reads sample documents to determine SQL column names and types
- Supports str, int, float, bool, ObjectId, datetime, nested JSON objects, and arrays
- Converts nested structures into flattened field paths (e.g., address.street → address_street)

MongoDB Extraction
- Connects to your MongoDB Atlas cluster using environment variables
- Reads an entire collection and processes all documents
- Converts BSON → JSON → flattened Python dicts

SQL Conversion
- Auto-generates a CREATE TABLE schema
- Outputs thousands of SQL INSERT statements
- Produces .sql files ready for MySQL, PostgreSQL, or SQLite

Safe, Configurable, and Environment-Based
- Uses .env for MongoDB URI, db name, and collection
- Can process large datasets (your version handled 40k+ rows)
- Logging helps track conversion progress

Tech Stack
Component	      Technology
Language	      Python
Database	      MongoDB Atlas
Libraries	      PyMongo, json, datetime
Output	        SQL Schema + Insert Statements
Env Config	    python-dotenv

Project Structure
MONGOTOSQL/
│
├── converter.py          # Main conversion script
├── requirements.txt

Setup & Installation
1. Install dependencies
pip install pymongo python-dotenv

2. Create a .env file
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/
MONGO_DB=your_database_name
MONGO_COLLECTION=your_collection_name

Usage
Run the converter:
python converter.py

How It Works
1. Connect to MongoDB using PyMongo and the connection details from .env.

2. Retrieve the entire collection. Documents are loaded from MongoDB as Python dicts.

3. Flatten nested objects
Example:
{
  "name": "John",
  "address": { "city": "NYC", "zip": 10001 }
}

Becomes:
name, address_city, address_zip

4. Infer SQL Column Types

Examples:

MongoDB Type	  SQL Type
ObjectId	      TEXT
str	            TEXT
int	            INTEGER
float	          REAL
bool	          BOOLEAN
datetime	      DATETIME
dict/array	    TEXT (serialized JSON)

5. Write SQL Files

CREATE TABLE schema

Bulk INSERT statements

Sanitizes strings and escapes quotes



Project Summary
This project showcases skills in:
- ETL pipeline development
- Database migration
- Schema inference & data modeling
- Working with MongoDB Atlas
- Python scripting & data processing
- Handling large-scale datasets
