#include <iostream>
using namespace std;
int main()
{
    char a[2];
    a[1] = 254;
    a[0] = 1;
    short *ps;
    void * vp;
    vp = a;
    ps = (short*) vp;
    cout<<*ps<<endl;
    return 0;
}