#!/bin/bash
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_SESSION_TOKEN=

# List of workers
workers=(1 2 3 4 5)
# List of pool_size to iterate over
pool_size=(1 2 4 8 16 32 64 128)

for worker in "${workers[@]}"; do
  # Loop through each pool in the list
  for pool in "${pool_size[@]}"; do

    primary_key="naive:1000req:${worker}worker:${pool}pool:${worker}entity"
    echo "Executing command with $primary_key"
    aws dynamodb put-item \
          --table-name ReadModelTable \
          --item "{
                      \"PrimaryKey\": {\"S\": \"$primary_key\"},
                      \"entity1_version\": {\"N\": \"0\"},
                      \"entity2_version\": {\"N\": \"0\"},
                      \"entity3_version\": {\"N\": \"0\"},
                      \"entity4_version\": {\"N\": \"0\"},
                      \"entity5_version\": {\"N\": \"0\"}
                  }"

    sleep 2

    # Record the start time
    start_time=$(date +%s)

#    python naive_preload.py "$primary_key" 1000 "$pool" entity1

    for (( i=1; i<=worker; i++ ))
    do
      # Run the Python script with the same constructed pool and additional parameters
      python naive_preload.py "$primary_key" 1000 "$pool" entity"$i" &
    done

    # Wait for all background processes to finish before moving to the next iteration
    wait

    # Record the end time
    end_time=$(date +%s)

    # Calculate the duration
    duration=$((end_time - start_time))

    # Print the execution time for the current iteration
    echo "Iteration with pool $pool took $duration seconds."

    sleep 2
  done
done
wait
