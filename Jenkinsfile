pipeline {
    agent {
        docker {
            image 'docker:dind'
            args '--privileged -v /var/run/docker.sock:/var/run/docker.sock'
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
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_HOST}:5000/${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    sh "docker push ${DOCKER_HOST}:5000/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh """
                    ssh user@${DOCKER_HOST} 'docker stop ${IMAGE_NAME} || true'
                    ssh user@${DOCKER_HOST} 'docker rm ${IMAGE_NAME} || true'
                    ssh user@${DOCKER_HOST} 'docker run -d --name ${IMAGE_NAME} -p 8000:8000 ${DOCKER_HOST}:5000/${IMAGE_NAME}:${IMAGE_TAG}'
                    """
                }
            }
        }
    }
}
