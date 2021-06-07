def main():
    # TODO:
    # 0) get all cmd args (<passwd>, <path>, <server_mode=(tcp || http)>, <server_host>, <server_port>, ...)
    # 1) get [server_database] from <path>
    #   1.1) check if <path> -> 'is ok'
    #   1.2) decrypt [server_database] with <passwd>
    #   1.2) open server database and check whether it's empty or not
    #       => if it is empty -- try create new db with <std_user> and <std_script> (=std_tables)
    #       => if it is not empty -- print content to [stdout]
    # 2) start
    # 3) start in [interactive mode] (=event_loop) => new Thread for working with user
    #       - prints <messages> from [tcp_server] || [http_server?]
    #       - waits for user [commands] = {
    #               stop_server: {}
    #               restart_server: {}
    #               update_db: { table="", field="", value="" },
    #               add_or_replace_script:  { username="", script_name="", script_content="<JSON>" },
    #               add_script_from_path:   { username="", script_name="", json_file="<path>" },
    #               exit: {}
    #       }
    pass
