#!/bin/bash

# Jenkins Setup Script for messaging_app CI/CD

echo "Setting up Jenkins in Docker container..."

# Pull and run Jenkins container
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts

echo "Jenkins is starting up..."
echo "Please wait 30-60 seconds for Jenkins to initialize..."

# Wait for Jenkins to be ready
sleep 60

# Get initial admin password
echo "Initial Admin Password:"
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

echo ""
echo "Jenkins is now running at: http://localhost:8080"
echo "Use the above password to unlock Jenkins"
echo ""
echo "Next steps:"
echo "1. Install suggested plugins"
echo "2. Create admin user"
echo "3. Install additional plugins: Git, Pipeline, ShiningPanda"
echo "4. Configure GitHub credentials"
echo "5. Create new pipeline job using Jenkinsfile"

# Create a simple test script
cat > test_pipeline.sh << 'EOF'
#!/bin/bash
echo "Testing messaging_app..."
cd messaging_app
python -m pytest chats/tests.py -v
EOF

chmod +x test_pipeline.sh

echo "Test script created: test_pipeline.sh"
