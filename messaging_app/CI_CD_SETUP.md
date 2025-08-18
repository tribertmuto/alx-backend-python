# CI/CD Setup Guide for Messaging App

This guide covers the complete setup of Jenkins and GitHub Actions for the messaging app.

## 1. Jenkins Setup

### Prerequisites
- Docker installed on your system
- GitHub account with access to the repository

### Installation Steps

1. **Run Jenkins in Docker:**
   ```bash
   cd messaging_app
   ./setup_jenkins.sh
   ```

2. **Access Jenkins:**
   - Open http://localhost:8080
   - Use the provided admin password
   - Install suggested plugins
   - Create admin user

3. **Install Required Plugins:**
   - Git plugin
   - Pipeline plugin
   - ShiningPanda plugin
   - Docker plugin

4. **Configure Credentials:**
   - GitHub credentials (username/password or token)
   - Docker Hub credentials

5. **Create Pipeline Job:**
   - New Item → Pipeline
   - Name: messaging-app-pipeline
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: https://github.com/your-username/alx-backend-python.git
   - Script Path: messaging_app/Jenkinsfile

## 2. GitHub Actions Setup

### Repository Secrets Required
Add these secrets in your GitHub repository settings:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password/token

### Workflows Created

1. **CI Workflow** (`.github/workflows/ci.yml`):
   - Runs on push/PR to main/develop
   - Sets up MySQL test database
   - Runs Django tests with pytest
   - Performs flake8 linting
   - Generates coverage reports

2. **Deployment Workflow** (`.github/workflows/dep.yml`):
   - Builds Docker image
   - Pushes to Docker Hub
   - Runs on main branch pushes and version tags

## 3. Local Testing

### Run Tests Locally
```bash
cd messaging_app
python -m pytest chats/tests.py -v
```

### Run with Coverage
```bash
python -m pytest chats/tests.py --cov=chats --cov-report=html
```

### Linting
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## 4. Jenkins Pipeline Stages

1. **Checkout**: Pulls code from GitHub
2. **Setup**: Creates Python virtual environment
3. **Test**: Runs pytest with coverage
4. **Build**: Creates Docker image
5. **Deploy**: Placeholder for deployment

## 5. GitHub Actions Jobs

1. **test**: Runs Django tests with MySQL
2. **build-and-push**: Builds and pushes Docker image

## 6. Monitoring

### Jenkins
- Access logs: http://localhost:8080/log
- Build history: http://localhost:8080/job/messaging-app-pipeline/

### GitHub Actions
- Check Actions tab in GitHub repository
- View workflow runs and logs

## 7. Troubleshooting

### Jenkins Issues
- If Jenkins won't start, check Docker logs:
  ```bash
  docker logs jenkins
  ```

### GitHub Actions Issues
- Check workflow logs in GitHub Actions tab
- Ensure all secrets are properly configured

### Database Connection Issues
- Ensure MySQL service is running in GitHub Actions
- Check DATABASE_URL format in environment variables
