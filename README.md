# Redis Transfer #

Python scripts that allow you to transfer files and directories between the sender and receiver script through a Redis server.

#### Usage

On receive side

    ./redis-receiver.py <redis_server_IP> <redis_server_port>

On sending side

    ./redis-sender.py <redis_server_IP> <redis_server_port> <transfer_chunk_byte_size> <directory_or_files>


#### Optimization

You can use the memwatch script to monitor memory usage of the Redis server, keep in mind that files are actually copied into the Redis server memory, not disk, so if you send data faster than you receive it then it's possible to use all the server's memory. Avoid crashing the server by limiting the amount of memory allowed to Redis. A decent chunk size to transfer is ~1MB at a time.

    ./redis-memwatch.py <redis_server_IP> <redis_server_port>
