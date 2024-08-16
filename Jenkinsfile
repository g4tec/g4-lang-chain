node('master') {
    stage ('Checkout') {
        checkout scm
    }
    stage('Setup Network') {
            steps {
                script {
                    sh 'docker network ls | grep redis_network || docker network create redis_network'
                }
            }
        }
        
    stage ('Build') {
        sh "docker build --build-arg SERVER_PORT=${SERVER_PORT} -m 3g -t ${PROJECT_NAME}:B${BUILD_NUMBER} -f Dockerfile ."
    }
    stage ('Deployment') {
        try {
            sh "docker service rm ${PROJECT_NAME}"
        } catch (Exception e) {
            sh "echo 'container not running'"
        }
        sh "docker service create --replicas ${REPLICAS} \
        --network redis_network \
        -e OPENAI_KEY='${OPENAI_KEY}' \
        -e ANTHROPIC_API_KEY='${ANTHROPIC_API_KEY}' \
        -e REDIS_HOST='${REDIS_HOST}' \
        -p ${SERVER_PORT}:80 \
        --name ${PROJECT_NAME} ${PROJECT_NAME}:B${BUILD_NUMBER}"
        // Be carreful with white spaces before the '\'
        
    }
}


