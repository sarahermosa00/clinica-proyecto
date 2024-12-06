# Sistema de Gestión Clínica con Django


### Sistema para clínica de Fisioterapia que necesita gestionar el diagnóstico de sus pacientes.

---


## Cuenta con un Sistema de Usuarios con los siguientes roles


1. ### Secretaría
    > 📌 Puede agregar, modificar o eliminar los turnos de los Pacientes y los datos de los mismos.


2. ### Profesional médico
    > 📌 Puede agregar observaciones al historial médico de sus pacientes, ver el listado de Pacientes filtrando por día, mes o año.

    > 📌 Solo puede ver los pacientes atendidos que se le fueron asignados.


## Para iniciar el sistema

> Crear un entorno virtual e instalar lo que haya en requerimientos.txt

> Crear las migraciones python manage.py makemigrations

> Migrar a la base de datos python manage.py migrate

> Ejecutar el script inicial python manage.py runscript inicial

> OPCIONAL Cargar datos de prueba python manage.py loaddata datosfake.json