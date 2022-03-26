properties([parameters([choice(choices: ['enabled', 'disabled'], description: 'if to deploy', name: 'DEPLOY'),
  string(defaultValue: 'latest', description: 'build version', name: 'VERSION')
])])

node(label: 'linux') {
  if (DEPLOY.equals('enabled')) {
    stage("Git Clone") {
      git branch: 'master', credentialsId: 'github-jenkins', url: 'https://github.com/Dorbra/kandula-project-app'
    }
    stage("Docker build&push") {
      dir("") {
        script {
          withDockerRegistry(credentialsId: 'dockerhub-dorbra') {
            def image = docker.build("dorbra/kandula-midproject:${VERSION}")
            image.push()
          }
        }
      }
    }
    stage("config Kubernetes cluster") {
        sh 'aws eks update-kubeconfig --region us-east-1 --name dorbra-kandula-prod-23'
    }
    stage("Deploy Kandula on k8s") {
        sh 'chmod +x kandula-script.sh'
        sh './kandula-script.sh'
    }
  }

}
