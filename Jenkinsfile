pipeline {
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

    environment {
        IMAGE = 'ghcr.io/umuttvar/homelab-app'
    }

    triggers {
        pollSCM('H/3 * * * *')
    }

    stages {
        stage('Build & Push') {
            steps {
                container('kaniko') {
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

        stage('Update GitOps') {
            steps {
                container('jnlp') {
                    withCredentials([usernamePassword(credentialsId: 'github-homelab',
                                                      usernameVariable: 'GH_USER',
                                                      passwordVariable: 'GH_TOKEN')]) {
                        sh '''
                            set +x
                            TAG=$(echo "$GIT_COMMIT" | cut -c1-7)

                            rm -rf homelab
                            git clone https://$GH_USER:$GH_TOKEN@github.com/umuttvar/homelab.git
                            cd homelab

                            sed -i "s/^  tag: .*/  tag: '$TAG'/" gitops/charts/homelab-app/values.yaml

                            git config user.name "jenkins"
                            git config user.email "jenkins@homelab.local"
                            git diff --quiet || git commit -am "build(homelab-app): deploy $TAG"
                            git push origin HEAD:main
                        '''
                    }
                }
            }
        }
    }
}