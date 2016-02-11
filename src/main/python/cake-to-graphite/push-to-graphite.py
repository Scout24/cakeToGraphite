import socket


class GraphiteLogger():
    def __init__(self, graphite_host):
        self.graphite_host = graphite_host
        self.localhost = socket.gethostname().split('.')[0]
        self.graphite_port = 2003

    def send_status_to_graphite(self, project, dimension, value, check_time):
        graphite_string = project + "." + str(dimension) + " " + str(value) + " " + str(check_time) + "\n"
        try:
            s = socket.socket()
            s.connect((self.graphite_host, self.graphite_port))
            s.settimeout(10)
            s.sendall(graphite_string)
        finally:
            s.close()


def push_data(response_dict, test_name, graphite_host):
    for response in response_dict.values():
        status_name = response.keys()[0]
        performance_name = response.keys()[1]
        location_name = response.keys()[2]
        time_name = response.keys()[3]
        status = response[status_name]
        check_time = response[time_name]
        performance = response[performance_name]
        graphite = GraphiteLogger(graphite_host)
        graphite.send_status_to_graphite("test.statuscake." + test_name, performance_name, performance, check_time)
        if status == 200:
            count = 1;
        else:
            count = 0;
        graphite.send_status_to_graphite("test.statuscake." + test_name, status, count, check_time)
