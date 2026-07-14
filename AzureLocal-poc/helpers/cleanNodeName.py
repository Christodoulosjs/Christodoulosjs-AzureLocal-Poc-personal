import json          
def get_node_name(data):            
    output = data["properties"]["properties"]["instanceView"]["output"]
    print(data)
    try:
        result = json.loads(output)
        node_name = result["Node"]
        return node_name
    except Exception:
        pass

    for line in output.splitlines():
        if "Starting resize on node:" in line:
            return line.split(":", 1)[1].strip()

    raise ValueError("Node name not found in run command output")