pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t faceweb:latest .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker rm -f faceweb_app || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh 'docker run -d --name faceweb_app -p 5000:5000 faceweb:latest'
            }
        }

        stage('Check App') {
            steps {
                sh 'curl http://localhost:5000/'
            }
        }
    }
}
