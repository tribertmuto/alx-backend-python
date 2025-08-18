# Create a Docker volume for persistent storage
docker volume create jenkins_home

# Run Jenkins LTS container with persistent storage and port mapping
docker run -d \
  --name jenkins-lts \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --restart=unless-stopped \
  jenkins/jenkins:lts

# Alternative: Using bind mount instead of named volume
docker run -d \
  --name jenkins-lts \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /path/to/jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --restart=unless-stopped \
  jenkins/jenkins:lts

# Get initial admin password after container starts
docker exec jenkins-lts cat /var/jenkins_home/secrets/initialAdminPassword

# View container logs
docker logs jenkins-lts

# Stop the container
docker stop jenkins-lts

# Start the container
docker start jenkins-lts

# Remove the container (data persists in volume)
docker rm jenkins-lts