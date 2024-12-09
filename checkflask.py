import subprocess

# Get the list of environments
result = subprocess.run(['conda', 'env', 'list'], stdout=subprocess.PIPE)
envs = result.stdout.decode().splitlines()

# Skip any empty lines
for env in envs:
    if not env.strip():  # Skip empty lines
        continue

    if "*" not in env:  # Skip the active environment
        env_name = env.split()[0]
        result = subprocess.run(['conda', 'activate', env_name, '&&', 'conda', 'list', 'flask'], stdout=subprocess.PIPE, shell=True)
        if "Flask" in result.stdout.decode():
            print(f"Flask is installed in {env_name}")
        else:
            print(f"Flask is NOT installed in {env_name}")