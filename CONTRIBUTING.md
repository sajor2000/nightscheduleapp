# Contributing to MICU Night Shift Scheduler

Thank you for your interest in contributing to the MICU Night Shift Scheduler!

## Development Setup

1. Clone the repository
```bash
git clone <repository-url>
cd micu-scheduler
```

2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Frontend setup
```bash
cd frontend
npm install
```

4. Database setup
```bash
# Set DATABASE_URL environment variable
# Run the schema script or use init_db.py
python backend/init_db.py
```

## Development Workflow

1. Create a new branch for your feature
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Test your changes
4. Commit with meaningful messages
```bash
git commit -m "feat: add new feature"
```

5. Push and create a pull request

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for functions and classes

### JavaScript (Frontend)
- Use ES6+ features
- Follow React best practices
- Keep components small and focused

### CSS
- Use CSS variables for consistency
- Follow BEM naming convention where applicable
- Mobile-first responsive design

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Test on multiple browsers

## Pull Request Guidelines

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure CI/CD passes
4. Request review from maintainers

## Reporting Issues

- Use the issue template
- Provide clear reproduction steps
- Include browser/environment details

## Questions?

Feel free to open an issue for any questions about contributing.