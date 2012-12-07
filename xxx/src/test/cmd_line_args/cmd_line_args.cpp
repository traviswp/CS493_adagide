/*
 *   lab 5: p2 (p4)
 */

#include <iostream>

using namespace std; 

int main(int argc, char *argv[])
{
    // argc contains the number of arguments present at the command line
    cout << "There are " << argc << " arguments:" << endl; 

    // argv is an array which contains the arguments present at the command
    // line - by looping through the array in order (or accessing a particular
    // element), you can get the argument(s) you need/want. 
    int nArg; 
    for (nArg = 0; nArg < argc; nArg++)
    {
        cout << "argument " << nArg << ": " << argv[nArg] << endl;
    }
 
    return 0;
}