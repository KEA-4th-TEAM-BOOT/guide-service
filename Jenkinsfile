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

    tools {
        // Python 설정 (도구 이름은 Jenkins 설정에 따라 다를 수 있습니다)
        python 'Python-3.10'
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
                sh 'pip install -r requirements.txt'
                sh 'pytest'  // 테스트 실행, 테스트를 실행하려면 pytest를 설치하고 테스트 스크립트를 준비해야 함
            }
        }

        stage('컨테이너 빌드 및 업로드') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'main') {
                        // DockerHub 로그인
                        withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
                            sh '''
                                echo $PASSWORD | docker login -u $USERNAME --password-stdin
                            '''
                        }

                        // Docker 이미지 빌드 및 푸시
                        sh "docker build -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG} ."
                        sh "docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}"

                        // 로컬 Docker 이미지 삭제
                        sh "docker rmi ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}"
                    } else if (env.BRANCH_NAME == 'prod') {
                        // AWS ECR 로그인
                        withCredentials([string(credentialsId: 'aws-credentials', variable: 'AWS_ACCESS_KEY_ID'), string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')]) {
                            sh '''
                                aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                                aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                                aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                            '''
                        }

                        // AWS ECR에 이미지 빌드 및 푸시
                        sh "docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${TAG} ."
                        sh "docker tag ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest"
                        sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${TAG}"
                        sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest"

                        // 로컬 Docker 이미지 삭제
                        sh "docker rmi ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${TAG}"
                        sh "docker rmi ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest"
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
