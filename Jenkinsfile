pipeline {
  agent { label 'docker' }

  environment {
    REGISTRY = 'docker.io'
    IMAGE_TAG = "${BUILD_NUMBER}"
    // Remplacer par l'identifiant Docker Hub utilisé dans Jenkins.
    DOCKERHUB_NAMESPACE = 'CHANGE_ME'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      steps {
        sh 'docker build -t $DOCKERHUB_NAMESPACE/smarttask-frontend:$IMAGE_TAG ./frontend'
        sh 'docker build -t $DOCKERHUB_NAMESPACE/smarttask-backend:$IMAGE_TAG ./backend'
      }
    }
    stage('Tag') {
      steps {
        sh 'docker tag $DOCKERHUB_NAMESPACE/smarttask-frontend:$IMAGE_TAG $DOCKERHUB_NAMESPACE/smarttask-frontend:latest'
        sh 'docker tag $DOCKERHUB_NAMESPACE/smarttask-backend:$IMAGE_TAG $DOCKERHUB_NAMESPACE/smarttask-backend:latest'
      }
    }
    stage('Login Registry') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
        }
      }
    }
    stage('Push') {
      steps {
        sh 'docker push $DOCKERHUB_NAMESPACE/smarttask-frontend:$IMAGE_TAG'
        sh 'docker push $DOCKERHUB_NAMESPACE/smarttask-frontend:latest'
        sh 'docker push $DOCKERHUB_NAMESPACE/smarttask-backend:$IMAGE_TAG'
        sh 'docker push $DOCKERHUB_NAMESPACE/smarttask-backend:latest'
      }
    }
  }
  post {
    always { sh 'docker logout || true' }
  }
}
