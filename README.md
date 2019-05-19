# StatFive

## Build and run the project  
`$> docker-compose up -d`

## Test the tracker
You must install an X Server like VcXsrv for Windows 10  
`$> docker exec -it -e DISPLAY=$YOUR_IP_ADDRESS:0.0 statfive_tensorflow_1 bash`  
`$> python tracker.py`
