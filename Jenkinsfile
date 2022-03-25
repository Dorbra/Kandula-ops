pipeline{
    agent {label 'linux'}
   parameters {
        choice(name: 'deploy', choices: ['enabled', 'disabled'], description: 'deploy docker?' )
        string(defaultValue: '0', description: 'Build Versioning', name: 'VERSION')
    }
    stages{
        stage("Deploy?"){
            when {
                expression { params.deploy == "enabled" }
            }
            stages{
                stage("Git Clone"){
                    steps{
                      echo "GIT CLONE WITH Jenkinsfile
                        git branch: 'master', credentialsId: 'github-jenkins', url: 'https://github.com/Dorbra/kandula-project-app'
                    }
                }
                stage("Docker build&push") {
                    steps{
                        dir(""){
                            script{
                                withDockerRegistry(credentialsId: 'dockerhub-dorbra') {
                                    def image = docker.build("dorbra/kandula-midproject:${VERSION}")
                                    image.push()
                                }
                            }
                        }
                    }
                }
