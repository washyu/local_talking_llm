pipeline {
    agent any
    
    environment {
        DOCKER_HOST = 'aiserver'
        IMAGE_NAME = 'local-talking-llm'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_HOST}:5000/${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        
        stage('Push Docker Image') {
            steps {
                sh "docker push ${DOCKER_HOST}:5000/${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
        
        stage('Deploy') {
            steps {
                sh """
                docker stop ${IMAGE_NAME} || true
                docker rm ${IMAGE_NAME} || true
                docker run -d --name ${IMAGE_NAME} -p 8000:8000 ${DOCKER_HOST}:5000/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }
}