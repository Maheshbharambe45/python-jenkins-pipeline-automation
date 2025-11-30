pipeline{

agent any

environment {
    IMG_NAME = 'maheshbharambe45/flask_app'
    PORT_MAPPING = '8081:5000'
    MINIKUBE_IP = '3.110.138.250'
}

stages{

    stage('check_files') {
      steps { sh 'ls -l' }
    }

    stage('Install dependencies'){
        steps {
                sh 'pip install -r requirements.txt'
            }
    }

    stage('Running tests'){
        steps{
            sh 'pytest -q'
        }
    }

    stage('Build Docker Image') {
        steps {
            sh '''
            echo "Building Docker Image ----->"
            docker build -t ${IMG_NAME}:latest .
            '''
        }
    }

    stage('Push Image') {
        steps {
            withCredentials([usernamePassword(
            credentialsId: 'docker-crediantials',
            usernameVariable: 'MY_DOCKER_USER',
            passwordVariable: 'MY_DOCKER_PASS'
            )]) {
            sh '''
                echo "$MY_DOCKER_PASS" | docker login -u "$MY_DOCKER_USER" --password-stdin
                docker push ${IMG_NAME}:latest
            '''
            }
        }
    }


    stage("Deploy to Minikube on EC2") {
        steps {
            withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY')]) {

            // Upload both YAML files
            sh """
                scp -i "$SSH_KEY" -o StrictHostKeyChecking=no deployment.yml service.yml \
                ubuntu@${MINIKUBE_IP}:/home/ubuntu/
            """

            // Apply deployment & service on EC2’s Minikube
            sh """
                ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no ubuntu@${MINIKUBE_IP} '
                kubectl delete -f deployment.yml --ignore-not-found=true
                kubectl delete -f service.yml --ignore-not-found=true

                kubectl apply -f deployment.yml
                kubectl apply -f service.yml

                kubectl get pods -o wide
                '
            """
            }
        }
        }
        

}
}