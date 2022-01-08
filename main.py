from subprocess import run

a = run(['docker', 'exec', '3ee25031d576fe555568b9a1a61b55fea14a4ff1f11dab1e34fb769151f9c00f', 'python', 'submit.py', 1, 2], capture_output=True)
print(a.stdout)