def execute(scope, data, wait = None):
    conn = scope.get('_connection')
    for line in data:
        conn.send(line)
    return 1
