import httpx

httpx.post('http://localhost:8000/api/v1/users', json={
    "email": "user@example.com",
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
})
