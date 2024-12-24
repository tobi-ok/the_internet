# The Internet Simulation

This project simulates basic internet operations by implementing a network of interconnected servers. Users can create servers, connect them, and simulate operations such as `ping`, `traceroute`, and more.

## Features
- **Create and Manage Servers:**
  - Add servers with valid IPv4 addresses.
  - Display all servers and their connections.

- **Networking Operations:**
  - `ping`: Simulates a ping to a target server and returns the time.
  - `traceroute`: Finds the path between the current server and a target server, showing intermediate hops and times.

- **Custom Commands:**
  - `create-connection`: Connect two servers with a specified time delay.
  - `set-server`: Select the active server for operations.
  - `ip-config`: View the current active server's details.

## Commands
1. `create-server [server_name] [ip_v4_address]`  
   Adds a server with the specified name and IPv4 address.
   
2. `create-connection [server_1] [server_2] [connect_time]`  
   Connects two servers with a specified connection time (in milliseconds).

3. `set-server [server_name or ip_v4_address]`  
   Sets the active server for subsequent commands.

4. `ping [server_name or ip_v4_address]`  
   Simulates a ping operation, showing the round-trip time.

5. `traceroute [server_name or ip_v4_address]`  
   Displays the path and times from the active server to the target.

6. `ip-config`  
   Shows the active server's name and IP address.

7. `display-servers`  
   Lists all servers and their connections.

8. `quit`  
   Ends the simulation.

## Requirements
- Python 3.x

## Running the Program
1. Ensure the Python file (`the_internet.py`) is in your working directory.
2. Run the script using:
   ```bash
   python the_internet.py
