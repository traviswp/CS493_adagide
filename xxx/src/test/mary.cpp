/*
 *   lab 5: p1
 */

#include <iostream>
#include <fstream>      // need to include fstream

using namespace std; 

int main()
{
    // variables
    string line1,line2; 
    string fname1,fname2;     
    int count = 1; 
    fstream f1,f2; 

    cout << "Please enter the name of the first file: "; 
    getline (cin, fname1); 
    cout << "Please enter the name of the second file: "; 
    getline (cin, fname2); 


    // open the file
    f1.open(fname1.c_str());  
    f2.open(fname2.c_str());  

    // check to make sure file was opened successfully
    // &
    // process file(s)
    if (f1.is_open() && f2.is_open())
    {
        cout << "Both files ('Mary.txt' and 'Mary2.txt') were opened successfully!\n"; 
        cout << "-----------------------------------------------------------------\n";

        while ( f1.good() && f2.good())
        {
            getline (f1,line1);
            getline (f2,line2);
            
            if (!(line1 == line2))
            {
                cout << "Files differ on line " << count << ":\n"; 
                cout << fname1 << ": " << line1 << endl; 
                cout << fname2 << ": " << line2 << endl; 
                break;
            }


            count++; 
        }

        // check to see if one file is shorter...
        if (f1.good())
        {
            cout << "File '" << fname2 << "' is shorter.\n" << endl; 
        }
        else if (f2.good())
        {
            cout << "File '" << fname1 << "' is shorter.\n" << endl; 
        }

        // always close your file(s)!!!
        f1.close();
        f2.close();

        cout << "-----------------------------------------------------------------\n";
    }
    else
    {
        if (f1.is_open())
        {
            cout << "Unable to open file '" << fname2 << "'.\n"; 
        }
        else if (f2.is_open())
        {
            cout << "Unable to open file '" << fname1 << "'.\n"; 
        }
        else
        {
            cout << "Unable to open '" << fname1 << "' or '" << fname2 << "'.\n"; 
        }
    }

    return 0; 
}
