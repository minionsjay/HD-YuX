import subprocess
import math

'''

Basic Operation:
    - xorOperation(strIn,strOut,n,command)
    - addOperation(strIn,strOut,n,command)
    - copyOperation(strIn,strOut,n,command)
    - generalCopyOperation(strIn,strOut,n,command)
    - powerOperation(strIn,strOut,n,d,command)
    - queryFalse

'''

'''

STP:
    startSATsolver(stp_file)
    solveSTP(stp_file)

'''

PATH_CRYPTOMINISAT = "/usr/local/bin/cryptominisat5"
PATH_STP = "/usr/local/bin/stp"


# ============= XOR ==============
def xorOperation(strIn, strOut, n):
    command=""
    command += "ASSERT " + strOut + \
        " = BVPLUS(" + str(n) + "," + strIn[0] + "," + strIn[1] + ");\n"
    command += "ASSERT " + strOut + " & " + \
        strIn[0] + " = " + strIn[0] + ";\n\n"

    return command
def gen3xorOperation(strIn,strOut,n):
    command=""
    command += "ASSERT " +strOut + " = BVPLUS(" + str(n) + "," + strIn[0] + "," + strIn[1] + ","+strIn[2] + ");\n"
    command += "ASSERT " +strOut + " & " + strIn[0] + " = " + strIn[0] + ";\n\n"
    # for i in range(len(strIn)):
    #     command += "ASSERT  BVLE ({} , {});\n".format(strIn[i], strOut)
    command += "ASSERT {} & {} = {} ;\n".format(strOut, strIn[1],strIn[1])

    command += "ASSERT {} & {} = {} ;\n".format(strOut, strIn[2],strIn[2])

    addstr = "0bin" + "0".zfill(n-1)
    weight_out=f"BVPLUS({n}"
    for i in range(n):
        weight_out+=f", {addstr}@({strOut}[{i}:{i}])"
    
    weight_in=f"BVPLUS({n}"
    for i in range(n):
        for j in range(len(strIn)):
            weight_in+=f", {addstr}@({strIn[j]}[{i}:{i}])"

    command+=f"ASSERT {weight_out}) = {weight_in});\n"
    # for i in range(n):

    # command += "ASSERT BVLE ({} , {});\n".format(strIn[2], strOut)

    return command
def gen7xorOperation(strIn,strOut,n):
    command=""
    command += "ASSERT " +strOut + " = BVPLUS(" + str(n) 
    for i in range(7):
        command+="," + strIn[i] 
    command+= ");\n"
    for i in range(7):
        command += "ASSERT " +strOut + " & " + strIn[i] + " = " + strIn[i] + ";\n"
    # for i in range(len(strIn)):
    #     command += "ASSERT  BVLE ({} , {});\n".format(strIn[i], strOut)

    addstr = "0bin" + "0".zfill(n-1)
    weight_out=f"BVPLUS({n}"
    for i in range(n):
        weight_out+=f", {addstr}@({strOut}[{i}:{i}])"
    
    weight_in=f"BVPLUS({n}"
    for i in range(n):
        for j in range(len(strIn)):
            weight_in+=f", {addstr}@({strIn[j]}[{i}:{i}])"

    command+=f"ASSERT {weight_out}) = {weight_in});\n"
    # for i in range(n):

    # command += "ASSERT BVLE ({} , {});\n".format(strIn[2], strOut)

    return command
def gen16xorOperation(strIn,strOut,n):
    command=""
    command += "ASSERT " +strOut + " = BVPLUS(" + str(n) 
    for i in range(16):
        command+="," + strIn[i] 
    command+= ");\n"
    for i in range(16):
        command += "ASSERT " +strOut + " & " + strIn[i] + " = " + strIn[i] + ";\n"
    # for i in range(len(strIn)):
    #     command += "ASSERT  BVLE ({} , {});\n".format(strIn[i], strOut)

    addstr = "0bin" + "0".zfill(n-1)
    weight_out=f"BVPLUS({n}"
    for i in range(n):
        weight_out+=f", {addstr}@({strOut}[{i}:{i}])"
    
    weight_in=f"BVPLUS({n}"
    for i in range(n):
        for j in range(len(strIn)):
            weight_in+=f", {addstr}@({strIn[j]}[{i}:{i}])"

    command+=f"ASSERT {weight_out}) = {weight_in});\n"
    # for i in range(n):

    # command += "ASSERT BVLE ({} , {});\n".format(strIn[2], strOut)

    return command
# ============= ADD ==============
def addOperation(strIn, strOut, n):

    command=""
    command += "ASSERT " + strIn[0] + " = " + strOut + ";\n"
    command += "ASSERT " + strIn[1] + " = " + strOut + ";\n"
    # command += "ASSERT " + strIn[0] + " = " + strIn[1] + ";\n"
    command += "\n"

    return command


# ============= COPY ==============
def copyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(1);\n".format(strMod)

    command += "ASSERT {}@{} = BVPLUS( {} , 0bin0@{}, 0bin0@{}, 0bin{}@{});\n".format(
        strMod, strIn, n+1, strOut[0], strOut[1], downstr, strMod)
    command += "ASSERT {}@{} /= 0bin1{};\n".format(strMod, strIn, downstr)

    return command

# ============= 3-COPY ==============


def general3CopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(2);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin10);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin00);\n".format(strMod)

    command += "ASSERT {}@{} = BVPLUS( {} , 0bin00@{}, 0bin00@{}, 0bin00@{},0bin{}@{});\n".format(
        strMod, strIn, n+2, strOut[0], strOut[1], strOut[2], downstr, strMod)
    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin00 ELSE BVGE( {} , 0bin00) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command

# ============= 4-COPY ==============


def general4CopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(2);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin11);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin00);\n".format(strMod)

    command += "ASSERT {}@{} = BVPLUS( {} , 0bin00@{}, 0bin00@{}, 0bin00@{}, 0bin00@{}, 0bin{}@{});\n".format(
        strMod, strIn, n+2, strOut[0], strOut[1], strOut[2],strOut[3], downstr, strMod)
    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin00 ELSE BVGE( {} , 0bin00) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command


# =============7-COPY================


def general7CopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(3);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin110);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin000);\n".format(strMod)

    command += f"ASSERT {strMod}@{strIn} = BVPLUS( {n+3} "
    for i in range(7):
        command += f", 0bin000@{strOut[i]} "
    command+= f", 0bin{downstr}@{strMod});\n"

    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin000 ELSE BVGE( {} , 0bin000) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command
# =============8-COPY================


def general8CopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(3);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin111);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin000);\n".format(strMod)

    command += f"ASSERT {strMod}@{strIn} = BVPLUS( {n+3} "
    for i in range(8):
        command += f", 0bin000@{strOut[i]} "
    command+= f", 0bin{downstr}@{strMod});\n"

    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin000 ELSE BVGE( {} , 0bin000) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command
# =============9-COPY================


def general9CopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(4);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin1000);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin0000);\n".format(strMod)

    command += f"ASSERT {strMod}@{strIn} = BVPLUS( {n+4} "
    for i in range(9):
        command += f", 0bin0000@{strOut[i]} "
    command+= f", 0bin{downstr}@{strMod});\n"

    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin0000 ELSE BVGE( {} , 0bin0000) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command

# =============10-COPY================


def general10CopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(4);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin1001);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin0000);\n".format(strMod)

    command += f"ASSERT {strMod}@{strIn} = BVPLUS( {n+4} "
    for i in range(10):
        command += f", 0bin0000@{strOut[i]} "
    command+= f", 0bin{downstr}@{strMod});\n"

    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin0000 ELSE BVGE( {} , 0bin0000) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command
# =============16-COPY================


def general16CopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(4);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin1111);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin0000);\n".format(strMod)

    command += f"ASSERT {strMod}@{strIn} = BVPLUS( {n+4} "
    for i in range(16):
        command += f", 0bin0000@{strOut[i]} "
    command+= f", 0bin{downstr}@{strMod});\n"

    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin0000 ELSE BVGE( {} , 0bin0000) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command
# =============17-COPY================


def general17CopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(5);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin10000);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin00000);\n".format(strMod)

    command += f"ASSERT {strMod}@{strIn} = BVPLUS( {n+5} "
    for i in range(17):
        command += f", 0bin00000@{strOut[i]} "
    command+= f", 0bin{downstr}@{strMod});\n"

    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin00000 ELSE BVGE( {} , 0bin00000) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command

# =============18-COPY================


def general18CopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(5);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin10001);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin00000);\n".format(strMod)

    command += f"ASSERT {strMod}@{strIn} = BVPLUS( {n+5} "
    for i in range(18):
        command += f", 0bin00000@{strOut[i]} "
    command+= f", 0bin{downstr}@{strMod});\n"

    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin00000 ELSE BVGE( {} , 0bin00000) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command

# =============19-COPY================


def general19CopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(5);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin10010);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin00000);\n".format(strMod)

    command += f"ASSERT {strMod}@{strIn} = BVPLUS( {n+5} "
    for i in range(19):
        command += f", 0bin00000@{strOut[i]} "
    command+= f", 0bin{downstr}@{strMod});\n"

    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin00000 ELSE BVGE( {} , 0bin00000) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command
# =============7-COPY================


def generalCopyOperation(strIn, strOut, n):

    command=""
    downstr = "0".zfill(n)
    strMod = "t_" + strIn
    command += "{} : BITVECTOR(3);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin111);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin000);\n".format(strMod)

    command += "ASSERT {}@{} = BVPLUS( {} , 0bin000@{}, 0bin000@{}, 0bin000@{}, 0bin000@{},0bin000@{},0bin000@{},0bin000@{},0bin{}@{});\n".format(
        strMod, strIn, n+3, strOut[0], strOut[1], strOut[2], strOut[3], strOut[4], strOut[5], strOut[6], downstr, strMod)
    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin000 ELSE BVGE( {} , 0bin000) ENDIF);\n".format(
        strIn, downstr, strMod, strMod)

    return command

# ============= POWER ==============


def powerOperation(strIn, strOut, n, d):
#    print(d)
    command=""
    lenp = math.floor(math.log(d-1)/math.log(2))+1
#    print(lenp)
    rangep = "{:b}".format(d-1).zfill(lenp)

    strMod = "p_" + strIn
    command += "{} : BITVECTOR({});\n".format(strMod, lenp)

    command += "ASSERT BVLE( {} , 0bin{});\n".format(strMod, rangep)
    command += "ASSERT BVGE( {} , 0bin{});\n".format(strMod, "0".zfill(lenp))

    newlen = n + lenp
    strMul0 = "{:b}".format(d).zfill(newlen)
    strMul1 = "0".zfill(lenp) + "@" + strOut
    strAdd = "0".zfill(n) + "@" + strMod

    command += "ASSERT {}@{} = BVPLUS( {}, BVMULT( {}, 0bin{}, 0bin{} ),0bin{});\n".format(
        strMod, strIn, newlen, newlen, strMul0, strMul1, strAdd)

    return command


def queryFalse(fw):
    command = "QUERY FALSE;\nCOUNTEREXAMPLE;\n"
    fw.write(command)


###################################################################################


"""
Return CryptoMiniSat process started with the given stp_file.
"""


def startSATsolver(stp_file):

    # Start STP to construct CNF
    subprocess.check_output([PATH_STP, "--exit-after-CNF", "--output-CNF",
                            stp_file, "--CVC", "--disable-simplifications"])

    # if test
    # Find the number of solutions with the SAT solver
    sat_params = [PATH_CRYPTOMINISAT, "--maxsol", str(1000000000),
                  "--verb", "0", "--printsol", "0", "output_0.cnf"]

    sat_process = subprocess.Popen(
        sat_params, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    return sat_process


'''
Returns the solution for the given SMT problem using STP.
'''


def solveSTP(stp_file):

    stp_parameters = [PATH_STP, stp_file, "--CVC"]
    result = subprocess.check_output(stp_parameters)

    return result.decode("utf-8")
