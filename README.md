# GT-Challenge

Challenge for GlobalTask

## Stack

- Poetry
- FastAPI
- SQLAlchemy
- htmx

## Setup

## Supuestos

- las personas pueden cambiar de correo
- los vehiculos pueden ser repatentados cambiando su patente
- los oficiales necesitan un password para generar el token
- los oficiales no pueden cambiar su número identificatorio

## Mejoras

- sistema de usuarios para administar person, vehículo, oficiales e infracción
- la interfaz necesita autenticación y autorización
- paginación en interfaces
- generar refresh_token

## Generación de token

Se deja endoint e interfaz para fácil consulta

con la interfaz:

1 - Con el explorador navegar al localhost puerto seteado (http://127.0.0.1:8000/)
2 - ir a Interface y luego a Oficial
3 - crear un oficial (el password lo usará luego, procure no olvidarlo)
4 - volver a home con botón home
5 - a traves de la interfaz ubicada en raiz navegar a "Token / login", esto es url "/login"
6 - complete nombre de oficial y password generado
7 - el token generado será reenderizado en el mismo formulario para fácil copiado

con el endpoint:
crear un oficial como se indicó a través de la interfaz

método post: "/api/v1/login/access-token"
payload tipo form con contenido:
username: el nombre del oficial
password: el password del oficial

ej usando curl

```bash

curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/login/access-token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=officer_name&password=officer_password'
```

## Comandos

generar interfaces

chequear que endpoint api generar infracción devuelva 500
indicar como generar token

5. Por último, cree una imagen Docker que permita ejecutar todos los componentes
   de la solución (servidor de apps, bd, etc) y súbala al repo público de Docker, de
   forma que esta pueda ser descargada y ejecutada fácilmente.

# Arquitectura en AWS

> Proponga una arquitectura de servicios AWS que sea compatible con el despliegue de esta aplicación en producción. Haga un listado de los servicios que recomendaría y justifique su elección.

Arquitectura de cointeiners serverless.

Para la presente solución se propone desplegar en servicios tipo Serverles como es Fargate, con uso de balanceador de carga. Respecto a la base de datos se recomienda utilizar RDS.

Es importante destacar que la base de datos debe de desplegarse en una subnet privada (sin internet gateway), con las rutas en route table correctamente configuradas para que NO sea accesible desde internet, sólo desde la subnet donde se despliega el backend de la app.

## Servicios:

Route53: administración de entradas de dns, simplifica la gestión de otros servicios como load balancer. de costo muy bajo.

AWS EKR: almacenamiento de imágenes privadas docker

AWS ECS: aquí se montan las imágenes, permite simple gestión a través de de task y services. Implementación sensilla de logs con aws CloudWatch. También permite la captura de métricas para su monitoreo.
Otros puntos importantes son la simple configuración de Healt checks, posible despliegue Blue/Green.

Elastic Load Balancing: Balanceo de carga y routing son indispensables si el tráfico es elevado. Es recomendable el uso de Application Load Balancer evitando Load balancer Tradicional ya que provee mejores features. Como simple enlace y setup con ECS, gestiona el trafico en caso de despliegue Blue/Green.

RDS: Base de datos relacional con multiples motores, escalable y de fácil configuración.

SecretsManager: Gestion de secretos, aqui debe guardarse las credenciales de DB y otros servicios delicados, permite la rotación de credenciales sin necesidad de reiniciar servicios ya que el proceso de la app puede solicitarlos y no por variables de ambiente.

CI/CD: dependiendo el proveedor de repositorio git. Puede ser GithubActions o si se se trabaja con CodeCommit (repositorio git de aws) pueden utilizarse CodePipeline para la gestion del pipeline y CodeBuild para build de imágen y correr test.
