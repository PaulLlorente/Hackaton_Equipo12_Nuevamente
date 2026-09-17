# 📋 Guía de Flujo de Trabajo y Uso del Tablero Kanban – NuevaMente

Este documento establece las reglas y el flujo operativo oficial para la gestión de tareas del **G10-LATAM-equipo-12** utilizando **GitHub Projects**.

---

## 🎯 Objetivo del Tablero
Centralizar el progreso del desarrollo del MVP, mantener la transparencia de las actividades y asegurar que cada miembro del equipo sepa qué hacer, qué se está desarrollando y qué falta por validar.

---

## 🗂️ Significado y Uso de las Columnas

Nuestro tablero Kanban está dividido en cuatro estados clave que reflejan el ciclo de vida de cada tarea:

### 1. 🔵 Por Hacer / Pendiente (`Backlog / Ready`)
* **¿Qué es?:** El repositorio de tareas planificadas para el Sprint actual.
* **Cuándo se usa:** Aquí se ubican todas las tareas definidas que aún no han sido tomadas por ningún integrante. 
* **Regla:** Ningún código debe empezar a escribirse si la tarjeta no ha pasado previamente por esta columna.

### 2. 🟡 En progreso / Trabajándose (`In Progress`)
* **¿Qué es?:** El espacio de desarrollo activo.
* **Cuándo se usa:** Cuando un integrante toma un *Issue* del tablero, se lo asigna, crea su rama de trabajo (`feature/nombre-tarea`) en su entorno local y **comienza a programar**.
* **Regla:** Para mantener el enfoque y evitar cuellos de botella, **se recomienda no tener más de 2 o 3 tareas simultáneas** en esta columna por persona.

### 3. 🟣 En revisión / Control de calidad (`In Review`)
* **¿Qué es:** La fase de validación de código.
* **Cuándo se usa:** Se mueve automáticamente (o manualmente) cuando el desarrollador termina la tarea, sube su rama a GitHub y **abre un Pull Request (PR)** hacia la rama protegida `main`.
* **Regla:** Ninguna tarjeta avanza a la siguiente columna si no cuenta con el análisis y la **aprobación de al menos un revisor** (otro compañero del equipo o el Project Manager).

### 4. 🟠 Completado (`Done`)
* **¿Qué es:** El hito final de la tarea.
* **Cuándo se usa:** Cuando el Pull Request ha sido **aprobado y fusionado (*merged*) exitosamente** en la rama principal `main`.
* **Regla:** ¡Tarea terminada y probada! El código ya forma parte oficial de la versión actual del proyecto.

---

## ⚙️ Buenas Prácticas para el Equipo

1. **Vincular Pull Requests:** Al abrir un PR en GitHub, asegúrate de enlazarlo con su respectiva tarjeta del tablero o *Issue* para automatizar el movimiento de estados.
2. **Actualización en Dailys:** Durante nuestras sincronizaciones, revisaremos este tablero para identificar bloqueos si una tarjeta pasa demasiado tiempo en *"En progreso"* o *"En revisión"*.
3. **Claridad en los Títulos:** Los *Issues* creados deben tener títulos descriptivos (ej. *[Backend] Integración de ChromaDB para embeddings*).