from pydantic import BaseModel
from typing import List,Literal

#Validación y estructura de los datos de salida
class Resumen(BaseModel):
    formato:Literal["resumen"]
    conceptos_clave:str
    tiempo_estudio:int
    evaluacion_calidad:str
    contenido_adaptado:str

class Tarjetas(BaseModel):
    pregunta:str
    respuesta:str

class Flashcards(BaseModel):
    formato:Literal["flashcard"]
    conceptos_clave:str
    tiempo_estudio:int
    evaluacion_calidad:str
    contenido_adaptado: List[Tarjetas]

class PreguntasQuiz(BaseModel):
    pregunta:str
    opciones:str
    respuesta_correcta:str

class Quiz(BaseModel):
    formato:Literal["quiz"]
    conceptos_clave:str
    tiempo_estudio:int
    evaluacion_calidad:str
    contenido_adaptado: List[PreguntasQuiz]

class Escena(BaseModel):
    marca_tiempo: str  
    numero_escena: int  
    narrador: str  

class Guion(BaseModel):
    formato:Literal["guion"]
    titulo: str  
    tiempo_estimado: str  
    escenas: List[Escena]  
from typing import Union
from pydantic import Field

# Contrato de entrada para el endpoint /adaptar
class AdaptarRequest(BaseModel):
    query: str = Field(..., description="Pregunta, tema o concepto a consultar")
    tenant_id: str = Field(default="default", description="Identificador del tenant o usuario")
    perfil: Literal["principiante", "intermedio", "avanzado"] = Field(
        default="intermedio", 
        description="Perfil pedagógico de la audiencia"
    )
    formato: Literal["resumen", "flashcard", "quiz", "guion"] = Field(
        default="resumen", 
        description="Formato educativo deseado"
    )
    top_k: int = Field(default=3, ge=1, le=10, description="Cantidad de fragmentos a recuperar del RAG")

# Unión tipada para respuesta según el formato seleccionado
AdaptarResponse = Union[Resumen, Flashcards, Quiz, Guion]