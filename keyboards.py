import json

KEYBOARD = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": json.dumps(''),
                "label": "Узнать предположительное качество дороги"
            },
            "color": "primary"
        }],
        [{
            "action": {
                "type": "text",
                "payload": json.dumps(''),
                "label": "Узнать период ремонта конкретной дороги"
            },
            "color": "primary"
        }]
    ]
    }