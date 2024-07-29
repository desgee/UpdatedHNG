# User Management and Organization API using Flask #
This is a Python API using Flask Framework that Connects the application to a Postgres database server. ORM like SQLAlchemy was used

**Base Endpoint**
(https://updated-hng.vercel.app)

````
Endpoints implemented:
[POST]   https://updated-hng.vercel.app/auth/register
[POST]   https://updated-hng.vercel.app/auth/login
[POST]	https://updated-hng.vercel.app/api/organisations[PROTECTED]
[GET]   https://updated-hng.vercel.app/api/users/:id
[GET]	https://updated-hng.vercel.app/api/organisations/:orgId[PROTECTED]
[POST]  https://updated-hng.vercel.app/api/organisations/:orgId/users[PROTECTED]
[GET] https://updated-hng.vercel.app/api/organisations[PROTECTED]
````


**Register Endpoint [POST]**

> base_url/auth/register
This endpoint Registers a user and creates a default organisation 

**Register request body:**
```
{
	"firstName": "string",
	"lastName": "string",
	"email": "string",
	"password": "string",
	"phone": "string",
}
```
**Login request body:**

**Login Endpoint**
> [POST] /auth/login : logs in a user. When you log in, you can select an organisation to interact with
````
{
	"email": "string",
	"password": "string",
}
````
**Get a user Organization(s) Endpoint**
> [GET] /api/organisations: a user gets their own record or user record in organisations they belong to or created [PROTECTED]

**Get a single organization Endpoint**
> [GET] /api/organisations/:orgId the logged in user gets a single organisation record [PROTECTED]

**Create organization Endpoint**
> [POST] /api/organisations : a user can create their new organisation [PROTECTED]

```
{
	"name": "string", // Required and cannot be null
	"description": "string",
}
```

**Add a user to a particluar organization Endpoint**
> [POST] /api/organisations/:orgId/users : adds a user to a particular organisation

````
{
	"userId": "string"
}
````
````
Framework:
Flask
Python Version:
3.11.9
Vercel: used for application deployment and hosting.
Supabase: used for PostgresQL Database deployment and hosting.
````
