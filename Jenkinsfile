node('master') {
    stage('Checkout') {
        checkout scm
    }
        
    stage('Build') {
        sh "docker build --build-arg SERVER_PORT=${SERVER_PORT} -m 3g -t ${PROJECT_NAME}:B${BUILD_NUMBER} -f Dockerfile ."
    }
    
    stage('Deployment') {
        try {
            sh "docker stop ${PROJECT_NAME}"
            sh "docker rm ${PROJECT_NAME}"
        } catch (Exception e) {
            sh "echo 'Container not running or does not exist'"
        }
        try {
            sh "docker network create redis_network"
        } catch (Exception e) {
            sh "echo 'Network may already exist'"
        }
        
        sh "docker run -d \
            --name ${PROJECT_NAME} \
            --network redis_network \
            -e OPENAI_KEY='${OPENAI_KEY}' \
            -e ANTHROPIC_API_KEY='${ANTHROPIC_API_KEY}' \
            -e REDIS_HOST='${REDIS_HOST}' \
            -p ${SERVER_PORT}:80 \
            ${PROJECT_NAME}:B${BUILD_NUMBER}"
    }
}
