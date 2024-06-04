pipeline {
    agent any

    environment {
        // 환경 변수 설정
        DOCKERHUB_USERNAME = 'codrin2'
        GITHUB_URL = 'https://github.com/KEA-4th-TEAM-BOOT/guide-service.git'
        APP_VERSION = '1.1.1'
        BUILD_DATE = sh(script: "echo `date +%y%m%d.%H%M`", returnStdout: true).trim()
        TAG = "${APP_VERSION}"
        IMAGE_NAME = 'voda-guide'
        SERVICE_NAME = 'guide'
        ECR_REPOSITORY = 'voda-guide'  // AWS ECR 리포지토리 이름
        AWS_REGION = 'ap-northeast-2'  // AWS 리전
        AWS_ACCOUNT_ID = '981883772993'  // AWS 계정 ID
    }

    stages {
        stage('소스파일 체크아웃') {
            steps {
                script {
                    env.BRANCH_NAME = env.BRANCH_NAME ?: 'main'
                    checkout([$class: 'GitSCM', branches: [[name: "*/${env.BRANCH_NAME}"]], userRemoteConfigs: [[url: GITHUB_URL, credentialsId: 'github-signin']]])
                }
            }
        }

        stage('의존성 설치 및 테스트') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-credentials') {
                        def customImage = docker.build("${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}")
                        customImage.run()
                    }
                    sh 'pytest'
                }
            }
        }

        stage('컨테이너 빌드 및 업로드') {
    steps {
        script {
            if (env.BRANCH_NAME == 'main') {
                docker.withRegistry('', 'dockerhub-credentials') {
                    def customImage = docker.build("${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}")
                    customImage.push()
                }
            } else if (env.BRANCH_NAME == 'prod') {
                withAWS(credentials: 'aws-credentials', region: AWS_REGION) {
                    sh """#!/bin/bash
                        aws ecr get-login --no-include-email | sed 's|^docker login -u AWS -p \\(.*\\)https://|docker login -u AWS -p \\1 |'
                    """

                    def customImage = docker.build("${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${TAG}")
                    customImage.push("${TAG}")
                    customImage.push("latest")
                }
            }
        }
    }
}

    }

    post {
        always {
            // 로그아웃 및 자격 증명 정보 정리
            sh 'docker logout'
            sh 'unset AWS_ACCESS_KEY_ID'
            sh 'unset AWS_SECRET_ACCESS_KEY'
        }
    }
}
