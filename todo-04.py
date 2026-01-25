import json

def lambda_handler(event, context):
    # Parse incoming request
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {'statusCode': 400, 'body': json.dumps({'error': 'Invalid JSON'})}

    game_data = body.get("game_data", {"tasklist": [], "donelist": []})
    action = body.get("action")
    payload = body.get("payload")
    
    response_msg = ""

    # Logic processing
    if action == "add":
        task = payload.strip()
        if not task:
            response_msg = "❌You cant do that!❌"
        elif task in game_data["tasklist"]:
            response_msg = f"❌{task} already in Quests❌"
        else:
            game_data["tasklist"].append(task)
            response_msg = f"✅{task} added to Quests✅"

    elif action == "done":
        # Simplified: payload is the task string or index
        if payload in game_data["tasklist"]:
            game_data["tasklist"].remove(payload)
            game_data["donelist"].append(payload)
            response_msg = f"🏆{payload} complete!🏆"
        else:
            response_msg = "❌Quest does not exist...❌"

    elif action == "delete":
        if payload in game_data["tasklist"]:
            game_data["tasklist"].remove(payload)
            response_msg = f"🗑️{payload} deleted🗑️"
        elif payload in game_data["donelist"]:
            game_data["donelist"].remove(payload)
            response_msg = f"🗑️{payload} deleted🗑️"

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "game_data": game_data,
            "message": response_msg
        })
    }
