node('master') {
    stage ('Checkout') {
        checkout scm
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
        --network g4pay_redis_network \
        -e WRITE_SCOPE=${WRITE_SCOPE} \
        -e READ_SCOPE=${READ_SCOPE} \
        -e GRANT_TYPE=${GRANT_TYPE} \
        -e OAUTH_TOKEN_URL=${OAUTH_TOKEN_URL} \
        -e CREATE_IMMEDIATE_CHARGE_URL=${CREATE_IMMEDIATE_CHARGE_URL} \
        -e LIST_IMMEDIATE_CHARGE_URL=${LIST_IMMEDIATE_CHARGE_URL} \
        -e FIND_IMMEDIATE_CHARGE_URL=${FIND_IMMEDIATE_CHARGE_URL} \
        -e KEYCLOAK_SERVER_URL=${KEYCLOAK_SERVER_URL} \
        -e KEYCLOAK_CLIENT_ID_PAYMENT=${KEYCLOAK_CLIENT_ID_PAYMENT} \
        -e KEYCLOAK_REALM_NAME=${KEYCLOAK_REALM_NAME} \
        -e KEYCLOAK_CLIENT_SECRET_PAYMENT=${KEYCLOAK_CLIENT_SECRET_PAYMENT} \
        -e MONGO_URI='${MONGO_URI}' \
        -e MONGO_DATABASE=${MONGO_DATABASE} \
        -e SERVER_PORT=${SERVER_PORT} \
        -e CACHE_REDIS_HOST=${CACHE_REDIS_HOST} \
        -e CACHE_REDIS_PORT=${CACHE_REDIS_PORT} \
        -e CACHE_REDIS_DB=${CACHE_REDIS_DB} \
        -e CACHE_DEFAULT_TIMEOUT=${CACHE_DEFAULT_TIMEOUT} \
        -e BANK_SLIP_URL='${BANK_SLIP_URL}' \
        -e REGISTER_WEB_HOOK_URL='${REGISTER_WEB_HOOK_URL}' \
        -e BANK_NAME='${BANK_NAME}' \
        -e OAUTH_USE_AUTH='${OAUTH_USE_AUTH}' \
        -p ${SERVER_PORT}:80 \
        --name ${PROJECT_NAME} ${PROJECT_NAME}:B${BUILD_NUMBER}"
        // Be carreful with white spaces before the '\'
        
    }
}


