
# http://example.comのmock

# Success
class MockResponse_1():
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {
            "success": True,
            "message": "success",
            "estimated_data": {
                "class": 1,
                "confidence": 0.8683
            }
        }


# Failure
class MockResponse_2():
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {
            "success": False,
            "message": "Error:E50012",
            "estimated_data": {}
        }
