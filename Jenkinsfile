pipeline{
    agent any
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

          stage("Credentials Testi") {
              steps{
                withCredentials([usernamePassword(credentialsId: 'github-homelab',
                usernameVariable: 'GH_USER',
                passwordVariable: 'GH_TOKEN')]) {
                  sh '''
                    curl -s -H "Authorization: Bearer $GH_TOKEN" \
                      https://api.github.com/repos/umuttvar/homelab | grep "push"
                  '''
                }
              }
          }
          stage ("ghcr Testi") {
              steps{
                withCredentials([usernamePassword(credentialsId: 'ghcr',
                usernameVariable: 'GH_USER',
                passwordVariable: 'GH_TOKEN')]) {
                  sh '''
                    curl -s -H "Authorization: Bearer $GH_TOKEN" \
                      https://api.github.com/user | grep "login"
                  '''
                }
              }
            }
  }   
}