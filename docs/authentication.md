# Authentication Service Guide

## Overview
The Authentication Service is a critical component responsible for user sign-up, login, and session management. It uses JWT (JSON Web Tokens) for secure communication between the client and server.

## Login Flow
1. User provides email and password.
2. The server validates the credentials against the database.
3. Upon success, the server generates a JWT containing the user's ID and role.
4. The token is sent back to the client and stored for subsequent requests.
The default expiration for a token is 24 hours.