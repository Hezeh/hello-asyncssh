import asyncio, asyncssh

async def run_client(host, username, password, command):
    async with asyncssh.connect(host, username=username, password=password) as conn:
        return await conn.run(command)

async def run_multiple_clients():
    # Put your lists of hosts here
    hosts = ['ip1', 'ip2']

    tasks = (run_client(host, 'user1', '', 'date') for host in hosts)
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print('Task %d failed: %s' % (i, str(result)))
        elif result.exit_status != 0:
            print('Task %d exited with status %s:' % (i, result.exit_status))
            print(result.stderr, end='')
        else:
            print('Task %d succeeded:' % i)
            print(result.stdout, end='')

        print(75*'-')

asyncio.get_event_loop().run_until_complete(run_multiple_clients())