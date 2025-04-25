pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = "bookstore.settings"
        PATH = "/usr/local/bin:$PATH"
    }

    stages {
        stage('Clone Repo') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Test') {
            steps {
                sh 'docker-compose run --rm web python manage.py test'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        failure {
            echo '❌ Pipeline failed. Check test or deployment stage.'
        }
        success {
            echo '✅ Pipeline succeeded.'
        }
    }
}