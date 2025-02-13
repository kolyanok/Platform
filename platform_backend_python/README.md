## Система авторизации с помощью JWT-токенов

### Info

Система запускается через docker-compose на порту 8000.
База данных (PostgreSQL) - на порту 5432.

Проверка токенов выполняется с помощью алгоритма
**RS256** используя публичный и приватный ключи.

JWT-токены не хранятся в базе данных.

В разделе Endpoints 
приведен пример использования авторизации.

#### Tokens lifetime

access token lifetime = 60 min

refresh token lifetime = 60 days


### Launch

> `cd .../plaform_backend_python`
> 
> `docker-compose up --build`


### API

#### Endpoints

- Получить инфу по любому пользователю по его username

  **GET "127.0.0.1:8000/api/v1/user/{username}"**

  При успешном ответе (status = 200)
  отправляется **публичная** инфа о пользователе.

  ```
  {
    "created_at": "2025-02-13T15:15:41.760573Z",
    "updated_at": null,
    "username": "test_user1"
  }
  ```


- Создать нового пользователя

  BODY:
  ```
  {
    "username": "test_user1",
    "email": "test_email@gmail.com",
    "password1": "test_password1",
    "password2": "test_password1"
  }
  ```
  
  **POST "127.0.0.1:8000/api/v1/user"**

  При успешном ответе (status = 201)
  отправляется инфа о созданном пользователе.
  
  ```
  {
    "created_at": "2025-02-13T15:15:41.760573Z",
    "username": "test_user1",
    "is_active": true,
    "uuid": "5c6b4008-1f70-4a38-8e95-a04f456d692b"
  }
  ```

- Авторизация 
    
  BODY:
  ```
  {
    "username": "test_user1",
    "password": "test_password1"
  }
  ```

  **POST "127.0.0.1:8000/api/v1/auth-jwt/login"**

  При успешном ответе (status = 200) отправляются 
  access и refresh токены как в BODY, так и в Cookies. 

  ```
  {
    "access_token": "{access_token}",
    "refresh_token": "{refresh_token}"
  }
  ```
  

- Получение информации о текущем пользователе по 
  access токену.
  Можно отправить access_token в Cookies или в Headers.
  
  COOKIES:
  ```
  {
    "access_token": "{access_token}"
  }
  ```
  
  HEADERS:
  ```
  Authorization: Bearer {access_token}
  ```
  
  **GET "127.0.0.1:8000/api/v1/auth-jwt/user-info"**

  При успешном ответе (status = 200) 
  отправляется вся инфа о пользователе.

  ```
  {
    "created_at": "2025-02-13T15:15:41.760573Z",
    "updated_at": null,
    "username": "test_user1",
    "email": "test_email@gmail.com",
    "is_active": true,
    "uuid": "5c6b4008-1f70-4a38-8e95-a04f456d692b"
  }
  ```
  
- Обновление access токена через refresh токен.
  
  Можно отправить refresh_token в Cookies или в Headers.
  
  COOKIES:
  ```
  {
    "refresh_token": "{refresh_token}"
  }
  ```
  
  HEADERS:
  ```
  Authorization: Bearer {refresh_token}
  ```
  
  **POST "1127.0.0.1:8000/api/v1/auth-jwt/refresh"**

  При успешном ответе (status = 200)
  отправляется новый access_token 
  как в BODY, так и в Cookies.

  ```
  {
    "access_token": "{access_token}",
    "token_type": "Bearer"
  }
  ```