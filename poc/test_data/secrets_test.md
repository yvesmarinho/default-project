# Security Test: Secrets Detection

This file contains intentional secrets for testing sanitization.

## API Key (should be detected)
api_key = "sk_test_1234567890abcdefghijklmnop"

## Password (should be detected)
password: "mySecretP@ssw0rd123"

## GitHub Token (should be detected)
export GITHUB_TOKEN=ghp_1234567890123456789012345678901234567

## Email (PII, should be detected)
Contact: john.doe@example.com

## AWS Key (should be detected)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE

## Safe content (should NOT be detected)
This is a normal sentence about passwords in general.
The word "token" can appear in documentation safely.
