// Dll2.cpp: define the function of generatin dll
#define EXPORT __declspec(dllexport)


#include<iostream>
using namespace std;


class TestDLL{
public:
    void hello();
};

void TestDLL::hello() {
    cout << "hello world" << endl;
}



extern "C" {
    TestDLL td;
    EXPORT void hello() {
        td.hello();
    }

    EXPORT void hello1() {
        cout << "hello world 111111" << endl;
    }
}