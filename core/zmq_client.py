import zmq

def send_command(command):
    try:
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        socket.send_json(command)
        response = socket.recv_json()
        return response
    except Exception as e:
        return {"status": "error", "message": str(e)}
