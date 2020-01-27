///////////////////////////////////////////////////////////////////////////////
//                   
// Author:           Paige Champagne
// Email:            paigechamp@gmail.com
// Label:            assignment 2
// Title:            Commenting Code
// Course:           CMPS 2143
// Semester:         Spring 2020
//
// Description:
//       This is just me commenting a program that has a linked list that does things? 
//
// Usage:
//       whatever you may use a linked list for
//
// Files:           main.cpp
/////////////////////////////////////////////////////////////////////////////////

#include <iostream>

using namespace std;

int A[100]; //initializes an integer array of size 100
/**
 * Struct Node
 * 
 * Description:
 *      the objects that make up the linked list
 * 
 * Public Methods:
 *      Node() : default constructor
 *      Node(int n) : constructor that takes an integer and creates a node with it
 * 
 * 
 * Usage: 
 * 
 *     -it's each item of the linked list
 *      
 */

struct Node
{
    int x;
    Node *next;
    Node()
    {
        x = -1;
        next = NULL;
    }
    Node(int n)
    {
        x = n;
        next = NULL;
    }
};
/**
 * Class List
 * 
 * Description:
 *     links Nodes together
 * 
 * Public Methods:
 *      - default constructor : List()
 *      - void Push(int val)
 *      - void Insert(int val)
 *      - void PrintTail()
 *      - string Print()
 *      - int pop()
 *      - List operator+(const List &Rhs)
 * 
 * Private Methods:
 *      - just these variables
 *          Node *Head, *Tail
 *          int Size
 * Usage: 
 * 
 *      - linked list with methods to insert an integer, pops one,
 *        prints fom the back of the list, and prints it. Also has
 *        an overloaded operator I think??? idk how that works yet
 *      
 */
class List
{
  private:
    Node *Head;
    Node *Tail;
    int Size;

  public:
    List()
    {
        Head = Tail = NULL;
        Size = 0;
    }
    /**
     * Public : Push
     * 
     * Description:
     *      pushes a new node onto the end of the list
     * 
     * Params:
     *      - int val
     *          value of the new node
     * 
     * Returns:
     *      - void: nothing
     */
    void Push(int val)
    {
        // allocate new memory and init node
        Node *Temp = new Node(val);

        if (!Head && !Tail)
        {
            Head = Tail = Temp;
        }
        else
        {
            Tail->next = Temp;
            Tail = Temp;
        }
        Size++;
    }
    /**
     * Public : Insert
     * 
     * Description:
     *      inserts a new node onto the front of the list
     * 
     * Params:
     *      - int val
     *          value of noed to be inserted
     * 
     * Returns:
     *      - void: nothing
     */
    void Insert(int val)
    {
        // allocate new memory and init node
        Node *Temp = new Node(val);

        // figure out where it goes in the list

        Temp->next = Head;
        Head = Temp;
        if (!Tail)
        {
            Tail = Head;
        }
        Size++;
    }
    /**
     * Public : PrintTail
     * 
     * Description:
     *      prints the last value
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - void
     */
    void PrintTail()
    {
        cout << Tail->x << endl;
    }
    /**
     * Public : Print
     * 
     * Description:
     *      moves the list into one string variable and returns it
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - string list
     *          
     */
    string Print()
    {
        Node *Temp = Head;
        string list;

        while (Temp != NULL)
        {
            list += to_string(Temp->x) + "->";
            Temp = Temp->next;
        }

        return list;
    }
    /**
     * Public : Pop
     * 
     * Description:
     *      it should pop a node off but it seems to just subtract 1 from size
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - int
     *          just 0
     */
    // not implemented 
    int Pop()
    {
        Size--;
        return 0; //
    }
     /**
     * Public : operator+
     * 
     * Description:
     *      i honestly don't know
     * 
     * Params:
     *      - const List &Rhs
     * 
     * Returns:
     *      - List
     *         a new list 
     */
    // not implemented 
    List operator+(const List &Rhs)
    {
        // Create a new list that will contain both when done
        List NewList;

        // Get a reference to beginning of local list
        Node *Temp = Head;

        // Loop through local list and Push values onto new list
        while (Temp != NULL)
        {
            NewList.Push(Temp->x);
            Temp = Temp->next;
        }

        // Get a reference to head of Rhs
        Temp = Rhs.Head;

        // Same as above, loop and push
        while (Temp != NULL)
        {
            NewList.Push(Temp->x);
            Temp = Temp->next;
        }

        // Return new concatenated version of lists
        return NewList;
    }
    /**
     * Public : Operator[]
     * 
     * Description:
     *      i also don't know
     * 
     * Params:
     *      - int index
     * 
     * Returns:
     *      - int
     *          Temp's value
     */
    // Implementation of [] operator.  This function returns an
    // int value as if the list were an array.
    int operator[](int index)
    {
        Node *Temp = Head;

        if (index >= Size)
        {
            cout << "Index out of bounds, exiting";
            exit(0);
        }
        else
        {

            for (int i = 0; i < index; i++)
            {
                Temp = Temp->next;
            }
            return Temp->x;
        }
    }
    /**
     * Public : ostream &operator<<
     * 
     * Description:
     *      overloads and makes printing simpler
     * 
     * Params:
     *      - ostream &os, List L
     * 
     * Returns:
     *      - friend
     *          os
     */
    friend ostream &operator<<(ostream &os, List L)
    {
        os << L.Print();
        return os;
    }
};
    /**
     * Public : main
     * 
     * Description:
     *      main function, creates two lists, loads them with numbers, prints
     * 
     * Params:
     *      - int argc
     *      - char **argv
     * 
     * Returns:
     *      - int
     *          0
     */
int main(int argc, char **argv)
{
    List L1;
    List L2;

    for (int i = 0; i < 25; i++)
    {
        L1.Push(i);
    }

    for (int i = 50; i < 100; i++)
    {
        L2.Push(i);
    }

    //cout << L1 << endl;
    L1.PrintTail();
    L2.PrintTail();

    List L3 = L1 + L2;
    cout << L3 << endl;

    cout << L3[5] << endl;
    return 0;
}