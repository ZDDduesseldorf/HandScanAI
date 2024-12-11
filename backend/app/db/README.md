# MongoDB with Beanie

This is a short guide how to interact with our MongoDB database with Beanie. First get the Docker container running and started the backend server (refer to the Backend README for setup instructions).

---

## Usage Steps

### 1. Import the Models
Start by importing the required Beanie models:
```python
from app.db.models import MetadataModel, ImagesModel
```

### 2. Create a New Document and Insert It
You can create a new document and insert it into the database as follows:
```python
entry = ImagesModel(id="test", original_image="Testbild")
await entry.insert()
```

### 3. Query for an Entry
To query the database for specific entries, use the following syntax:
```python
result = await ImagesModel.find(ImagesModel.id == 'test').to_list()
```
This will return a list of all matching documents.

### 4. Delete a Collection
To delete an entire collection from the database:
```python
await ImagesModel.get_motor_collection().drop()
```

---

Take a look at the Beanie focumentation/tutorial for more help: https://beanie-odm.dev/tutorial/finding-documents/



