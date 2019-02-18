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

## POST /get-balance
Get the balance for the users account

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
    balance: [int]
}
```
**Status Code: 400+**
```
{
    error: [string]
}
```
---

## POST /buy
Buy a particular item from the store

### Parameters
```
{
    token: [string],
    item_id: [int],
}
```

### Response
**Status Code: 200**
```
{
    transaction_id: [int]
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

## POST /transactions
Return a list of the transactions made on their account

### Parameters
```
{
    token: [string]
}
```

### Response
**Status Code: 200**
```
{
    transactions: [array[strings]]
}
```
**Status Code: 400+**
```
{
    error: [string]
}
```
---

## POST /items
Return a list of the items to be bought from whiteteam store

### Parameters
```
{
    token: [string]
}
```

### Response
**Status Code: 200**
```
{
    items: [array[dicts]]
}
```
**Status Code: 400+**
```
{
    error: [string]
}
```
---

## POST /transfer
Transfer money from one team to another

### Parameters
```
{
    token: [string],
    recipient: [int],
    amount: [int]
}
```

### Response
**Status Code: 200**
```
{
    transaction_id: [int]
}
```
**Status Code: 400+**
```
{
    error: [string]
}
```
---