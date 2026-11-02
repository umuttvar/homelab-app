pipeline{
environment {
  IMAGE= "ghcr.io/umuttvar/homelab-app"
}
    agent {
      kubernetes {
        yaml '''
        apiVersion: v1
        kind: Pod
        spec:
          containers:
            - name: kaniko
              image: gcr.io/kaniko-project/executor:v1.24.0-debug
              command: ["/busybox/cat"]
              tty: true
        '''
      }
    }
    stages{
        stage("SELAMLAR"){
            steps{
              sh  '''
                echo "${GIT_COMMIT} numaralı build"
                ls -la
                hostname
              '''          
            }
          }

        stage("Build") {
          steps {
            container ('kaniko') {
               withCredentials([usernameColonPassword(credentialsId: 'ghcr', variable: 'USERPASS')]) {
                sh '''
                  set +x 
                  TAG=$(echo "$GIT_COMMIT" | cut -c1-7)
                  AUTH=$(printf '%s' "$USERPASS" | base64)
                  mkdir -p /kaniko/.docker
                  printf '{"auths":{"ghcr.io":{"auth":"%s"}}}' "$AUTH" > /kaniko/.docker/config.json
                  /kaniko/executor \
                --context="$WORKSPACE" \
                --dockerfile="$WORKSPACE/Dockerfile" \
                --build-arg APP_VERSION="$TAG" \
                --destination="$IMAGE:$TAG" 
            '''
            }
            }
          }
        }  
  }  
}   



  