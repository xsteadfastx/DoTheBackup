#!groovy
node {
    docker.image('xsteadfastx/tox-python:latest').inside {
        stage('checkout') {
            git url: 'https://github.com/xsteadfastx/DoTheBackup.git'
        }
        stage('test') {
            sh 'tox -r'
        }
    }
}
