# ISTS16-Backend
Backend of ecommerce website

# API

## POST /login
Login with a users credentials, send token with credentials, will be attached to the account if successfully logged in

### Parameters
```
{
    username: [string],
    password: [string],
}
```

### Response
**Status Code: 200**
```
{
    token: [string]
}
```
**Status Code: 400+**
```
{
    error: [string]
}
```
---

## POST /validate-session
Validates a users session is still authorized

### Parameters
```
{
    token: [string],
}
```

### Response
**Status Code: 200**
```
{
    success: [string]
}
```
**Status Code: 400+**
```
{
    error: [string]
}
```
---

## POST /update-password
Update a users password

### Parameters
```
{
    old_password: [string],
    new_password: [string],
    username: [string],
}
```

### Response
**Status Code: 200**
```
{
    success: [string]
}
```
**Status Code: 400+**
```
{
    error: [string]
}
```
---

## POST /expire-session
Expire a session for a user

### Parameters
```
{
    token: [string],
}
```

### Response
**Status Code: 200**
```
{
    success: [string]
}
```
**Status Code: 400+**
```
{
    error: [string]
}
```
---

## POST /update-session
Update a users session from and old token to a new one

### Parameters
```
{
    old_token: [string],
    new_token: [string],
}
```

### Response
**Status Code: 200**
```
{
    success: [string]
}
```
**Status Code: 400+**
```
{
    error: [string]
}
```
---
