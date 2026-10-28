import subprocess
from input.INPUTS import PROGRAM_ITERATIONS
from multiprocessing import Pool


for i in range(PROGRAM_ITERATIONS):
    print(f"Calling main.py (Iteration {i+1}/{PROGRAM_ITERATIONS})...")
    subprocess.run(['python', 'main.py'])  



# # Funzione per eseguire un comando del terminale
# def run_main_script(script_name):
#     try:
#         result = subprocess.run(['python', script_name])

#         return result.returncode  
#     except Exception as e:
#         print(f"Errore nell'esecuzione di {script_name}: {e}")
#         return -1  

# if __name__ == "__main__":
#     script_name = "main.py"  
#     num_runs = PROGRAM_ITERATIONS 

#     with Pool(processes=num_runs) as pool:
#         results = pool.map(run_main_script, [script_name] * num_runs)

#     print("Codici di ritorno:", results)
