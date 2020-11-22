import json

KEYBOARD = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": json.dumps(''),
                "label": "Предположительное качество дороги"
            },
            "color": "primary"
        }]
    ]
    }