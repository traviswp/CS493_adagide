#include <iostream>

using namespace std;
#include "ccc_shap.cpp"

int main()
{  double slope;

   double xcoord, ycoord;
   Point p1, p2; 

   cout << "Input x coordinate of the first point: ";
   cin >> xcoord;
   cout << "Input y coordinate of the first point: ";
   cin >> ycoord;

   p1 = Point(xcoord, ycoord);

   cout << "Input x coordinate of the second point: ";
   cin >> xcoord;
   cout << "Input y coordinate of the second point: ";
   cin >> ycoord;

   p2 = Point(xcoord, ycoord);

   slope = (p2.get_y() - p1.get_y()) / (p2.get_x() - p1.get_x() );

   cout << "The slope of the line between Points 1 and 2 is " << slope ;
   return 0;
}
