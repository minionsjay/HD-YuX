# 编译器
CXX = g++
# 编译选项
CXXFLAGS = -std=c++11 -O3
# 库
LIBS = -lntl -lgmp
# 头文件目录
INCLUDES = -I../Yux

# 源文件
SRC_DIR = ../Yux
ENC_SRC = enc-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp
DEC_SRC = dec-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp

# 可执行文件
ENC_TARGET = enc-sum-Yu2x-16
DEC_TARGET = dec-sum-Yu2x-16

# 默认目标：编译全部
all: $(ENC_TARGET) $(DEC_TARGET)

# 编译加密求和程序
$(ENC_TARGET): enc-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.h
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ enc-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp $(LIBS)

# 编译解密求和程序
$(DEC_TARGET): dec-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.h
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ dec-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp $(LIBS)

# 清理目标
clean:
	rm -f $(ENC_TARGET) $(DEC_TARGET)
