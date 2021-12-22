#pragma once
#include <iostream>
#include <list>
#include <vector>
#include <pybind11/stl.h>
#include <cmath>


using namespace std;
class Rect
{
    friend class R_Tree;
private:
    class Point {
        friend class R_Tree;
    public:
        double x;
        double y;
        Point(double x, double y);
        Point();
        bool operator==(const Point& rhs);


    };
public:
    Rect(Point lt, Point rb);
    Rect(double ltx, double lty, double rbx, double rby);
    Rect();
    bool operator==(const Rect& rhs);
    friend ostream& operator<<(ostream& os, const Rect& rct);
    Point get_lt();
    Point get_rb();
    string to_string();
    static double distance(Point p1, Point p2);
    static string to_str(Point p);
    double get_ltx();
    double get_lty();
    double get_rbx();
    double get_rby();

private:


    Point lt;
    Point rb;
    static bool is_overlap(Rect E, Rect S);
    double area();
    static double area_to_increase(Rect E, Rect S);
    static Rect marged_rect(Rect E, Rect S);
    static double Area(vector<Rect> R);








};

