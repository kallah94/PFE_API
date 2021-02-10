node('diaf-moussa-api-node') {
    checkout scm 
    
    stage('pull github changes') {
        dir('/home/fmoussa/PFE_API') {
            sh "git pull origin master"
        }
    }
    
    stage('build') {
        dir('/home/fmoussa/PFE_API') {
            sh "python -m pip install -r requirements.txt"
        }
    }
    
    stage('deploy') {
        sh "sudo systemctl restart api"
        sh "sudo systemctl status api"
    }
}
