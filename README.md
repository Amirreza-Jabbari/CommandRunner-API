### **CommandRunner API: A Unified Solution for OS and Math Operations**

---

## **Project Overview**

This project demonstrates a client-server application using **Django REST Framework (DRF)** and **ZeroMQ (ZMQ)** for communication. The server processes two types of commands:

1. **OS Commands:** Executes system commands like `ping`, `ls`, or `echo`.
2. **Math Commands:** Evaluates basic arithmetic expressions such as `(2 + 3) * 4`.

---

## **Technologies Used**

1. **Django**: Python web framework for building the server-side application.
2. **Django REST Framework (DRF)**: Simplifies API development.
3. **ZeroMQ (ZMQ)**: A high-performance messaging library for client-server communication.

---

## **Features**

- Processes OS and Math commands.
- Communicates between client and server using **ZeroMQ**.
- API endpoint for executing commands.
- Handles invalid commands gracefully with error responses.

---

## **How to Set Up and Run**

### **1. Prerequisites**
- Python 3.8 or higher installed.
- Install required libraries:
  ```bash
  pip install django djangorestframework pyzmq
  ```

---

### **2. Start the ZeroMQ Server**
Navigate to the project directory and run the server:
```bash
python core/zmq_server.py
```
The server will start listening on `tcp://*:5555`.

#### Press `Ctrl + C` to Stop:
Output:

```plaintext
[INFO] Server is running...
[INFO] Received message: {'command_type': 'os', 'parameters': ['echo', 'Hello']}
[INFO] Sending response: {'status': 'success', 'result': 'Hello\n'}
^C
[INFO] Server is shutting down...
[INFO] Server closed.
```
---

### **3. Run the Django Application**
Start the Django development server:
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/api/execute-command/`.

---

### **4. Test the API**

You can send POST requests to the `/api/execute-command/` endpoint using **Postman**, **curl**, or similar tools.

#### Example: OS Command
Request:
```json
POST http://127.0.0.1:8000/api/execute-command/
{
  "command_type": "os",
  "parameters": ["echo", "Hello, World!"]
}
```

Response:
```json
{
  "status": "success",
  "result": "Hello, World!\n"
}
```

#### Example: Math Command
Request:
```json
POST http://127.0.0.1:8000/api/execute-command/
{
  "command_type": "compute",
  "expression": "(5 + 3) * 2"
}
```

Response:
```json
{
  "status": "success",
  "result": 16
}
```

---

### **5. Run Tests**
Run the Django unit tests:
```bash
python manage.py test
```

---


## **How It Works**

1. **Client Sends Command:** A JSON request is sent to the `/api/execute-command/` endpoint.
2. **API Processes Request:** The Django view sends the command to the ZeroMQ server.
3. **Server Executes Command:** The ZeroMQ server processes the command (OS or Math) and returns the result.
4. **Response Sent Back:** The API sends the response back to the client.

---

## **Optional Features**

- **unit tests:** Implemented unit tests for the client and server in `tests.py`.
- **Logging:** Added command logging in `zmq_server.py`.
