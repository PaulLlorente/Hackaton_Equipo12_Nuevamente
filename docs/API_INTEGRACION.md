# Guia Tecnica: API RAG + JWT Supabase

**Rama:** feature/hrax-api-rag-integration

## 1. Requisitos e instalacion
```bash
git checkout feature/hrax-api-rag-integration
git pull origin feature/hrax-api-rag-integration
pip install -r requirements.txt
```

## 2. Variables de entorno
Crear un archivo .env en la raiz:
```env
SUPABASE_JWT_SECRET=<JWT_SECRET_DEL_PROYECTO_SUPABASE>
```

## 3. Ejecucion del servidor
- Git Bash / Linux / macOS:
  PYTHONPATH=. python -m uvicorn src.api:app --reload
- Windows CMD:
  set PYTHONPATH=. && python -m uvicorn src.api:app --reload
- Windows PowerShell:
  $env:PYTHONPATH="."; python -m uvicorn src.api:app --reload

## 4. Endpoints
- Swagger: http://127.0.0.1:8000/docs
- Healthcheck: GET /health (retorna 200 OK)
- Protegidos: POST /api/search y POST /api/ingest (requieren header Authorization: Bearer <access_token>)
