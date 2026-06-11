pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/shanmathisivakumar/Pipeline-Django-Project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Migration') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py migrate
                '''
            }
        }

        stage('Collect Static') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Run Django') {
            steps {
                sh '''
                . venv/bin/activate
                nohup python manage.py runserver 0.0.0.0:8000 &
                '''
            }
        }
    }
}
