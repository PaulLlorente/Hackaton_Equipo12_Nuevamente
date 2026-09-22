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
