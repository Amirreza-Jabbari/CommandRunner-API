from django.test import TestCase
from django.urls import reverse
import json

import zmq
import unittest

class ZMQServerTests(unittest.TestCase):
    def setUp(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")

    def tearDown(self):
        self.socket.close()
        self.context.term()

    def test_valid_os_command(self):
        command = {
            "command_type": "os",
            "parameters": ["echo", "Hello, World!"]
        }
        self.socket.send_json(command)
        response = self.socket.recv_json()
        self.assertEqual(response["status"], "success")
        self.assertIn("Hello, World!", response["result"])

    def test_valid_compute_command(self):
        command = {
            "command_type": "compute",
            "expression": "5 + 3 * 2"
        }
        self.socket.send_json(command)
        response = self.socket.recv_json()
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["result"], 11)

    def test_invalid_command(self):
        command = {
            "command_type": "invalid"
        }
        self.socket.send_json(command)
        response = self.socket.recv_json()
        self.assertEqual(response["status"], "error")

    def test_empty_request(self):
        command = {}
        response = self.client.post(
            reverse('execute-command'),
            data=json.dumps(command),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json()["status"])

    def test_missing_fields(self):
        command = {"command_type": "compute"}
        response = self.client.post(
            reverse('execute-command'),
            data=json.dumps(command),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json()["status"])

    def test_invalid_json_format(self):
        response = self.client.post(
            reverse('execute-command'),
            data="{command_type: os, parameters: [ls]}",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)  # Django should raise a JSONDecodeError
