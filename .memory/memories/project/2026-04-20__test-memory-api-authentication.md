---
title: Test Memory — API Authentication
category: project
tags: test,  api,  authentication,  jwt
---
# API Authentication Pattern

## Decision
Use JWT tokens with 1h expiration for API authentication.

## Rationale
- Stateless (no server-side session storage)
- Short expiration minimizes risk
- Refresh tokens allow seamless renewal

## Implementation
JWT tokens stored in Authorization header.
Refresh tokens in httpOnly cookies.