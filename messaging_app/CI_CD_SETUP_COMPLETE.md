# Complete CI/CD Setup Guide for Messaging App

## Overview
This guide provides step-by-step instructions to set up the complete CI/CD pipeline for the messaging app using Jenkins and GitHub Actions.

## ✅ Completed Updates
- **Jenkinsfile**: Updated with correct GitHub repository and Docker Hub credentials
- **GitHub Workflows**: Updated CI and deployment workflows with correct repository details
- **Requirements**: All dependencies are properly configured

## 🚀 Jenkins Setup Instructions

### 1. Install Jenkins in Docker Container
```bash
# Run the setup script
chmod +x messaging_app/setup_jenkins.sh
./messaging_app/setup_jenkins.sh

# Or manually run:
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

### 2. Configure Jenkins
1. **Access Jenkins**: Open http://localhost:8080
2. **Get initial password**: 
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. **Install plugins**: Choose "Install suggested plugins"
4. **Create admin user**: Follow the setup wizard

### 3. Install Required Plugins
- Git plugin
- Pipeline plugin
- ShiningPanda plugin
- Docker Pipeline plugin

### 4. Configure Credentials
1. **GitHub Credentials**:
   - Go to Manage Jenkins → Manage Credentials → Add Credentials
   - Kind: Username with password
   - ID: `github-credentials`
   - Username: Your GitHub username
   - Password: Your GitHub token

2. **Docker Hub Credentials**:
   - Go to Manage Jenkins → Manage Credentials → Add Credentials
   - Kind: Username with password
   - ID: `docker-hub-credentials`
   - Username: `tribert`
   - Password: Your Docker Hub token

### 5. Create Jenkins Pipeline
1. **New Item** → **Pipeline**
2. **Name**: messaging-app-pipeline
3. **Definition**: Pipeline script from SCM
4. **SCM**: Git
5. **Repository URL**: https://github.com/tribert/alx-backend-python.git
6. **Script Path**: messaging_app/Jenkinsfile

## 🔧 GitHub Actions Setup

### 1. Repository Secrets
Add these secrets to your GitHub repository:
- `DOCKER_USERNAME`: tribert
- `DOCKER_PASSWORD`: Your Docker Hub password/token

### 2. Verify Workflows
The workflows are already configured:
- **CI**: `.github/workflows/ci.yml` - Runs tests on push/PR
- **Deployment**: `.github/workflows/dep.yml` - Builds and pushes Docker image

## 🧪 Testing the Pipeline

### 1. Test Jenkins Pipeline
1. Go to Jenkins dashboard
2. Click on your pipeline job
3. Click "Build Now"
4. Monitor the console output

### 2. Test GitHub Actions
1. Push changes to the main branch
2. Check the Actions tab in GitHub
3. Verify all workflows pass

## 📋 Pre-deployment Checklist

### Jenkins
- [ ] Jenkins is running on port 8080
- [ ] GitHub credentials are configured
- [ ] Docker Hub credentials are configured
- [ ] Pipeline job is created and configured
- [ ] First build is successful

### GitHub Actions
- [ ] Repository secrets are added
- [ ] Workflows are triggered on push
- [ ] All tests pass
- [ ] Docker image is built and pushed

## 🐛 Troubleshooting

### Common Issues
1. **Docker permission denied**: Ensure Docker socket is mounted correctly
2. **GitHub authentication**: Verify GitHub token has correct permissions
3. **MySQL connection**: Check MySQL service is running and accessible

### Debug Commands
```bash
# Check Jenkins logs
docker logs jenkins

# Test Docker build
cd messaging_app
docker build -t messaging-app-test .

# Test pytest
python -m pytest chats/tests.py -v
```

## 📞 Support
For issues or questions, refer to:
- Jenkins documentation: https://jenkins.io/doc/
- GitHub Actions documentation: https://docs.github.com/en/actions
- Docker documentation: https://docs.docker.com/
