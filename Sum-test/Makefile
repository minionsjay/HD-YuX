
CXX = g++

CXXFLAGS = -std=c++11 -O3

LIBS = -lntl -lgmp

INCLUDES = -I../Yux


SRC_DIR = ../Yux
ENC_SRC = enc-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp
DEC_SRC = dec-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp


ENC_TARGET = enc-sum-Yu2x-16
DEC_TARGET = dec-sum-Yu2x-16


all: $(ENC_TARGET) $(DEC_TARGET)


$(ENC_TARGET): enc-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.h
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ enc-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp $(LIBS)


$(DEC_TARGET): dec-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.h
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ dec-sum-Yu2x-16.cpp $(SRC_DIR)/Yu2x-16.cpp $(LIBS)


clean:
	rm -f $(ENC_TARGET) $(DEC_TARGET)
