pipeline {
  agent {
    label 'linux'
  }
  parameters {
    choice(name: 'deploy', choices: ['enabled', 'disabled'], description: 'deploy docker?')
  }
    
  stages {
    stage("Deploy?") {
      when {
        expression {
          params.deploy == "enabled"
        }
      }
      stages {
        sh 'sudo ./kandula-script.sh'
      }
  }
}
}
