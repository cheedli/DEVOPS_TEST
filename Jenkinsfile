def branchName
def targetBranch

pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "taharejeb97"
        DEV_TAG = "${DOCKERHUB_USERNAME}/themenufy-ai:v1.0.0-dev"
        STAGING_TAG = "${DOCKERHUB_USERNAME}/themenufy-ai:v1.0.0-staging"
        PROD_TAG = "${DOCKERHUB_USERNAME}/themenufy-ai:v1.0.0-prod"
    }
    
    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Git branch name')
        string(name: 'CHANGE_ID', defaultValue: '', description: 'Git change ID for merge requests')
        string(name: 'CHANGE_TARGET', defaultValue: '', description: 'Git change ID for the target merge requests')
    }
    
    stages {
        stage('Initialize Branch') {
            steps {
                script {
                    branchName = params.BRANCH_NAME
                    targetBranch = branchName // Adjust if different target branch needed
                    echo "Current branch name: ${branchName}"
                    echo "Target branch name: ${targetBranch}"
                }
            }
        }

        stage('Git Checkout') {
            steps {
                git branch: branchName, credentialsId: 'github', url: 'https://github.com/cheedli/DEVOPS_TEST.git'
            }
        }
    }
}
