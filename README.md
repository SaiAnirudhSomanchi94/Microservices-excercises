# Git Link: https://github.com/SaiAnirudhSomanchi94/Microservices-excercises

# Coworking Space Service Extension
The Coworking Space Service is a set of APIs that enables users to request one-time tokens and administrators to authorize access to a coworking space. This service follows a microservice pattern and the APIs are split into distinct services that can be deployed and managed independently of one another.

For this project, you are a DevOps engineer who will be collaborating with a team that is building an API for business analysts. The API provides business analysts basic analytics data on user activity in the service. The application they provide you functions as expected locally and you are expected to help build a pipeline to deploy it in Kubernetes.

## Getting Started

### Dependencies
#### Local Environment
1. Python Environment - run Python 3.6+ applications and install Python dependencies via `pip`
2. Docker CLI - build and run Docker images locally
3. `kubectl` - run commands against a Kubernetes cluster
4. `helm` - apply Helm Charts to a Kubernetes cluster

#### Remote Resources
1. AWS CodeBuild - build Docker images remotely
2. AWS ECR - host Docker images
3. Kubernetes Environment with AWS EKS - run applications in k8s
4. AWS CloudWatch - monitor activity and logs in EKS
5. GitHub - pull and clone code

### Default Arguments

* `DB_USERNAME`
* `DB_PASSWORD`
* `DB_HOST` (defaults to `127.0.0.1`)
* `DB_PORT` (defaults to `5432`)
* `DB_NAME` (defaults to `mydatabase`)

### Process
#### 1. Version Details
kubectl Version
```bash
workspace root$ kubectl version
Client Version: version.Info{Major:"1", Minor:"20", GitVersion:"v1.20.2", GitCommit:"faecb196815e248d3ecfb03c680a4507229c2a56", GitTreeState:"clean", BuildDate:"2021-01-13T13:28:09Z", GoVersion:"go1.15.5", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"24+", GitVersion:"v1.24.17-eks-2d5f260", GitCommit:"89754d01890de9a2e8316f075ec0a47cccc74b13", GitTreeState:"clean", BuildDate:"2024-12-12T21:00:12Z", GoVersion:"go1.21.8", Compiler:"gc", Platform:"linux/amd64"}
```
##### AWS Version
```bash
workspace root$ aws --version
aws-cli/2.15.25 Python/3.11.8 Linux/5.15.0-1065-gke exe/x86_64.ubuntu.18 prompt/off
```

#### 2. Region : us-east-1

#### 3. ommand Used to create EKS and updating Config file:
```bash
eksctl create cluster --name my-cluster --region us-east-1 --nodegroup-name my-nodes --node-type t3.small --nodes 1 --nodes-min 1 --nodes-max 2
aws eks --region us-east-1 update-kubeconfig --name my-cluster
```


#### 4. Command Used to create ECR:
```bash
aws ecr create-repository --repository-name coworking --region us-east-1
```

#### 5. Updating the YAML Files (Deployment Folder)
1. pvc.yaml
2. pv.yaml
3. postgresql-deployment.yaml
4. postgresql-service.yaml
5. secret.yaml
6. configmap.yaml
7. deployment.yaml
8. buildspec.yaml (is available for reference used in Github)

#### 6. Applying the Yaml Files using below command
```bash
kubectl apply -f deployment/<.yaml>
```

#### 7. Command to Forward traffic locally to Postgresql
```bash
kubectl port-forward service/postgresql-service 5433:5432 &
```

#### 8. Setting Up light weight Postgresql and inserting data to it (.sql files are available in db folder)
```bash
apt update
apt install postgresql postgresql-contrib
export DB_PASSWORD=mypassword
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U myuser -d mydatabase -p 5433 < db/<.sql files>
kubectl port-forward svc/postgresql-service 5433:5432 &
```

#### 9. To Run the application the below setup commands are executed

```bash
# Update the local package index with the latest packages from the repositories
apt update

# Install a couple of packages to successfully install postgresql server locally
apt install build-essential libpq-dev

# Update python modules to successfully build the required modules
pip install --upgrade pip setuptools wheel

# Installing Requirements
pip install -r analytics/requirements.txt

# Exporting the environment variables
export DB_USERNAME=myuser
export DB_PASSWORD=${POSTGRES_PASSWORD}
export DB_HOST=127.0.0.1
export DB_PORT=5433
export DB_NAME=mydatabase

# Set up port forwarding
kubectl port-forward --namespace default svc/postgresql-service 5433:5432 &

#Setting up Secret using Kubectl
kubectl create secret generic postgresql-service --from-literal=postgres-password=mypassword


# Export the password. Replace 
export POSTGRES_PASSWORD=$(kubectl get secret --namespace default postgresql-service -o jsonpath="{.data.postgres-password}" | base64 -d)

# Running application
python analytics/app.py
```

#### 10. Commands To Test the connectivity locally
```bash
curl http://127.0.0.1:5153/api/reports/daily_usage
curl http://127.0.0.1:5153/api/reports/user_visits
```

#### 11. Dockerising 

```bash
# Updating Packages

apt update
apt install docker-ce docker-ce-cli containerd.io

# Build Docker Image

docker build -t test-coworking-analytics .

# Run it locally (Make sure the port-forwarding is done on postresql service and the app.py which is executed before is closed)
docker run --network="host" test-coworking-analytics

```

#### 12. Gitlab link is done on CodeBuild 
#### 13. Buildspec.yaml is available in the code
#### 14. ConfigMap is configured with default arguments 
#### 15. Deployment.yaml is configured and fetch the secret from secrets configured by secret.yaml
#### 16. Testing is completed using the curl commands
#### Output:
```bash
workspace root$ curl a7e4ce245faf84fe483cf9139fb4913b-482396259.us-east-1.elb.amazonaws.com:5153/api/reports/daily_usage
{"2023-02-07":40,"2023-02-08":202,"2023-02-09":179,"2023-02-10":158,"2023-02-11":146,"2023-02-12":176,"2023-02-13":196,"2023-02-14":142}
workspace root$ curl a7e4ce245faf84fe483cf9139fb4913b-482396259.us-east-1.elb.amazonaws.com:5153/api/reports/user_visits
{"1":{"joined_at":"2023-01-20 03:23:39.757813","visits":6},"2":{"joined_at":"2023-02-02 16:23:39.757830","visits":5},"3":{"joined_at":"2023-01-31 10:23:39.757836","visits":5},"4":{"joined_at":"2023-02-13 05:23:39.757840","visits":2},"5":{"joined_at":"2023-02-11 22:23:39.757844","visits":7},"6":{"joined_at":"2023-02-07 18:23:39.757848","visits":3},"7":{"joined_at":"2022-12-26 05:23:39.757852","visits":5},"8":{"joined_at":"2023-01-10 15:23:39.757855","visits":7},"9":{"joined_at":"2023-01-18 17:23:39.757859","visits":2},"10":{"joined_at":"2023-01-16 04:23:39.757862","visits":4},"11":{"joined_at":"2023-01-02 03:23:39.757866","visits":3},"12":{"joined_at":"2023-02-05 17:23:39.757869","visits":5},"13":{"joined_at":"2023-01-29 18:23:39.757873","visits":6},"14":{"joined_at":"2022-12-16 01:23:39.757876","visits":4},"15":{"joined_at":"2023-01-24 16:23:39.757880","visits":4},"16":{"joined_at":"2023-02-12 23:23:39.757883","visits":11},"17":{"joined_at":"2023-01-02 11:23:39.757886","visits":9},"18":{"joined_at":"2023-01-15 06:23:39.757890","visits":3},"19":{"joined_at":"2022-12-20 12:23:39.757893","visits":4},"20":{"joined_at":"2023-02-12 05:23:39.757897","visits":5},"21":{"joined_at":"2023-01-14 22:23:39.757900","visits":4},"22":{"joined_at":"2023-01-11 07:23:39.757903","visits":8},"23":{"joined_at":"2023-01-05 10:23:39.757907","visits":4},"24":{"joined_at":"2023-01-07 00:23:39.757911","visits":2},"25":{"joined_at":"2023-01-11 07:23:39.757914","visits":7},"26":{"joined_at":"2022-12-26 05:23:39.757918","visits":8},"27":{"joined_at":"2022-12-22 15:23:39.757921","visits":5},"28":{"joined_at":"2023-01-12 19:23:39.757925","visits":2},"29":{"joined_at":"2022-12-19 05:23:39.757928","visits":7},"30":{"joined_at":"2022-12-16 09:23:39.757931","visits":4},"31":{"joined_at":"2023-02-09 03:23:39.757935","visits":8},"32":{"joined_at":"2023-02-12 12:23:39.757938","visits":3},"33":{"joined_at":"2023-01-26 04:23:39.757941","visits":3},"34":{"joined_at":"2022-12-16 16:23:39.757945","visits":7},"35":{"joined_at":"2023-01-24 00:23:39.757949","visits":6},"36":{"joined_at":"2023-01-02 03:23:39.757952","visits":7},"37":{"joined_at":"2023-02-08 01:23:39.757955","visits":3},"38":{"joined_at":"2023-01-05 20:23:39.757958","visits":9},"39":{"joined_at":"2023-02-08 15:23:39.757962","visits":2},"40":{"joined_at":"2023-01-25 22:23:39.757965","visits":7},"41":{"joined_at":"2023-01-22 03:23:39.757968","visits":3},"42":{"joined_at":"2023-02-11 22:23:39.757972","visits":3},"43":{"joined_at":"2023-01-19 02:23:39.757975","visits":4},"44":{"joined_at":"2023-01-21 09:23:39.757979","visits":5},"45":{"joined_at":"2023-02-03 19:23:39.757982","visits":6},"46":{"joined_at":"2022-12-22 13:23:39.757985","visits":2},"47":{"joined_at":"2023-01-20 18:23:39.757989","visits":9},"48":{"joined_at":"2023-01-20 21:23:39.757992","visits":6},"49":{"joined_at":"2022-12-15 12:23:39.757995","visits":4},"50":{"joined_at":"2023-01-16 22:23:39.757999","visits":7},"51":{"joined_at":"2023-02-10 16:23:39.758002","visits":5},"52":{"joined_at":"2023-01-11 21:23:39.758005","visits":8},"53":{"joined_at":"2023-02-06 22:23:39.758008","visits":6},"54":{"joined_at":"2022-12-25 16:23:39.758012","visits":8},"55":{"joined_at":"2023-01-29 00:23:39.758015","visits":8},"56":{"joined_at":"2022-12-17 06:23:39.758018","visits":8},"57":{"joined_at":"2022-12-28 10:23:39.758024","visits":7},"58":{"joined_at":"2023-01-16 22:23:39.758027","visits":6},"59":{"joined_at":"2022-12-28 03:23:39.758031","visits":5},"60":{"joined_at":"2023-01-12 14:23:39.758034","visits":9},"61":{"joined_at":"2023-01-04 19:23:39.758037","visits":4},"62":{"joined_at":"2022-12-30 13:23:39.758040","visits":2},"63":{"joined_at":"2023-01-13 19:23:39.758044","visits":5},"64":{"joined_at":"2023-01-21 20:23:39.758047","visits":6},"65":{"joined_at":"2022-12-27 12:23:39.758051","visits":5},"66":{"joined_at":"2023-01-20 07:23:39.758054","visits":7},"67":{"joined_at":"2023-01-19 08:23:39.758058","visits":8},"68":{"joined_at":"2023-02-07 15:23:39.758061","visits":5},"69":{"joined_at":"2022-12-16 19:23:39.758064","visits":3},"70":{"joined_at":"2023-01-14 00:23:39.758067","visits":4},"71":{"joined_at":"2022-12-21 07:23:39.758071","visits":6},"72":{"joined_at":"2023-01-13 16:23:39.758074","visits":1},"74":{"joined_at":"2023-01-14 21:23:39.758081","visits":9},"75":{"joined_at":"2023-02-10 13:23:39.758084","visits":9},"76":{"joined_at":"2022-12-24 08:23:39.758087","visits":4},"77":{"joined_at":"2023-01-12 01:23:39.758091","visits":5},"78":{"joined_at":"2023-01-26 19:23:39.758094","visits":6},"79":{"joined_at":"2022-12-31 12:23:39.758098","visits":1},"80":{"joined_at":"2023-01-15 21:23:39.758101","visits":5},"81":{"joined_at":"2023-01-24 19:23:39.758104","visits":5},"82":{"joined_at":"2023-01-03 12:23:39.758107","visits":3},"83":{"joined_at":"2022-12-23 03:23:39.758111","visits":2},"84":{"joined_at":"2023-02-06 17:23:39.758114","visits":3},"85":{"joined_at":"2023-01-09 23:23:39.758117","visits":2},"86":{"joined_at":"2023-01-21 17:23:39.758121","visits":6},"87":{"joined_at":"2023-01-27 08:23:39.758124","visits":8},"88":{"joined_at":"2023-01-28 15:23:39.758128","visits":4},"89":{"joined_at":"2023-02-13 18:23:39.758131","visits":5},"90":{"joined_at":"2023-01-11 02:23:39.758134","visits":2},"91":{"joined_at":"2023-01-28 23:23:39.758138","visits":6},"92":{"joined_at":"2023-01-22 23:23:39.758141","visits":5},"93":{"joined_at":"2022-12-24 19:23:39.758144","visits":2},"94":{"joined_at":"2023-01-01 23:23:39.758148","visits":5},"95":{"joined_at":"2022-12-26 02:23:39.758151","visits":5},"96":{"joined_at":"2022-12-14 17:23:39.758154","visits":4},"97":{"joined_at":"2023-01-24 10:23:39.758158","visits":4},"98":{"joined_at":"2023-01-19 15:23:39.758161","visits":2},"99":{"joined_at":"2023-01-28 21:23:39.758165","visits":5},"100":{"joined_at":"2023-01-05 01:23:39.758168","visits":6},"101":{"joined_at":"2022-12-25 18:23:39.758171","visits":2},"102":{"joined_at":"2023-01-22 15:23:39.758175","visits":5},"103":{"joined_at":"2022-12-21 09:23:39.758178","visits":5},"104":{"joined_at":"2023-01-28 04:23:39.758181","visits":2},"105":{"joined_at":"2023-01-14 10:23:39.758184","visits":2},"106":{"joined_at":"2023-01-12 23:23:39.758188","visits":5},"107":{"joined_at":"2022-12-19 10:23:39.758191","visits":7},"108":{"joined_at":"2023-01-31 15:23:39.758194","visits":3},"109":{"joined_at":"2022-12-18 07:23:39.758198","visits":7},"110":{"joined_at":"2023-01-17 15:23:39.758201","visits":4},"111":{"joined_at":"2023-01-13 23:23:39.758205","visits":4},"112":{"joined_at":"2023-01-09 14:23:39.758208","visits":7},"113":{"joined_at":"2023-01-07 16:23:39.758211","visits":4},"114":{"joined_at":"2023-01-28 15:23:39.758215","visits":5},"115":{"joined_at":"2023-02-05 22:23:39.758218","visits":6},"116":{"joined_at":"2022-12-24 03:23:39.758221","visits":9},"117":{"joined_at":"2023-01-19 13:23:39.758225","visits":4},"118":{"joined_at":"2022-12-18 11:23:39.758228","visits":6},"119":{"joined_at":"2023-02-03 10:23:39.758231","visits":3},"120":{"joined_at":"2023-01-16 07:23:39.758234","visits":4},"121":{"joined_at":"2023-01-10 06:23:39.758238","visits":4},"122":{"joined_at":"2023-01-11 11:23:39.758241","visits":5},"123":{"joined_at":"2023-01-31 17:23:39.758245","visits":7},"124":{"joined_at":"2023-02-05 16:23:39.758248","visits":5},"125":{"joined_at":"2023-01-03 16:23:39.758251","visits":3},"126":{"joined_at":"2023-01-23 17:23:39.758255","visits":5},"127":{"joined_at":"2022-12-23 18:23:39.758258","visits":7},"128":{"joined_at":"2022-12-30 18:23:39.758261","visits":5},"129":{"joined_at":"2022-12-15 01:23:39.758265","visits":7},"130":{"joined_at":"2022-12-16 23:23:39.758268","visits":1},"131":{"joined_at":"2023-02-01 06:23:39.758271","visits":5},"132":{"joined_at":"2022-12-15 16:23:39.758275","visits":7},"133":{"joined_at":"2022-12-22 00:23:39.758278","visits":6},"134":{"joined_at":"2022-12-31 15:23:39.758282","visits":6},"135":{"joined_at":"2022-12-14 06:23:39.758285","visits":5},"136":{"joined_at":"2023-01-06 11:23:39.758288","visits":6},"137":{"joined_at":"2022-12-26 08:23:39.758291","visits":7},"138":{"joined_at":"2023-02-04 06:23:39.758295","visits":4},"139":{"joined_at":"2022-12-17 22:23:39.758298","visits":5},"140":{"joined_at":"2022-12-19 06:23:39.758301","visits":5},"141":{"joined_at":"2023-01-05 22:23:39.758305","visits":7},"142":{"joined_at":"2022-12-29 11:23:39.758308","visits":5},"143":{"joined_at":"2023-02-06 02:23:39.758311","visits":3},"144":{"joined_at":"2023-01-21 10:23:39.758315","visits":4},"145":{"joined_at":"2022-12-28 21:23:39.758318","visits":8},"146":{"joined_at":"2023-02-08 03:23:39.758321","visits":3},
```
#### 17. Cloudwatch logs screenshots are available

## Commands for Reference
* Connecting Via Port Forwarding
```bash
kubectl port-forward --namespace default svc/<SERVICE_NAME>-postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d postgres -p 5432
```

* Connecting Via a Pod
```bash
kubectl exec -it <POD_NAME> bash
PGPASSWORD="<PASSWORD HERE>" psql postgres://postgres@<SERVICE_NAME>:5432/postgres -c <COMMAND_HERE>
```

4. Run Seed Files
We will need to run the seed files in `db/` in order to create the tables and populate them with data.

```bash
kubectl port-forward --namespace default svc/<SERVICE_NAME>-postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d postgres -p 5432 < <FILE_NAME.sql>
```

### 2. Running the Analytics Application Locally
In the `analytics/` directory:

1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Run the application (see below regarding environment variables)
```bash
<ENV_VARS> python app.py
```

There are multiple ways to set environment variables in a command. They can be set per session by running `export KEY=VAL` in the command line or they can be prepended into your command.


If we set the environment variables by prepending them, it would look like the following:
```bash
DB_USERNAME=username_here DB_PASSWORD=password_here python /analytics/app.py
```
The benefit here is that it's explicitly set. However, note that the `DB_PASSWORD` value is now recorded in the session's history in plaintext. There are several ways to work around this including setting environment variables in a file and sourcing them in a terminal session.

3. Applying and deploying the applicaiton using kubectl

#kubectl apply -f deployment/pvc.yaml
#kubectl apply -f deployment/pv.yaml
#kubectl apply -f deployment/postgresql-deployment.yaml
#kubectl apply -f deployment/postgresql-service.yaml
#kubectl apply -f deployment/secret.yaml
#kubectl apply -f deployment/configmap.yaml
#kubectl apply -f deployment/deployment.yaml

#Note: buildspec.yaml is also available

4. Verifying The Application
* Generate report for check-ins grouped by dates
`curl <BASE_URL>/api/reports/daily_usage`

* Generate report for check-ins grouped by users
`curl <BASE_URL>/api/reports/user_visits`

## Project Instructions
1. Set up a Postgres database with a Helm Chart
2. Create a `Dockerfile` for the Python application. Use a base image that is Python-based.
3. Write a simple build pipeline with AWS CodeBuild to build and push a Docker image into AWS ECR
4. Create a service and deployment using Kubernetes configuration files to deploy the application
5. Check AWS CloudWatch for application logs

### Deliverables
1. `Dockerfile`
2. Screenshot of AWS CodeBuild pipeline
3. Screenshot of AWS ECR repository for the application's repository
4. Screenshot of `kubectl get svc`
5. Screenshot of `kubectl get pods`
6. Screenshot of `kubectl describe svc <DATABASE_SERVICE_NAME>`
7. Screenshot of `kubectl describe deployment <SERVICE_NAME>`
8. All Kubernetes config files used for deployment (ie YAML files)
9. Screenshot of AWS CloudWatch logs for the application
10. `README.md` file in your solution that serves as documentation for your user to detail how your deployment process works and how the user can deploy changes. The details should not simply rehash what you have done on a step by step basis. Instead, it should help an experienced software developer understand the technologies and tools in the build and deploy process as well as provide them insight into how they would release new builds.
