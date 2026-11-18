// Pipeline declarativo: pruebas en un contenedor efímero, imagen y prueba de humo.
pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    environment {
        IMAGEN = "inventario:${env.BUILD_NUMBER}"
        CONTENEDOR = "inventario-humo-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Pruebas unitarias') {
            // Contenedor efímero: Jenkins lo crea solo para esta etapa y lo elimina al terminar
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                }
            }
            steps {
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    pip install --no-cache-dir -q -r requirements-dev.txt
                    pytest -v --junitxml=reporte-pruebas.xml
                '''
            }
            post {
                always {
                    junit 'reporte-pruebas.xml'
                }
            }
        }

        stage('Construir imagen') {
            steps {
                sh 'docker build -t $IMAGEN .'
            }
        }

        stage('Prueba de humo') {
            steps {
                sh '''
                    docker run -d --name $CONTENEDOR $IMAGEN
                    sleep 3
                    docker exec $CONTENEDOR python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/salud').read().decode())"
                '''
            }
            post {
                always {
                    sh 'docker rm -f $CONTENEDOR || true'
                }
            }
        }
    }
}
