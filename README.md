# Client Server Test

## Installation Instructions 
Install python3.7 
Clone the repository 
install required packages through pip
> pip install -r requirements.txt


## Prepare Dataset
To generate random files for the test. Use Util.py 
**create_sample** function will generate random files from *sample_data* folder and paste them in *dataset* folder with random names. A utility function called **reference_name** generates the random string for each file. 
> How to Use it ? 
```sh
  
if __name__ == '__main__':  
    a = Util()  
    print('preparing dataset')  
 for i in range(0, 100): 
     print(" Number of Images Copied:", i + 1) 
     a.create_samples()
```
## Server.py

Server.py works as the server to accept files upload and give back response to client. For authentication client passes a string that is hardcoded in server.py to check the client authenticity. 
Performs sha256 and verifies source and server checksum

## Client.py
Client.py sends the data to the server, it takes two arguments 'folder_destination' and 'concurrency_rate' for sending data to server. The Authentication code is hard coded inside the code. 
Performs  sha256 checksums on files number of files transfer is proportional to concurrency
>How to Use it  
```sh
if __name__ == '__main__':  
    print(os.path.abspath(sys.argv[1]))  
  
    client_main(os.path.abspath(sys.argv[1]), sys.argv[2])
```
> Run it by typing on terminal 
``` python client.py folder_name concurrency_value #should be integer[0..8] ```


## Generated Test
To run test and generate graph on different concurrency rate run this on client.py 
```
if __name__ == '__main__': 
	import pandas as pd  
	from matplotlib import pyplot as plt  
  
	list_data = list()  
	c1 = client_main('dataset_1', 1)  
	c2 = client_main('dataset_1', 2)  
	c3 = client_main('dataset_1', 4)  
	c4 = client_main('dataset_1', 8)  
	list_data.append(c1)  
	list_data.append(c2)  
	list_data.append(c3)  
	list_data.append(c4)  
	df = pd.DataFrame(list_data)  
	# Using scatter plot  
	plt.scatter(df['concurrency_rate'], df['time_taken'])  
	plt.title('Concurrency throughput')  
	plt.ylabel('Time Taken in Seconds')  
	plt.xlabel('Concurrency rate')  
	plt.show()
```

>Here is the final result of the test scale on 100 files ranging from 8-10MB each in size 
>and running on 1,2,4 and 8 concurrency rate

![Graph Image Latest](https://github.com/jahanxb/client-server/blob/version-1.2.1/concurrency_graph_full.png?raw=true)

Results indicates that the concurrency works better in 2 and 4 workers rate. 
## References

 - https://medium.com/fintechexplained/advanced-python-concurrency-and-parallelism-82e378f26ced
 - https://github.com/vijendra1125/Python-Socket-Programming
 - https://realpython.com/python-sockets/
 - https://docs.python.org/3/library/socket.html

##Known Issues 
 - Checksum generated on two different directories might not match for some files. 
  
 
 
 
