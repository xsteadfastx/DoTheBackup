#!groovy
node {
    docker.image('xsteadfastx/tox-python:latest').inside {
        stage('checkout') {
            git url: 'https://github.com/xsteadfastx/DoTheBackup.git'
        }
        stage('prepate container') {
            sh 'sudo apt-get update'
            sh 'sudo apt-get install -y rsync'
        }
        stage('test') {
            sh 'tox -r'
        }
    }
}
