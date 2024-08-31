## benchmark_x86_025vcpu_05g

aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmark_x86_025vcpu_05g \
    --force-new-deployment

aws ecs describe-services --cluster rules-dev-fargate-cluster \
    --services benchmark_x86_025vcpu_05g

aws ssm start-session \
--target ecs:rules-dev-fargate-cluster_75dce46970a443b59126f02673435c03_75dce46970a443b59126f02673435c03-4001447092


## benchmarkx86_05vcpu_1g

aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmarkx86_05vcpu_1g \
    --force-new-deployment

aws ssm start-session \
--target ecs:rules-dev-fargate-cluster_75dce46970a443b59126f02673435c03_75dce46970a443b59126f02673435c03-4001447092


## benchmarkx86_1vcpu_2g

aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmarkx86_1vcpu_2g \
    --force-new-deployment


## benchmark_x86_2vcpu_4g
aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmark_x86_2vcpu_4g \
    --force-new-deployment


aws ssm start-session \
--target ecs:rules-dev-fargate-cluster_970b8d84c5ef486888ba001181848c8c_970b8d84c5ef486888ba001181848c8c-3752462716


## benchmark_x86_4vcpu_8g

aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmark_x86_4vcpu_8g \
    --force-new-deployment

aws ssm start-session \
--target ecs:rules-dev-fargate-cluster_7f0657d1853b43cf99acef77fefacfa3_7f0657d1853b43cf99acef77fefacfa3-1200670878




## benchmark_arm_025vcpu_05g
aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmark_arm_025vcpu_05g \
    --force-new-deployment


## benchmark_arm_05vcpu_1g
aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmark_arm_05vcpu_1g \
    --force-new-deployment


## benchmark_arm_1vcpu_2g
aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmark_arm_1vcpu_2g \
    --force-new-deployment


## benchmark_arm_2vcpu_4g
aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmark_arm_2vcpu_4g \
    --force-new-deployment
## benchmark_arm_4vcpu_8g
aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmark_arm_4vcpu_8g \
    --force-new-deployment



aws ssm start-session \
--target ecs:rules-dev-fargate-cluster_3171e0d550524bd783f595d23db904de_3171e0d550524bd783f595d23db904de-2614634824

aws ssm start-session \
--target ecs:rules-dev-fargate-cluster_29f958a139284a4c92eca2e50d235657_29f958a139284a4c92eca2e50d235657-2847488270




aws ecs update-service --cluster rules-dev-fargate-cluster \
    --enable-execute-command --service benchmark_x86_4vcpu_8g \
    --force-new-deployment

aws ssm start-session \
--target ecs:rules-dev-fargate-cluster_d3eebd6beb754430af8706fa334c821e_d3eebd6beb754430af8706fa334c821e-590012265
