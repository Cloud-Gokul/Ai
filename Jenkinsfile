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
                bat 'docker build -t faceweb:latest .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat 'docker rm -f faceweb_app || exit 0'
            }
        }

        stage('Run New Container') {
            steps {
                bat 'docker run -d --name faceweb_app -p 5000:5000 faceweb:latest'
            }
        }

        stage('Check App') {
            steps {
                bat 'curl http://localhost:5000/'
            }
        }
    }
}
