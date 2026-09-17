🔀 Guía de Control de Versiones y GitHub Flow – NuevaMente
Este documento establece el estándar obligatorio de versionado de código y el flujo de trabajo mediante ramas para todo el G10-LATAM-equipo-12. Ningún miembro debe hacer modificaciones directas sobre la rama principal.

🚀 Las 6 Reglas de Oro de GitHub Flow

1. Sincronización Inicial
Antes de iniciar cualquier tarea nueva, asegúrate de tener tu repositorio local actualizado con los últimos cambios de la rama principal (main):

git checkout main
git pull origin main

2. Creación de una Rama de Trabajo (feature/...)
Por cada tarea o Issue asignado en el tablero, debes crear una rama independiente utilizando una descripción corta y clara:

Sintaxis: git checkout -b feature/nombre-de-la-tarea

Ejemplo: git checkout -b feature/extraccion-pdf

3. Desarrollo y Commits Frecuentes
Trabaja localmente en tu rama implementando la solución. Realiza commits frecuentes y utiliza mensajes descriptivos sobre lo que estás añadiendo:


git add .
git commit -m "feat: implementa script de lectura de pdf con PyPDF"
git push origin feature/extraccion-pdf

4. Apertura del Pull Request (PR)
Una vez finalizada y probada la tarea en tu entorno local:

Sube tu rama definitiva a GitHub (git push).

Abre un Pull Request (PR) desde tu rama feature/... hacia la rama protegida main.

En la descripción del PR, explica brevemente el alcance de tus cambios y enlaza el Issue correspondiente del tablero.

5. Revisión Obligatoria de Código (Code Review)
Para mantener la calidad técnica del MVP:

Ningún PR puede fusionarse (merge) sin la revisión previa.

Es obligatorio contar con la aprobación de al menos 1 integrante diferente al creador (o del Project Manager) mediante el botón de Approve.

6. Integración y Limpieza
Una vez aprobado el PR y sin conflictos de código:

Haz clic en Merge pull request para integrar los cambios a main.

Borra la rama temporal de tu equipo tanto en local como en remoto para mantener el repositorio limpio y ordenado.