from basic import *

import sys
import os
import subprocess
import time


class GMP:
    def __init__(self, cipher_name, field, state_size, rounds) -> None:
        self.cipher_name = cipher_name
        self.field = field
        self.state_size = state_size
        self.rounds = rounds

        self.variables_p = []
        self.variables_k = []
        self.variables_x = []
        self.variables_y = []
        self.variables_xp = []
        self.variables_yp = []
        self.variables_a = []
        self.filename = f"{cipher_name}_r{self.rounds}_f{self.field}.cvc"
        self.gen_variables()
        self.all_variables = []
        self.all_variables += self.variables_p
        for v in self.variables_k:
            self.all_variables += v
        for v in self.variables_x:
            self.all_variables += v
        for v in self.variables_xp:
            for vv in v:
                if vv != []:
                    self.all_variables += vv
        for v in self.variables_y:
            self.all_variables += v
        for v in self.variables_yp:
            for vv in v:
                if vv != []:
                    self.all_variables += vv
        for v in self.variables_a:
            self.all_variables += v

    def gen_variables(self):
        # content=""
        state_size = self.state_size
        # field=self.field
        rounds = self.rounds
        ## generate plain
        self.variables_p += [f"p_{j}" for j in range(state_size)]
        ## generate key
        for i in range(rounds):
            self.variables_k.append([f"k_{i}_{j}" for j in range(state_size)])
        ## generate x
        for i in range(rounds + 1):
            self.variables_x.append([f"x_{i}_{j}" for j in range(state_size)])
        ## generate y
        for i in range(rounds):
            self.variables_y.append([f"y_{i}_{j}" for j in range(state_size)])
        ## generate x copy
        for i in range(rounds):
            tmp = []
            tmp.append([])
            for j in range(4):
                if j > 0:
                    tmp.append([f"xp_{i}_{j}_{t}" for t in range(j+1)])
            tmp.append([])
            for j in range(4, 8):
                if j > 4:
                    tmp.append([f"xp_{i}_{j}_{t}" for t in range(j-4+1)])
            tmp.append([])
            for j in range(8, 12):
                if j > 8:
                    tmp.append([f"xp_{i}_{j}_{t}" for t in range(j-8+1)])
            tmp.append([])
            for j in range(12, 16):
                if j > 12:
                    tmp.append([f"xp_{i}_{j}_{t}" for t in range(j-12+1)])
            self.variables_xp.append(tmp)
        ## generate y copy
        for i in range(rounds - 1):
            tmp = []
            for j in range(4):
                tmp.append([f"yp_{i}_{j}_{t}" for t in range(3-j + 6 + 1)])
            for j in range(4, 8):
                tmp.append([f"yp_{i}_{j}_{t}" for t in range(7-j + 6 + 1)])
            for j in range(8, 12):
                tmp.append([f"yp_{i}_{j}_{t}" for t in range(11-j + 6 + 1)])
            for j in range(12, 16):
                tmp.append([f"yp_{i}_{j}_{t}" for t in range(15-j + 6 + 1)])
            self.variables_yp.append(tmp)
        tmp = []
        for j in range(3):
            # if j > 0:
            tmp.append([f"yp_{self.rounds-1}_{j}_{t}" for t in range(4-j)])
        tmp.append([])
        for j in range(4, 7):
            # if j > 4:
            tmp.append([f"yp_{self.rounds-1}_{j}_{t}" for t in range(8-j)])
        tmp.append([])
        for j in range(8, 11):
            # if j > 8:
            tmp.append([f"yp_{self.rounds-1}_{j}_{t}" for t in range(12-j)])
        tmp.append([])
        for j in range(12, 15):
            # if j > 12:
            tmp.append([f"yp_{self.rounds-1}_{j}_{t}" for t in range(16-j)])
        tmp.append([])
        self.variables_yp.append(tmp)
        # print(self.variables_yp[-1])

        ## generate add var
        for i in range(rounds):
            self.variables_a.append([f"a_{i}_{j}" for j in range(state_size)])
    def gen_nonlinear_decrypt_cons(self, var_x, var_xp, var_y, var_yp, var_a, last=0):
        field = self.field
        content = ""
        ## copy x3
        copy4_in = var_x[3]
        copy4_out = var_xp[3]
        # print(copy4_in,copy4_out)
        content += general4CopyOperation(copy4_in, copy4_out, field)
        ## copy x2
        copy3_in = var_x[2]
        copy3_out = var_xp[2]
        content += general3CopyOperation(copy3_in, copy3_out, field)
        ## copy x1
        copy2_in = var_x[1]
        copy2_out = var_xp[1]
        content += copyOperation(copy2_in, copy2_out, field)
        ## and x1x2
        and_in = [var_xp[1][0], var_xp[2][0]]
        and_out = var_a[0]
        content += addOperation(and_in, and_out, field)
        ## three xor
        three_xor_in = [var_x[0], var_a[0], var_xp[3][0]]
        three_xor_out = var_y[0]
        content += gen3xorOperation(three_xor_in, three_xor_out, field)
        ## copy y0
        if last == 1:
            copy4_in = var_y[0]
            copy4_out = var_yp[0]
            # print(copy4_in)
            # print(copy4_out)
            content += general4CopyOperation(copy4_in, copy4_out, field)
        else:
            copy10_in = var_y[0]
            copy10_out = var_yp[0]
            content += general10CopyOperation(copy10_in, copy10_out, field)
        ## and x2x3
        and_in = [var_xp[2][1], var_xp[3][1]]
        and_out = var_a[1]
        content += addOperation(and_in, and_out, field)
        ## three xor
        three_xor_in = [var_xp[1][1], var_a[1], var_yp[0][-3]]
        three_xor_out = var_y[1]
        content += gen3xorOperation(three_xor_in, three_xor_out, field)
        ## copy y1
        if last == 1:
            copy3_in = var_y[1]
            copy3_out = var_yp[1]
            content += general3CopyOperation(copy3_in, copy3_out, field)
        else:
            copy9_in = var_y[1]
            copy9_out = var_yp[1]
            content += general9CopyOperation(copy9_in, copy9_out, field)
        ## and x3y0
        and_in = [var_xp[3][2], var_yp[0][-2]]
        and_out = var_a[2]
        content += addOperation(and_in, and_out, field)
        ## three xor
        three_xor_in = [var_xp[2][2], var_a[2], var_yp[1][-2]]
        three_xor_out = var_y[2]
        content += gen3xorOperation(three_xor_in, three_xor_out, field)
        ## copy y2
        if last == 1:
            copy2_in = var_y[2]
            copy2_out = var_yp[2]
            content += copyOperation(copy2_in, copy2_out, field)
        else:
            copy8_in = var_y[2]
            copy8_out = var_yp[2]
            content += general8CopyOperation(copy8_in, copy8_out, field)
        ## and y0y1
        and_in = [var_yp[0][-1], var_yp[1][-1]]
        and_out = var_a[3]
        content += addOperation(and_in, and_out, field)
        ## three xor
        three_xor_in = [var_xp[3][3], var_a[3], var_yp[2][-1]]
        three_xor_out = var_y[3]
        content += gen3xorOperation(three_xor_in, three_xor_out, field)
        ## copy y3
        if last != 1:
            copy7_in = var_y[3]
            copy7_out = var_yp[3]
            content += general7CopyOperation(copy7_in, copy7_out, field)

        return content
    def gen_nonlinear_cons(self, var_x, var_xp, var_y, var_yp, var_a, last=0):
        field = self.field
        content = ""
        ## copy x0
        copy4_in = var_x[0]
        copy4_out = var_xp[0]
        content += general4CopyOperation(copy4_in, copy4_out, field)
        ## copy x1
        copy3_in = var_x[1]
        copy3_out = var_xp[1]
        content += general3CopyOperation(copy3_in, copy3_out, field)
        ## copy x2
        copy2_in = var_x[2]
        copy2_out = var_xp[2]
        content += copyOperation(copy2_in, copy2_out, field)
        ## and x0x1
        and_in = [var_xp[0][0], var_xp[1][0]]
        and_out = var_a[0]
        content += addOperation(and_in, and_out, field)
        ## three xor
        three_xor_in = [var_x[3], var_a[0], var_xp[2][0]]
        three_xor_out = var_y[3]
        content += gen3xorOperation(three_xor_in, three_xor_out, field)
        ## copy y3
        if last == 1:
            copy4_in = var_y[3]
            copy4_out = var_yp[3]
            # print(copy4_in)
            # print(copy4_out)
            content += general4CopyOperation(copy4_in, copy4_out, field)
        else:
            copy19_in = var_y[3]
            copy19_out = var_yp[3]
            content += general19CopyOperation(copy19_in, copy19_out, field)

        ## and y3x0
        and_in = [var_yp[3][-3], var_xp[0][1]]
        and_out = var_a[1]
        content += addOperation(and_in, and_out, field)
        ## three xor
        three_xor_in = [var_xp[2][1], var_a[1], var_xp[1][1]]
        three_xor_out = var_y[2]
        content += gen3xorOperation(three_xor_in, three_xor_out, field)
        ## copy y2
        if last == 1:
            copy3_in = var_y[2]
            copy3_out = var_yp[2]
            content += general3CopyOperation(copy3_in, copy3_out, field)
        else:
            copy18_in = var_y[2]
            copy18_out = var_yp[2]
            content += general18CopyOperation(copy18_in, copy18_out, field)

        ## and y2y3
        and_in = [var_yp[2][-2], var_yp[3][-2]]
        and_out = var_a[2]
        content += addOperation(and_in, and_out, field)
        ## three xor
        three_xor_in = [var_xp[1][2], var_a[2], var_xp[0][2]]
        three_xor_out = var_y[1]
        content += gen3xorOperation(three_xor_in, three_xor_out, field)
        ## copy y1
        if last == 1:
            copy2_in = var_y[1]
            copy2_out = var_yp[1]
            content += copyOperation(copy2_in, copy2_out, field)
        else:
            copy17_in = var_y[1]
            copy17_out = var_yp[1]
            content += general17CopyOperation(copy17_in, copy17_out, field)

        ## and y1y2
        and_in = [var_yp[1][-1], var_yp[2][-1]]
        and_out = var_a[3]
        content += addOperation(and_in, and_out, field)
        ## three xor
        three_xor_in = [var_xp[0][3], var_a[3], var_yp[3][-1]]
        three_xor_out = var_y[0]
        content += gen3xorOperation(three_xor_in, three_xor_out, field)
        ## copy y0
        if last != 1:
            copy16_in = var_y[0]
            copy16_out = var_yp[0]
            content += general16CopyOperation(copy16_in, copy16_out, field)

        return content

    def gen_linear_cons(self, var_in, var_out):

        content = ""
        for i in range(self.state_size):
            new_var_in = []
            for j in range(self.state_size):
                new_var_in.append(var_in[j][i])
            # print(new_var_in)
            content += gen16xorOperation(new_var_in, var_out[i], self.field)
        return content
    def gen_linear_new_cons(self, var_in, var_out):

        M_index=[[0, 3, 4, 8, 9, 12, 14], [1, 4, 5, 9, 10, 13, 15], [0, 2, 5, 6, 10, 11, 14], [1, 3, 6, 7, 11, 12, 15], [0, 2, 4, 7, 8, 12, 13], [1, 3, 5, 8, 9, 13, 14], [2, 4, 6, 9, 10, 14, 15], [0, 3, 5, 7, 10, 11, 15], [0, 1, 4, 6, 8, 11, 12], [1, 2, 5, 7, 9, 12, 13], [2, 3, 6, 8, 10, 13, 14], [3, 4, 7, 9, 11, 14, 15], [0, 4, 5, 8, 10, 12, 15], [0, 1, 5, 6, 9, 11, 13], [1, 2, 6, 7, 10, 12, 14], [2, 3, 7, 8, 11, 13, 15]]
        cnt = [0] * self.state_size  # 假设 self.state_size == 16
        content = ""
        for i in range(self.state_size):
            new_var_in = []
            # for j in range(self.state_size):
            #     new_var_in.append(var_in[j][i])
            # print(new_var_in)
            for j in M_index[i]:
                idx = cnt[j]               # 当前要取的下标
                new_var_in.append(var_in[j][idx])
                cnt[j] += 1                # 取用后计数器加一
            # print(new_var_in)
            content += gen7xorOperation(new_var_in, var_out[i], self.field)
        return content

    def set_variables(self):
        content = ""
        for v in self.all_variables:
            content += f"{v} : BITVECTOR({self.field});\n"
        return content

    def final_constrains(self, mode=0):
        content = ""
        test_degree1 = "{:b}".format(1)
        test_degree0 = "{:b}".format(0)
        for i in range(self.state_size):
            if i == mode:
                content += (
                    f"ASSERT {self.variables_x[self.rounds][i]}"
                    + " = 0bin"
                    + test_degree1.zfill(self.field)
                    + ";\n"
                )
            else:
                content += (
                    f"ASSERT {self.variables_x[self.rounds][i]}"
                    + " = 0bin"
                    + test_degree0.zfill(self.field)
                    + ";\n"
                )
        return content

    def initial_constrains(self, mode=[0]):
        content = ""
        test_degree0 = "{:b}".format(0)
        for i in range(self.state_size):
            if i not in mode:
                content += (
                    f"ASSERT {self.variables_p[i]}"
                    + " = 0bin"
                    + test_degree0.zfill(self.field)
                    + ";\n\n"
                )
            # content+=f"ASSERT x_0_3" + " = 0bin" + test_degree0.zfill(self.field) + ";\n\n"
        return content

    def gen_weight_constraints(self):
        content = ""
        addstr = "0bin" + "0".zfill(self.field - 1)
        content += "wx : BITVECTOR(" + str(self.field) + ");\n"
        content += "ASSERT wx = BVPLUS({}".format(self.field)
        for i in range(self.state_size):
            for b in range(self.field):
                content += "," + addstr + f"@({self.variables_p[i]}[{b}:{b}])"
        content += ");\n\n"
        # content += "\n"
        return content

    def last_constraints(self):
        content = ""
        for i in range(self.state_size):
            if i % 4 == 3:
                content += (
                    f"ASSERT {self.variables_x[-1][i]} = {self.variables_y[-1][i]};\n"
                )
            else:
                content += f"ASSERT {self.variables_x[-1][i]} = {self.variables_yp[-1][i][0]};\n"
        return content

    def gen_gmp_model(self, ts_d):
        content = ""
        content += self.set_variables()
        ## whiting key
        for i in range(self.state_size):
            xor_in = [self.variables_p[i], self.variables_k[0][i]]
            xor_out = self.variables_x[0][i]
            content += xorOperation(xor_in, xor_out, self.field)

        ## round function
        # print(self.variables_xp)
        for r in range(self.rounds):
            ## nonlinear layer
            for i in range(4):
                nonlinear_x = self.variables_x[r][4 * i : 4 * i + 4]
                nonlinear_xp = self.variables_xp[r][4 * i : 4 * i + 4]
                nonlinear_y = self.variables_y[r][4 * i : 4 * i + 4]
                nonlinear_yp = self.variables_yp[r][4 * i : 4 * i + 4]
                nonlinear_a = self.variables_a[r][4 * i : 4 * i + 4]
                if r == self.rounds - 1:
                    # print(nonlinear_yp[r])
                    content += self.gen_nonlinear_decrypt_cons(
                        nonlinear_x,
                        nonlinear_xp,
                        nonlinear_y,
                        nonlinear_yp,
                        nonlinear_a,
                        last=1,
                    )
                else:
                    content += self.gen_nonlinear_decrypt_cons(
                        nonlinear_x,
                        nonlinear_xp,
                        nonlinear_y,
                        nonlinear_yp,
                        nonlinear_a,
                    )
            ## linear layer
            # for i in range(self.state_size):
        for r in range(self.rounds - 1):
            linear_in = self.variables_yp[r]
            # print(linear_in)
            linear_out = self.variables_x[r + 1]
            content += self.gen_linear_new_cons(linear_in, linear_out)
        ## last cons
        content += self.last_constraints()
        ## final cons
        
        ## initial cons
        # content+=self.initial_constrains([0,3,4,7,8,11,12,15])
        input_index=[0]
        output_index=2
        content += self.initial_constrains(input_index)
        content += self.final_constrains(mode=output_index)
        ## weight
        content += self.gen_weight_constraints()
        testdegree = "{:b}".format(ts_d)

        testdegree = testdegree.zfill(self.field)
        self.result_CVC_file=f"{self.cipher_name}_r{self.rounds}_f{self.field}_testdegree{ts_d}_p_({input_index})_c_{output_index}.cvc"
        content += "ASSERT wx = 0bin{};\n".format(testdegree)
        content += "QUERY FALSE;\nCOUNTEREXAMPLE;\n"
        with open(self.filename, "w+") as file:
            file.write(content)

        # print(content)

    def solve(self):
        #PATH_STP = "/home/minions/tools/stp/build/stp"
        PATH_STP = "/home/ninini/tools/stp-new/new/stp"	
        #stp_parameters = f"{PATH_STP} {self.filename} --CVC --cryptominisat --threads 16"
        stp_parameters = f"{PATH_STP} {self.filename} --CVC --cadical "
        result_new = subprocess.run(
            stp_parameters,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout = result_new.stdout
        with open(self.result_CVC_file,"w+") as file:
            file.write(stdout)
        # print(stdout)
        # flag=False
        if "Invalid." in stdout:
            return True
        else:
            return False


if __name__ == "__main__":
    # exit_code = main()
    cipher_name = "YuX_decrypt"
    field = 8
    state_size = 16
    # rounds=3
    # import sys
    # import math
    begin_round = int(sys.argv[1])
    end_round = int(sys.argv[2])
    # gmp=GMP(cipher_name,field,state_size,rounds)
    # print(gmp.all_variables)
    # print(len(gmp.all_variables))
    # gmp.gen_gmp_model(ts_d=16)
    # before_degree=int(sys.argv[3])
    for r in range(begin_round, end_round):
        print("round:", r)
        resultfile = f"YuX_decrypt_r{r}_f{field}_result_p0.txt"
        gmp = GMP(cipher_name, field, state_size, r)
        flag = True
        print("1before_degree:", int(sys.argv[3]))
        testdegree = int(sys.argv[3])
        gmp.gen_gmp_model(ts_d=testdegree)
        start_time = time.time()
        while flag:
            print("testdegree:", testdegree)
            flag = gmp.solve()
            if flag == False:
                break
            testdegree += 1
            gmp.gen_gmp_model(ts_d=testdegree)
        end_time = time.time() - start_time
        # before_degree=testdegree-1
        # print("2before_degree:",before_degree)
        with open(resultfile, "w+") as file:
            file.write(f"round = {r}\n")
            file.write(f"maxdegree = {testdegree-1}\n")
            file.write(f"time = {end_time}\n")
        # return before_degree
    sys.exit(testdegree - 1)  # 使用 sys.exit 来返回状态码
