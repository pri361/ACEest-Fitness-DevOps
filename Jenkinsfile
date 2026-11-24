
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        SONARQUBE_SERVER = 'SonarQube'
        SONAR_SCANNER_TOOL = 'SonarScanner'
        SONAR_PROJECT_KEY = 'aceest-fitness'

        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        DOCKER_IMAGE_NAME = 'aceest-fitness'

        K8S_DEPLOYMENT = 'aceest-fitness'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Automated Testing') {
            steps {
                sh '''
                    docker run --rm \
                      ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} \
                      python -m pytest -v
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool(
                        name: "${SONAR_SCANNER_TOOL}",
                        type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    )

                    withSonarQubeEnv("${SONARQUBE_SERVER}") {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY}
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    script {
                        def qg = waitForQualityGate()

                        if (qg.status != 'OK') {
                            error "SonarQube Quality Gate failed: ${qg.status}"
                        }

                        echo 'SonarQube Quality Gate Passed'
                    }
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKERHUB_CREDENTIALS}",
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_PASSWORD'
                    )
                ]) {
                    sh '''
                        set +x

                        echo "$DOCKERHUB_PASSWORD" | docker login \
                          --username "$DOCKERHUB_USERNAME" \
                          --password-stdin

                        docker tag \
                          ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} \
                          "$DOCKERHUB_USERNAME/${DOCKER_IMAGE_NAME}:${BUILD_NUMBER}"

                        docker push \
                          "$DOCKERHUB_USERNAME/${DOCKER_IMAGE_NAME}:${BUILD_NUMBER}"

                        docker tag \
                          ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} \
                          "$DOCKERHUB_USERNAME/${DOCKER_IMAGE_NAME}:latest"

                        docker push \
                          "$DOCKERHUB_USERNAME/${DOCKER_IMAGE_NAME}:latest"

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKERHUB_CREDENTIALS}",
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_PASSWORD'
                    )
                ]) {
                    sh '''
                        set -e

                        sed "s|DOCKERHUB_USERNAME|${DOCKERHUB_USERNAME}|g; s|IMAGE_TAG|${BUILD_NUMBER}|g" \
                          k8s/deployment.yaml | kubectl apply -f -

                        kubectl apply -f k8s/service.yaml

                        if ! kubectl rollout status \
                          deployment/${K8S_DEPLOYMENT} --timeout=180s; then

                            echo "Deployment failed. Attempting rollback."

                            kubectl rollout undo \
                              deployment/${K8S_DEPLOYMENT} || true

                            kubectl rollout status \
                              deployment/${K8S_DEPLOYMENT} --timeout=180s || true

                            exit 1
                        fi

                        kubectl get deployments
                        kubectl get pods -o wide
                        kubectl get services
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'ACEest Fitness pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Please check the stage logs.'
        }
    }
}
