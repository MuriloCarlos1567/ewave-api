# eWave API
This API was built to be evaluated in a technical challenge and will not be used for professional purposes. Feel free to use as you wish.

## Endpoints:

### Products
This request will return all registered products and may receive parameters to filter the query.

- URL: '/api/v1/products'
- Method: **GET**

### Product
This request is used to register a new product. 

This request is used to view a single product.

- URL: '/api/v1/products/{productId}'
- Method: **GET**

And

**This endpoint can only be used if you are logged in**.
- URL: '/api/v1/products/{productId}'
- Method: **POST**
- Header:
Content-Type = application/json
Authorization = Bearer {token}
- RequestBody:

```d
{
    "productName": 'Vinho Robert Mondavi Woodbridge Cabernet Sauvignon 750 ml',
    "category": 'Wine',
    "amount": 23,
    "description": 'As uvas são maceradas e fermentadas em cubas de aço inox com controle de temperatura. Para melhor retenção de seu caráter frutado as uvas são prensadas ao final da fermentação. O vinho amadureceu em barricas de carvalho francês e americano.',
    "price": 89.90
}
```

#### Filter parameters
- minprice -> Minimum product price, default: 0
- maxprice -> Maximun product price, default: 10000
- category -> Category of all products
- limit -> Maximum number of products displayed per page
- offset -> Number of elements to skip

You can use the filters with '?' for the first param and the '&' operator:
'/api/v1/products?minprice=15&maxprice=120'

____

### User
Endpoint used to view a user
- URL: '/api/v1/users/{userId}'
- Method: **GET**

Note: The 'userId' must be an integer.

____

### Register
Request used to register users.

- URL: '/api/v1/register'
- Method: **POST**
- Header:
Content-Type = application/json
- Request Body:
```d 
{
    "login": "admin",
    "email": "example@admin.com",
    "password": "admin"
}
```
**IMPORTANT NOTE:** When you register, your account is not yet active and you need to activate it in your email. To make it easier to use, the next **endpoint (Confirm)** will also activate the user without the need for confirmation by email.
____

### UserConfirm
Endpoint created to facilitate application testing

- URL: '/api/v1/confirm/{userId}'
- Method: **GET**

**Note**: This request will return a HTML coded used in the email confirmation.

____

### AdminConfirm
Initially created to escalate privileges but not completed.

- URL: '/api/v1/admin/{userId}'
- Method: **GET**
____

### Login
The 'login' endpoint will give you your token to access some endpoints.
- URL: '/api/v1/login'
- Method: **POST**
- Header:
Content-Type = application/json
- Request Body:
```d
{
    "login": "admin",
    "password": "admin"
}
```
This endpoint will return your access token.

____

### Logout
The 'logout' endpoint will cause your access token to expire.
- URL: '/api/v1/logout'
- Method: **POST**
- Authorization = Bearer {token}

___

### PriceCheck
This endpoint will show you the price of your purchase query

- URL: '/api/v1/price'
- Method: **POST**
- Body Request:
```d
{
    "priceProduct": "robert",
    "priceAmount": 3
}
```

The Response Body will not be saved in database.

____

### Order
Endpoint created to check single orders.

- URL: 'api/v1/orders/{orderId}'
- Method: **GET**

____

### Orders
Endpoint used to check all orders.

- URL: '/api/v1/orders'
- Method: **GET**

### NewOrder
This endpoint will save the orders in the database.

- URL: '/api/v1/buy'
- Method: **POST**
- Body Request:
```d
{
    "orderProduct": "robert",
    "orderAmount": 2,
    "orderEmail": "example@admin.com",
    "orderPassword": "admin"
}
```

____

# Final talk
##### I had a lot of ideas to apply to this API but the weather didn't help me.

##### Some improvements:
- Cart System
- Privilege System
- Docker
- Microservice-based architecture
- Postgresql
