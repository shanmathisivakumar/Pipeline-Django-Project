pipeline {
    agent any

    environment {
        VENV = "venv"
        ALLOWED_HOSTS = "18.117.83.22,localhost,127.0.0.1"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-pat',
                    url: 'https://github.com/shanmathisivakumar/Pipeline-Django-Project.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                dir('flipkart/Flipkart') {
                    sh '''
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Migrate Database') {
            steps {
                dir('flipkart/Flipkart') {
                    sh '''
                    . $VENV/bin/activate
                    python manage.py migrate
                    '''
                }
            }
        }

        stage('Collect Static Files') {
            steps {
                dir('flipkart/Flipkart') {
                    sh '''
                    . $VENV/bin/activate
                    python manage.py collectstatic --noinput
                    '''
                }
            }
        }

        stage('Create Admin User') {
            steps {
                dir('flipkart/Flipkart') {
                    sh '''
                    . $VENV/bin/activate
                    python manage.py shell -c "
from django.contrib.auth.models import User;
User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','sshanmathi2502@gmail.com','Admin@123')
"
                    '''
                }
            }
        }

        stage('Start Django') {
            steps {
                dir('flipkart/Flipkart') {
                    sh '''
                    pkill -f "manage.py runserver" || true
                    . $VENV/bin/activate
                    nohup python manage.py runserver 0.0.0.0:8000 > app.log 2>&1 &
                    '''
                }
            }
        }
    }
}
