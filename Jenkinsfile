pipeline {
    agent {
        docker {
            image 'docker:dind'
            args '--privileged'
        }
    }
    
    environment {
        DOCKER_HOST = 'aiserver'
        IMAGE_NAME = 'local-talking-llm'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Start Docker Daemon') {
            steps {
                sh '''
                # Start Docker daemon
                dockerd-entrypoint.sh &
                sleep 10
                
                # Check if Docker is running
                docker info
                '''
            }
        }
        
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        // Rest of your stages remain the same
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_HOST}:5000/${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }
        
        // ... other stages
    }
}