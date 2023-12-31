# Ecolyo Home Monitor

Integrates the cozy `ecolyo` module in Home Assistant to provide electricity, gas, and water consumption.

### Installation

1. Generate JWT key

Open your terminal and write the command given below, this will give you a secret key which we will for authentication.

```sh
echo "JWT_SECRET=$(openssl rand -hex 32)" >> .env
```

2. Run docker containers

```sh
docker compose build --pull --no-cache
docker compose up --detach
```

### Authorization flow

This process ensures that the client application can access a user's Cozy data with the user's consent, while also maintaining security and privacy standards.

#### 1. Frontend Sends Create Client Request

The frontend wants to initiate the process of registering a client with the Cozy platform.

- The frontend application sends an HTTP POST request with client_url and client_name to the API requesting the creation of a client.

#### 2. API Returns the URL Pointing to Cozy Authorize Endpoint

The API processes the client registration request and return the Cozy platform's authorization url.

- The API communicates with Cozy's servers to register the client if it does not exist.
- Cozy's servers respond with the client informations.
- The API create the client and sends the cozy's authorization URL to the frontend.

#### 3. Frontend Confirms Registration on Cozy Page

The user confirms on the Cozy platform that they authorize the client application to access their Cozy data.

- The frontend redirects the user to the Cozy authorization URL received in the previous step.
- On the Cozy page, the user logs in (if not already logged in) and grants the necessary permissions to the client application.

#### 4. Cozy Redirects to the API

Once the user has granted permissions, Cozy needs to inform the API that the user has authorized the client.

- After the user grants permissions, Cozy redirects the user to the API's redirect URI.
- This redirect contains an authorization code that the API can use to obtain access tokens.

#### 5. API Saves Cozy Tokens and Redirects to the Frontend with its Own Bearer Access Token

The API exchange the authorization code for Cozy tokens.

- The API sends the received authorization code to Cozy's token endpoint to obtain an access token and a refresh token.
- The API securely saves these Cozy tokens for future requests to Cozy on behalf of the client.
- The API then generates its own bearer access token for the frontend.
- The frontend is redirected back with this token so it can make authenticated requests to the API.

### Ressources

- [Ecolyo](https://forge.grandlyon.com/web-et-numerique/factory/llle_project/ecolyo)

- [Cozy](https://docs.cozy.io/en/cozy-stack/mango/)

