import types
from weburg.ghowst.generic_http_web_service_client import *


http_web_service = GenericHTTPWebServiceClient("http://localhost:8081/generichttpws")

### Photo ###

# Create
photo = types.SimpleNamespace()
photo.caption = "Some Python K"
photo.photo_file = open("python.jpg", 'rb')
http_web_service.create_photos(photo=photo)

### Engine ###

# Create
engine = types.SimpleNamespace()
engine.name = "PythonEngine"
engine.cylinders = 44
engine.throttle_setting = 49
engine_id1 = http_web_service.create_engines(engine=engine)

# CreateOrReplace (which will create)
engine = types.SimpleNamespace()
engine.id = -1
engine.name = "PythonEngineCreatedNotReplaced"
engine.cylinders = 45
engine.throttle_setting = 50
http_web_service.create_or_replace_engines(engine=engine)

# Prepare for CreateOrReplace
engine = types.SimpleNamespace()
engine.name = "PythonEngine2"
engine.cylinders = 44
engine.throttle_setting = 49
engine_id2 = http_web_service.create_engines(engine=engine)

# CreateOrReplace (which will replace)
engine = types.SimpleNamespace()
engine.id = engine_id2
engine.name = "PythonEngine2Replacement"
engine.cylinders = 56
engine.throttle_setting = 59
http_web_service.create_or_replace_engines(engine=engine)

# Prepare for Update
engine = types.SimpleNamespace()
engine.name = "PythonEngine3"
engine.cylinders = 44
engine.throttle_setting = 49
engine_id3 = http_web_service.create_engines(engine=engine)

# Update
engine = types.SimpleNamespace()
engine.id = engine_id3
engine.name = "PythonEngine3Updated"
http_web_service.update_engines(engine=engine)

# Get
engine = http_web_service.get_engines(id=engine_id1)
print(f"Engine returned: {engine.name}")

# Get all
engines = http_web_service.get_engines()
print(f"Engines returned: {len(engines)}")

# Prepare for Delete
engine = types.SimpleNamespace()
engine.name = "PythonEngine4ToDelete"
engine.cylinders = 89
engine.throttle_setting = 70
engine_id4 = http_web_service.create_engines(engine=engine)

# Delete
http_web_service.delete_engines(id=engine_id4)

# Custom verb
http_web_service.restart_engines(id=engine_id2)