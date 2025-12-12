# Contributing to Event Horizon

Thank you for your interest in contributing to Event Horizon! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/EventHorizon.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Development Setup

### Using Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Using Docker

```bash
docker-compose up
```

## Code Style

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Write self-documenting code

## Testing

Before submitting a PR:

1. Run existing tests: `python manage.py test`
2. Add tests for new features
3. Ensure all tests pass
4. Test manually in the browser/API

## Commit Messages

Write clear, concise commit messages:

- Use the imperative mood ("Add feature" not "Added feature")
- Start with a capital letter
- Don't end with a period
- Reference issues and PRs when applicable

Examples:
```
Add event search functionality
Fix registration bug for full events
Update API documentation for new endpoints
```

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the API.md if API endpoints are modified
3. Add or update tests for your changes
4. Ensure your code follows the project's code style
5. Update documentation for any new features
6. Your PR will be reviewed by maintainers

## API Changes

When making API changes:

1. Update serializers if needed
2. Update views/viewsets
3. Update URL configurations
4. Document in API.md
5. Add tests for new endpoints
6. Ensure backward compatibility when possible

## Database Changes

When modifying models:

1. Create migrations: `python manage.py makemigrations`
2. Test migrations: `python manage.py migrate`
3. Update admin.py if needed
4. Update serializers
5. Consider data migration needs

## Adding New Features

1. Discuss major features in an issue first
2. Keep PRs focused on a single feature
3. Add documentation
4. Add tests
5. Update relevant files (README, API.md, etc.)

## Bug Reports

When reporting bugs, include:

- Clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

## Feature Requests

When requesting features:

- Explain the use case
- Describe the expected behavior
- Provide examples if possible
- Discuss potential implementation approaches

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

Reviewers will check:
- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Security considerations

## Questions?

Feel free to open an issue for questions or join our discussions.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).
