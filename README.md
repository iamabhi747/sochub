# Socket Hub

This project implements a socket hub, where a main server manages all networks. A network is a simple hub where sockets can connect to. This allows multiple sockets to communicate with each other across multiple endpoints.

## Features

- Manage multiple networks
- Connect multiple sockets to a network
- Send and receive messages across multiple endpoints

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```sh
    cd <project-directory>
    ```

## Testing

### Running the Server

To start the server, run the following command:
```sh
python test_server.py
```

### Connecting to the Server
To connect to the server and start an interactive session, run:
```sh
python test_spawn.py [network]
```
- If `network` is provided, it will connect to the specified network.
- If `network` is not provided, it will create a new network.

### Example
1. Start the server:
```sh
python test_server.py
```
2. Connect to the server:
```sh
python test_spawn.py
```
3. In another terminal, connect to the same server and network:
```sh
python test_spawn.py <network>
```

## Code Overview
- `hub.py`: Contains the `SocHub` class, which is the main server that manages all networks.
- `soc.py`: Contains helper function for connecting to network

## License
This project is licensed under the MIT License.