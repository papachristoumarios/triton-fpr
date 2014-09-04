cmake_minimum_required(VERSION 2.8)
project( detectors )
find_package( OpenCV REQUIRED )
SET (CMAKE_CXX_FLAGS "-fPIC -Wall")

add_library(detectors SHARED detectors.cpp)
#add_library(test SHARED test.cpp)


target_link_libraries( detectors ${OpenCV_LIBS} )
