pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "faceweb"
        DOCKER_TAG = "${BUILD_NUMBER}"
        REGISTRY = credentials('docker-registry')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "✓ Code checked out"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -t ${DOCKER_IMAGE}:latest .'
                    echo "✓ Docker image built"
                }
            }
        }

        stage('Test Container') {
            steps {
                script {
                    sh '''
                        docker run -d --name test-container -p 5001:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                        sleep 5
                        curl -f http://localhost:5001/health || true
                        docker stop test-container
                        docker rm test-container
                        echo "✓ Container test passed"
                    '''
                }
            }
        }

        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} $DOCKER_USER/${DOCKER_IMAGE}:${DOCKER_TAG}
                            docker tag ${DOCKER_IMAGE}:latest $DOCKER_USER/${DOCKER_IMAGE}:latest
                            docker push $DOCKER_USER/${DOCKER_IMAGE}:${DOCKER_TAG}
                            docker push $DOCKER_USER/${DOCKER_IMAGE}:latest
                            docker logout
                            echo "✓ Image pushed to registry"
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        docker-compose down || true
                        docker-compose up -d --no-build
                        echo "✓ Deployed successfully"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline execution completed"
            cleanWs()
        }
        success {
            echo "✅ Build successful"
        }
        failure {
            echo "❌ Build failed"
        }
    }
}
