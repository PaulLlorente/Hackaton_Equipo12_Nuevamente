from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

# 1. Al crear la app, deshabilitas la documentación por defecto
app = FastAPI(
    title="NUEVAMENTE EQUIPO 12",
    description="API unificada para Ingestión, Búsqueda Semántica y Generación",
    version="1.0.0",
    docs_url=None  # <- Esto es clave
)

# ... (aquí van tus app.include_router(...) que ya tienes) ...

# 2. Creas una ruta manual para inyectar el tema oscuro
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        # Este CSS transforma todo el fondo y las tipografías a modo oscuro
        swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css"
    )