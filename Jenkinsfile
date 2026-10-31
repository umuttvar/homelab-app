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
    }
   
}