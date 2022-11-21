import uvicorn
from fastapi import FastAPI
from Controllers.NumberController import numberController
from Controllers.PhotoController import photoController
from Controllers.AuthController import authController
from Controllers.DateController import dateController
from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.include_router(numberController)
app.include_router(photoController)
app.include_router(authController)
app.include_router(dateController)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == '__main__':
    uvicorn.run(app)
