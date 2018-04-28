#include <iostream>
using namespace std;
int main()
{
    void *vp;
    short *sp;
    char *cp;
    short a = 5;
    short b = -259;
    sp = &a;
    vp = sp;
    cp = (char*)vp;
    cout<<(int)*cp<<endl;
    cp ++;
    cout<<(int)*cp<<endl;

    sp = &b;
    vp = sp;
    cp = (char*)vp;
    cout<<(int)*cp<<endl;
    cp ++;
    cout<<(int)*cp<<endl;
    char* cp2;
    cp2 = new char[2];
    cp2[0] = --*cp;
    cp2[1] = ++*cp;
    vp = cp2;
    sp = (short*) vp;
    cout<<"\n"<<*sp<<endl;
    return 0;
}