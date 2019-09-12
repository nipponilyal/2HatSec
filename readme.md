### Solution stack

1. Containers (Docker)
2. Kubernetes - jobs
3. Rancher 
4. Python
5. mysql 
6. redis

### folder structure 

1. deployment - main kubernetes manifests for the json handler
2. intr - main python code (rediswq.py publicly available lib imported in to the project)
3. Dockerfile - to build the python image to be used by the k8s job
4. requirements.txt - 3rd party dependencies
5. run.sh - build and deploy the job
6. migrations - Using flyway to structure the db

### Solution explained

1. The data.json file is uploaded into an NFS server so that it can be shared across all running pods
2. i'm using Linux `split` commnad to split the large data file into smaller files (done manually)
3. Using redis as my work queue i'm adding the files names as tasks into redis (using redis-cli)
4. From the migration running run.sh to migrate and create the relevant tables
5. From the root folder - `run.sh` to create 3 pods that will start consuming the queue (redis) and adding the data to the mysql db