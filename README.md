**GET получить список организаций**
http://127.0.0.1:8000/api/organizations

ответ json
список организаций

[
  {
    "id" - id организации,
    "fullname" - полное наименование,
    "shortname" - короткое наименование
  }
]

**POST регистрация пользователя**
http://127.0.0.1:8000/api/register

data

{
  "email" - емайл,
  "password"- пароль,
  "surname" - Фамилия,
  "firstname" - имя,
  "phone" тел. номер,
  "id_organizations" - id'ки связанных организаций (list)
}

file - фото

ответ json c емайлом пользователя
{
  "email" - емайл
}

**GET получить список всех пользователей**
http://127.0.0.1:8000/api/users

ответ

[
  {
    "id" -id пользователя, 
    "organizations": - список организаций
    {
        "id" - id организации,
        "fullname"- наименование организации,
        "shortname"- короткое наименование организации
    },
    "email" - емайл,
    "password"- пароль,
    "surname" - фамилия,
    "firstname" - имя,
    "phone" тел. номер,
    "photo" - расположение фото, может быть null
  }
]

**POST редактирование пользователя**
http://127.0.0.1:8000/api/edit/user

data - то же что и в регистрация пользователя
если поле не редактируется, то он должно присутствовать и должно быть пустое
file - то же что и в регистрация пользователя

token - токен авторизации

ответ json c емайлом пользователя

{
  "email" - емайл
}

**GET информация о пользователе**
http://127.0.0.1:8000/api/user

data

{"id" - id'к пользователя}

ответ

{
  "user": 
  [
    {
      "id": 17,
      "email" - емайл,
      "password"- пароль,
      "surname" - фамилия,
      "firstname" - имя,
      "phone" тел. номер,
      "photo" - расположение фото, может быть null
    }
  ],
  "organizations":
  [
    {
      "id"- id организации,
      "fullname": - наименование организации,
      "shortname": - короткое наименование организации
    }
  ]
}

**POST авторизация пользователя**
http://127.0.0.1:8000/api/login
data
{"email"- емайл,
"password" - пароль}
в случае успешной авторицазии возвращается json

{"token" - токен авторизации (при успешной авторизации),

"auth" - access - в случае успешной авторизации, fail - не успешная авторизация}

**POST добавление новой организации**
http://127.0.0.1:8000/api/add_organization

data

{"fullname"- наименование организации,
"shortname"- короткое наименование организации}

ответ - json

{"fullname" - наименование организации}