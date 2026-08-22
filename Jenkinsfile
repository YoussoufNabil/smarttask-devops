pipeline {
  agent any

  environment {
    REGISTRY = 'docker.io'
    IMAGE_TAG = "${BUILD_NUMBER}"
    DOCKERHUB_NAMESPACE = 'YoussoufNabil'
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
    stage('Push') {
      steps {
        script {
          docker.withRegistry('', 'docker-hub-credentials') {
            sh 'docker push $DOCKERHUB_NAMESPACE/smarttask-frontend:$IMAGE_TAG'
            sh 'docker push $DOCKERHUB_NAMESPACE/smarttask-frontend:latest'
            sh 'docker push $DOCKERHUB_NAMESPACE/smarttask-backend:$IMAGE_TAG'
            sh 'docker push $DOCKERHUB_NAMESPACE/smarttask-backend:latest'
          }
        }
      }
    }
  }
}
