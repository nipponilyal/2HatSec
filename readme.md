### Solution stack

1. Containers (Docker)
2. Kubernetes - Using multiple parallel worker processes
3. Rancher - Wrapper around kubernetes (UI)
4. Python
5. mysql - Injecting the json data into this db
6. redis - Acting as a worker queue for the k8s jobs

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
6. db structure can be found in : `migrations/scritps/V1_moc-json.sql`

### Chalanges & TODOs to complete the project

1. Setting up a the nfs server so that it will be possible to mount the volume to all the workers
2. The split of the data.json file is manual - Can be automated via another dedicated service that will split and input the result to redis