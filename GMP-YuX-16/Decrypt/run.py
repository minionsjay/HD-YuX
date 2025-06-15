## HD_run_process
import subprocess
degree=0
for i in range(1,14):
    # print(degree)
    minisat_command=["python3","gen_smt_inverse_model.py",str(i),str(i+1),str(degree+1)]
    # cadical_command=["python3","test_degree.py",str(i),str(i+1),"cadical"]
    result=subprocess.run(minisat_command,cwd="./")
    degree = result.returncode
    print("degree:",degree)
    print()