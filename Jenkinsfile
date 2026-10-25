pipeline {
    agent any
    
    environment {
        AWS_REGION = 'us-east-1' // Change to your AWS region
        AWS_ACCOUNT_ID = '123456789012' // Replace with your AWS Account ID
        IMAGE_NAME = 'plant-care-tracker'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    }

    stages {
        stage('1. Pull Latest Code') {
            steps {
                // Pulls latest code from your GitHub repository
                git branch: 'main', url: 'https://github.com/shrusti-acharya/plant-care-tracker.git'
            }
        }

        stage('2. Build & Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest test_app.py
                '''
            }
        }

        stage('3. Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('4. Push to AWS ECR') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-ecr-credentials', 
                                                  usernameVariable: 'AWS_ACCESS_KEY_ID', 
                                                  passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                        # Log in to your AWS ECR
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        
                        # Tag and push image to your ECR account
                        docker tag ${IMAGE_NAME}:latest ${ECR_REGISTRY}/${IMAGE_NAME}:latest
                        docker push ${ECR_REGISTRY}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('5. Deploy to Minikube') {
            steps {
                sh '''
                    # Ensure Minikube is running
                    minikube status || minikube start
                    
                    # Apply Kubernetes manifests (update image URI in deployment.yaml to match your ECR registry)
                    kubectl apply -f k8s/deployment.yaml
                    kubectl rollout restart deployment/plant-care-tracker-deployment
                '''
            }
        }

        stage('6. Verify Application') {
            steps {
                sh '''
                    kubectl get pods
                    echo "Application URL:"
                    minikube service plant-care-tracker-service --url
                '''
            }
        }
    }
}
