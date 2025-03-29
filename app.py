from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

from routes.user_info import users

info = Info(title="Main API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Define the documentation tag
home_tag = Tag(name="Documentation", description="Selection of documentation style: Swagger, Redoc, or RapiDoc")

@app.get('/', tags=[home_tag])
def home():
    """
    Redirects to /openapi, where the user can choose the documentation style.
    """
    return redirect('/openapi')

app.register_api(users)
