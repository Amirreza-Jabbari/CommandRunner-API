import zmq
import os

def process_command(command):
    try:
        print(f"[INFO] Received command: {command}")
        command_type = command.get("command_type")
        if command_type == "os":
            cmd = " ".join(command.get("parameters", []))
            result = os.popen(cmd).read()
        elif command_type == "compute":
            result = eval(command.get("expression", ""))
        else:
            result = "Invalid command type"
        return {"status": "success", "result": result}
    except Exception as e:
        print(f"[ERROR] Failed to process command: {e}")
        return {"status": "error", "message": str(e)}

def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("[INFO] Server is running...")

    # Set a timeout for the socket to prevent indefinite blocking
    socket.setsockopt(zmq.RCVTIMEO, 1000)  # 1000 ms (1 second)

    try:
        while True:
            try:
                message = socket.recv_json()
                print(f"[INFO] Received message: {message}")
                response = process_command(message)
                print(f"[INFO] Sending response: {response}")
                socket.send_json(response)
            except zmq.Again:  # Raised if no message is received within timeout
                continue
            except Exception as e:
                print(f"[ERROR] Server encountered an error: {e}")
                socket.send_json({"status": "error", "message": str(e)})
    except KeyboardInterrupt:
        print("\n[INFO] Server is shutting down...")
    finally:
        socket.close()
        context.term()
        print("[INFO] Server closed.")

if __name__ == "__main__":
    start_server()
