Universal Pipeline
1. get_data
2. move_data (sometimes optional)
3. transform_data (substeps for multiple transforms)
4. stage_data
5. ingest_data

Specific to this CSV pipeline
0. process_data (master function / controller module)
    a. imports the below modules 
    b. calls the helper modules (never run by themselves)
    c. calls timer decorator and logger modules (never run by themselves)
1. get_data_csv
2. move_to_staged_directory (cloud proof future)
    a. copy_to_directory (valid URN)
    b. copy_to_s3 (whichever cloud platform)
3. transform_data (in memory)
    a. transform_data_currency
    b. transform_data_remove_subtotal_col
    b. transform_data_full_name_to_id
    c. transform_data_rename_percentage
        i. transform_person_type_to_id will be encapsulated in transform_data_full_name_to_id
    d. transform_data_percentage_to_int
        i. transform_data_percentage_to_int will be encapsulated in transform_data_rename_percentage
    
4. stage_data_for_ingest (output data)
5. ingest_data_postgres

this is mirroring getting into microservers and/or airflow/another platform
emphasize helper libraries
Setup extensive logging of each microfunction
Uses icecream for debugging

DOCKER COMMANDS
1. docker must be installed on local machine
2. Requirements.txt has all libraries and dependencies
3. docker build -t <image_name> . 
    docker build -t revolution_pipeline .
4. Configure all the files to your specific testing in subdirectory before running docker
    a. config
    b. files_to_consume
    c. logs
5. If there are code changes, rebuild the image:
    docker build -t revolution_pipeline:latest .
6. Run the container and connect to the network and mount the volumes for config, files_to_consume, and logs folders.
    docker run --add-host=postgres_palmdale:172.19.0.2 --name=pipeline_service --network my_network -v /Users/itech88/Desktop/Projects/Palmdale/Python/revolution_report_transform/config:/app/config -v /Users/itech88/Desktop/Projects/Palmdale/Python/revolution_report_transform/logs:/app/logs -v /Users/itech88/Desktop/Projects/Palmdale/Python/revolution_report_transform/files_to_consume/:/app/files_to_consume  -p 4000:80 revolution_pipeline:latest
-docker network inspect my_network
the docker postgres_palmdale container is at 172.19.0.2
