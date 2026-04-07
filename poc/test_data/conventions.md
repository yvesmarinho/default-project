# Team Conventions: Python Style

## Naming
- **snake_case** for variables, functions, methods
- **PascalCase** for classes
- **SCREAMING_SNAKE_CASE** for constants

## Imports
- Standard library first
- Third-party second
- Local imports last
- Alphabetize within groups

## Type Hints
- Required for all public functions
- Optional for private methods (use judgment)

## Docstrings
- Google style for public API
- One-liner for simple functions
- Include Args, Returns, Raises for complex functions

## Testing
- pytest for all tests
- Minimum 80% coverage
- Use fixtures for setup/teardown
