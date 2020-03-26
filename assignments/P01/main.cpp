///////////////////////////////////////////////////////////////////////////////
//                   
// Author:           Paige Champagne
// Email:            paigechamp@gmail.com
// Label:            program 1
// Title:            game of war
// Course:           CMPS 2143
// Semester:         Spring 2020
//
// Description:
//          main file that contains game driver
//
// Usage:
//       the part that actually does the thing
//
// Files:           main.cpp
//                  playingcard.hpp
//                  poker_game.hpp
//                  termio.h
/////////////////////////////////////////////////////////////////////////////////

#include "poker_game.hpp"
#include <iomanip>

int main(){

    Term::IO io;
    Game k; //instance of a game
    Deck D(52); //deck of 52 cards
    Hand player1(26); //hand for p1
    Hand player2(26); //hand for p2
    bool cont = true; //loop control variable
    for(int i=0;i<50;i++){ //fills deck
        D.Shuffle();
        //D.Print(2,true);
        break;
       // io << Term::sleep(200); 
    }

   D.Split(player1, player2); //splits deck between player hands
   player1.Shuffle(); 
  // player1.Print(4, true);
   
 
   player2.Shuffle();
  // player2.Print(4, true); 
while(cont){
  io << "Cards: " << player1.Size() << "     Cards: " << player2.Size() <<"\n";
   CardContainer i(player1.Play(), player2.Play()); //puts first card of each into playing container
    
   i.Print(2, false); //prints cards being played
    io<<"Player 1        Player 2\n";

    k.Distribute(k.Compare(i.Get(0), i.Get(1)), player1, player2, i); //compares and distributes cards
     
    if(player1.Size() == 0 || player2.Size() == 0){ //checks if either of them are out of cards
     cont = k.End(player1.Size(), player2.Size());//ends game if either is out of cards
    }

}
    return 0;
}