def get_selected(servers):
    for i, v in servers.items():
        if v["selected"]:
            return [i, v]


def get_server_data(servers, server):
    """
        Format:
        {
            servers = {
                ip: "",
                connections: {}
                selected = False
            }
            connections = {
                [server_1, server_2, connect_time]
            }
        }

     returns: (name, server_data)
    """

    # Search by name
    for name in servers.keys():
        if name == server:
            return [name, servers[name]]

    # Search by ip
    for name, data in servers.items():
        ip = data["ip"]
        if ip == server:
            return [name, data]


def get_connections(connections, server):
    """
    Returns all connections with connection_time from a target server

    :param connections:
    :param server:
    :return: [server_2, connection_time]
    """
    c = []

    for i in connections:
        if server in i:
            c.append(i)

    return c


def get_connection_time(connections, server_1, server_2):
    for i in connections:
        if server_1 in i and server_2 in i:
            return i[2]

def create_server(servers, server_name, ip_v4_address):

    # Validate Ip address
    for i in ip_v4_address.split('.'):
        i = int(i)

        if i < 0 or i > 255:
            print("Error: Invalid Ip")
            return

    existing_data = get_server_data(servers, server_name) or get_server_data(servers, ip_v4_address)
    if existing_data:
        print(f"Error: Server already exists as:\n{existing_data[0]}\t{existing_data[1]}")

    servers[server_name] = {"ip": ip_v4_address, "selected" : False}

    print(f"Success: A server with name {server_name} was created at ip {ip_v4_address}")


def create_connection(database, server_1, server_2, connect_time):
    servers = database["servers"]
    connections = database["connections"]
    s1 = get_server_data(servers, server_1)
    s2 = get_server_data(servers, server_2)

    # Check if both servers exist
    if not s1 or not s2:
        print(f"Error: Unable to find servers\n- {server_1}\n- {server_2}")
        return

    # Check if servers are already connected to each other
    if get_connection_time(database["connections"], server_1, server_2):
        print("Error: Servers are already connected to each other")
        return

    # Connect servers to each other
    connections.append([server_1, server_2, connect_time])

    print(f"Success: A server with name {server_1} is now connected to {server_2}")


def set_server(servers, server):
    s1 = get_server_data(servers, server)

    if not s1:
        print(f"Error: Unable to find server\n- {server}")
        return

    # Unselect other selected servers
    for i in servers.values():
        i["selected"] = False

    servers[s1[0]]["selected"] = True

    print(f"Server {s1[0]} was selected.")


def ping(database, target, server_time=0):
    """
        Finds path from current server to target server

        :return: list of used servers or None
    """
    route = traceroute(database, get_selected(database["servers"])[0], target, [])

    if route:
        for i in range(1, len(route)):
            server_1 = route[i-1]
            server_2 = route[i]
            connection_time = get_connection_time(database["connections"], server_1, server_2)
            server_time += int(connection_time)

        print(f"Reply from {target} time = {server_time} ms")

def traceroute(database, current, target, used):
    """
    Finds path from current server to target server

    :return: list of used servers or None
    """
    current_data = get_server_data(database["servers"], current)

    if not current_data:
        print(f"Error: Unable to find server\n- {current}")
        return

    used.append(current)
    connections = get_connections(database["connections"], current)

    for v in connections:
        name = v[0] if v[0] != current else v[1]
        t_data = get_server_data(database["servers"], name)

        if name == target or t_data[1]["ip"] == target:
            used.append(target)
            return used
        elif name not in used:
            result = traceroute(database, name, target, used)

            if result:
                return result
            else:
                used.pop(-1)


def ip_config(servers):
    selected = get_selected(servers)

    if selected:
        print(selected[0], selected[1]["ip"])
    else:
        print("Error: No server selected")


def display_servers(database):
    text = ""

    for name, data in database["servers"].items():
        text += f"\t{name}    {data["ip"]}\n"

        connections = get_connections(database["connections"], name)

        for connection in connections:
            server_2name = connection[0] if connection[0] != name else connection[1]
            connection_data = get_server_data(database["servers"], server_2name)
            text += f"\t\t{server_2name}    {connection_data[1]["ip"]}    {connection[1]}\n"

    print(text)


if __name__ == "__main__":
    mode = ""
    main_database = {"servers": {}, "connections": []}

    assignment_mode = False
    prompts = [
        "create-server twitter.com 104.244.42.193",
        "create-server facebook.com 157.240.241.35",
        "create-server amazon.com 172.5.12.128",
        "create-server netflix.com 158.69.7.238",
        "create-server wikipedia.org 208.80.154.244",
        "create-server umbc.edu 143.204.151.121",
        "create-server twitch.tv 151.101.210.167",
        "create-server discord.gg 162.159.134.234",
        "create-connection twitter.com facebook.com 34",
        "create-connection amazon.com netflix.com 22",
        "create-connection facebook.com amazon.com 14",
        "create-connection twitter.com netflix.com 31",
        "set-server netflix.com",
        "traceroute facebook.com",
        "traceroute umbc.edu",
        "traceroute amazon.com",
        "traceroute 172.5.12.128",
        "create-connection umbc.edu twitch.tv 33",
        "create-connection wikipedia.org umbc.edu 5",
        "create-connection wikipedia.org twitter.com 12",
        "display-servers",
        "ip-config",
        "ping wikipedia.org",
        "set-server umbc.edu",
        "tracert amazon.com",
        "tracert 172.5.12.128",
        "ping amazon.com",
        "quit",
    ]
    curr_prompt_index = 0

    if input("Auto-input? (input from project will run automatically) (y/n): ").lower() == "y":
        assignment_mode = True

    while mode != "quit":
        if assignment_mode and curr_prompt_index < len(prompts):
            mode = prompts[curr_prompt_index]
            print(f"\ncmd: {mode}")
            curr_prompt_index += 1
        else:
            mode = input("")

        mode = mode.split(" ")
        command = mode[0]

        if command == "create-server":
            create_server(main_database["servers"], mode[1], mode[2])
        elif command == "create-connection":
            create_connection(main_database, mode[1], mode[2], mode[3])
        elif command == "set-server":
            set_server(main_database["servers"], mode[1])
        elif command == "ping":
            ping(main_database, mode[1])
        elif command == "traceroute" or command  == "tracert":
            selected = get_selected(main_database["servers"])
            results = traceroute(main_database, selected[0], mode[1], [])

            print(f"Tracing route to {mode[1]}")

            if results:
                print(f"0    0    [{selected[1]["ip"]}]    {selected[0]}")

                for i in range(1, len(results)):
                    d = get_server_data(main_database["servers"], results[i])

                    if i == 1:
                        print(f"{i}    {get_connection_time(main_database["connections"], selected[0], d[0])}    [{d[1]["ip"]}]    {d[0]}")
                    else:
                        d_prev = get_server_data(main_database["servers"], results[i - 1])
                        print(f"{i}    {get_connection_time(main_database["connections"], d[0], d_prev[0])}    [{d[1]["ip"]}]    {d[0]}")

                print("Trace complete.")
            else:
                print(f"Unable to route to target system name {mode[1]}")
        elif command == "ip-config":
            ip_config(main_database["servers"])
        elif command == "display-servers":
            display_servers(main_database)