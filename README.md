# Pizza Delivery API
API desarrollada en [FastAPI](https://fastapi.tiangolo.com/).

Basada en el [tutorial de Ssali Jonathan](https://youtu.be/QQXQAZuJSdw) con algunas modificaciones propias.

## Inicializar la BD
Antes de levantar la API, hay que tener un servidor de [Postgresql](https://www.postgresql.org/) funcionando. Luego hay que correr el script [init_db.py](https://github.com/maxwellnewage/fastapi-pizza-delivery-api/blob/master/database/init_db.py), el cual creará todos los esquemas de tablas que hereden de la clase Base, los cuales podemos encontrar en [models.py](https://github.com/maxwellnewage/fastapi-pizza-delivery-api/blob/master/models.py).

## Configuración en PyCharm
Para poder correr la API, necesitamos un servidor Uvicorn funcionando. Esta es la configuración que armé para correrlo:

![Configuración PyCharm Uvicorn](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rqydt9ddj4p18asbalwr.png)

Los campos más importantes son Module name, Parameters y Working Directory.