# Generic HTTP Web Service Client in Python (GHoWSt)

## A client written to talk to the Generic HTTP Web Service Server

### Design goals

- Use local language semantics to talk to the server dynamically. The only thing
  required are the ghowst classes and 3rd party dependencies from the
  requirements.txt.
- Every call, using a method name convention to map to HTTP methods, gets
  translated to HTTP requests. Responses are parsed from JSON and mapped back to
  local objects.

### Example code

```python
import types

from weburg.ghowst.generic_http_web_service_client import *


http_web_service = GenericHTTPWebServiceClient("http://localhost:8081/generichttpws")

# Create
engine = types.SimpleNamespace()
engine.name = "PythonEngine"
engine.cylinders = 44
engine.throttle_setting = 49
engine_id1 = http_web_service.create_engines(engine=engine)
```

### Running the example

First, ensure the server is running. Refer to other grouped GHoWSt projects to
get and run the server. Ensure Python 3 is installed. Then, using pip or your
IDE, ensure that the dependencies in requirements.txt are installed to your
Python environment.

If using the CLI, ensure you are in the project directory. Run:

`python run_example_generic_http_web_service_client.py`

If using an IDE, you should only need to run the below file:

`run_example_generic_http_web_service_client.py`

The example runs several calls to create, update, replace, read, delete, and do
a custom action on resources.
