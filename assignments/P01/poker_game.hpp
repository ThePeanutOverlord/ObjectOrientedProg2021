///////////////////////////////////////////////////////////////////////////////
//                   
// Author:           Paige Champagne
// Email:            paigechamp@gmail.com
// Label:            program 1
// Title:            Game of War
// Course:           CMPS 2143
// Semester:         Spring 2020
//
// Description:
//       this file is the inmplementation of the CardContainer, Hand, Deck, and Game
//          classes for the game of War
//
// Usage:
//       This is a simulation of a game of war card game
//
// Files:           main.cpp
//                  playingcard.hpp
//                  poker_game.hpp
//                  termio.h
/////////////////////////////////////////////////////////////////////////////////
#include "termio.h"
#include "playingcard.hpp"
#include <algorithm> // std::random_shuffle
#include <iostream>
#include <string>
#include <deque>
#include <random>
#include <time.h>
#include <stdlib.h>

using namespace std;
Term::IO io;
const string spade = "♠";
const string diamond = "♦";
const string heart = "♥";
const string club = "♣";

const string suits[4] = {"♠", "♦", "♣", "♥"};

// Black background        blue ,  red , blue , red
const string colors2[4] = {"&60", "&20", "&60", "&20"};

// Colored background      blue  , red  , blue , red
const string colors[4] = {"&16", "&12", "&16", "&12"};

// Card labels (could be "Iron Man" or "Charmander" or "Elf" ... anything)
const string ranks[13] = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};


/*
  ██████╗ █████╗ ██████╗ ██████╗  ██████╗ ██████╗ ███╗   ██╗████████╗ █████╗ ██╗███╗   ██╗███████╗██████╗
 ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██║████╗  ██║██╔════╝██╔══██╗
 ██║     ███████║██████╔╝██║  ██║██║     ██║   ██║██╔██╗ ██║   ██║   ███████║██║██╔██╗ ██║█████╗  ██████╔╝
 ██║     ██╔══██║██╔══██╗██║  ██║██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██║██║██║╚██╗██║██╔══╝  ██╔══██╗
 ╚██████╗██║  ██║██║  ██║██████╔╝╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║██║██║ ╚████║███████╗██║  ██║
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
*/
/**
 * class CardContainer
 * 
 * Description:
 *      This is the class that Deck and Hand inhert from that holds a deque of cards
 * 
 * Public Methods:
 *      
 *       CardContainer(int)--constructs a card container of a set size
 *       CardContainer(Card* a, Card* b)--constructs a card container with two cards
 *       void Add(Card *)--adds cards to the card container
 *       bool isEmpty()--checks if the container is empty
 *       void Order()--orders the cards in the container
 *       Card *Remove()--removes a card from the container   
 *       void Reset()--resets the elements in the container
 *       void Shuffle()-shuffles the cards in the container
 *       int Size()--returns size of the container
 *       void Print(int columns, bool clear)--prints everything in the container
 *       Card* Get(int i)--returns a specific card in the container
 * 
 * 
 * Usage: 
 * 
 *     -the base for the Hand and deck classes, holds cards that are currently
 *      being played
 *      
 */
class CardContainer {
protected:
    Term::IO io;
    deque<Card *> Cards;//double ended queue of cards
    int RandomIndex(); //imma be honest i don't know what this or 
    struct CardCompare { //this is for
        bool operator()(Card *l, Card *r) {
            return *l < *r;
        }
    };

public:
    CardContainer(int);
    CardContainer(Card* a, Card* b);
    void Add(Card *);
    bool isEmpty();
    void Order();
    Card *Remove();
    void Reset();
    void Shuffle();
    int Size();
    void Print(int columns, bool clear);
    Card* Get(int i);

};
 /**
     * Public : CardContainer(int numCards)
     * 
     * Description:
     *      initializes new container of numCards size
     * 
     * Params:
     *      - int numCards
     *          the numer of cards to generate
     * 
     * Returns:
     *      - it's a constructor my dude so nothing
     */
CardContainer::CardContainer(int numCards) {
    for (int i = 0; i < numCards; i++) {
        Cards.push_back(new Card(i));
    }
}
 /**
     * Public : CardContainer(Card* a, Card* b)
     * 
     * Description:
     *      generates a new container with two card *s
     * 
     * Params:
     *      - Card* a
     *          Card 1
     *      - Card* b
     *          Card 2
     * 
     * Returns:
     *      - void: nothing
     */
CardContainer::CardContainer(Card* a, Card* b){

  Cards.push_back(a);
  Cards.push_back(b);

}
/**
     * Public : Add(Card* card)
     * 
     * Description:
     *      adds new card* to end of container
     * 
     * Params:
     *      - Card* card
     *          Card  to be added
     * 
     * Returns:
     *      - void: nothing
     */
void CardContainer::Add(Card *card) {

    Cards.push_back(card);
 
}
/**
     * Public : isEmpty()
     * 
     * Description:
     *      checks if the container is empty
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - bool: empty or not
     */
bool CardContainer::isEmpty() {
    return Cards.empty();
}
/**
     * Public : Order()
     * 
     * Description:
     *      uses sort to order cards. i literally never used
     *      this and am just now seeing wher CardCompare comes in
     *      but i still don't understand why it's a struct
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - void: nothing
     */
void CardContainer::Order() {
    sort(Cards.begin(), Cards.end(), CardCompare());
}
/**
     * Public : Remove
     * 
     * Description:
     *      removes a card from the front of the container
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - Card* temp
     */
Card *CardContainer::Remove() {
    Card *temp = Cards.front();
   // contSize--;
   // Cards.resize(contSize);
    Cards.pop_front();
    return temp;
}
/**
     * Public : Reset()
     * 
     * Description:
     *      deletes every card and replaces them with new ones
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - void: nothing
     */
void CardContainer::Reset() {
    for (int i = 0; i < Cards.size() - 1; i++) {
        delete Cards[i];
        Cards[i] = new Card(i);
    }
}
/**
     * Public : Shuffle()
     * 
     * Description:
     *      shuffles cards
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - void: nothing
     */
void CardContainer::Shuffle() {
  //srand(time(0));
    for (int i = 0; i < Cards.size() - 1; i++) {
        int j = i + rand() % (Cards.size() - i);
        swap(Cards[i], Cards[j]);
    }
}
/**
     * Public : Size()
     * 
     * Description:
     *      gets container size
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - int: size
     */
int CardContainer::Size() {
    return Cards.size();
}
/**
     * Public : print(int columns = 1, bool clear = false)
     * 
     * Description:
     *     prints the entire container
     * 
     * Params:
     *      - int columns
     *          number of columns to print the cards in
     *      - bool clear
     *          sets if the screen clears or doesn't
     * 
     * Returns:
     *      - void: nothing
     */
void CardContainer::Print(int columns = 1, bool clear = false) {
    int i = 0;
    deque<string> cards;

    if (clear) {
        io << Term::clear;
    }

    for (auto c : Cards) {
        cards.push_back(c->Repr());

        i++;
        if (i == columns) {
            io << Term::fuse(cards) << "\n";
            i = 0;
            cards.clear();
        }
    }

    // any cards left in the deque should be
    // printed out.
    if (cards.size() > 0) {
        io << Term::fuse(cards) << "\n";
    }
}
/**
     * Public : Get(int i)
     * 
     * Description:
     *     returns but doesn't delete the card at location i
     * 
     * Params:
     *      - int i
     *          index of card to get
     * 
     * Returns:
     *      - Card* of Cards[i]
     */
Card* CardContainer::Get(int i){
      Card *temp = Cards[i];
      return temp;
}
/*
 ██╗  ██╗ █████╗ ███╗   ██╗██████╗
 ██║  ██║██╔══██╗████╗  ██║██╔══██╗
 ███████║███████║██╔██╗ ██║██║  ██║
 ██╔══██║██╔══██║██║╚██╗██║██║  ██║
 ██║  ██║██║  ██║██║ ╚████║██████╔╝
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝
*/
/**
 * class Hand
 * 
 * Description:
 *      represents each player's hand, made up of card containers
 * Protected:
 *      -int handSize
 *          size of hand
 * Public Methods:
 *      
 *       Hand(int)-constructs a hand of a set size
 *       void Print(int columns, bool clear)-prints every card in hand
 *       Card* Play()-plays a card
 *       void PushCard(Card* a)- adds card to end
 *       void Shuffle()-shuffles cards
 *       int Size()-returns the size
 *       void Remove()-removes a card
 *      
 * 
 * Usage: 
 * 
 *     -inhertis from CardContainer, the players of the game
 *      
 */
class Hand : public CardContainer{
protected:
int handSize;

public:
    Hand(int);
    void Print(int columns, bool clear);
    Card* Play();
    void PushCard(Card* a);
    void Shuffle();
    int Size();
    void Remove();
};
/**
     * Public : shuffle()
     * 
     * Description:
     *     shuffles cards
     * 
     * Params:
     * 
     * Returns:
     *      - void: none
     */
void Hand::Shuffle(){
//srand(time(0));
  for (int i = 0; i < Cards.size() - 1; i++) {
        int j = i + rand() % (Cards.size() - i);
        swap(Cards[i], Cards[j]);
    }
}

/**
     * Public : PushCard(Card* a)
     * 
     * Description:
     *     pushes card onto back of the hand
     * 
     * Params:
     *      - Card* a
     *          Card* to add to hand
     * 
     * Returns:
     *      - void: none
     */
void Hand::PushCard(Card* a){
  handSize++;
  Cards.push_back(a);
}
/**
     * Public : Hand(int size)
     * 
     * Description:
     *     constructs hand of a certain size
     * 
     * Params:
     *      - int size
     *          size to make card container
     * 
     * Returns:
     *      - nothing it's a constructor
     */
Hand::Hand(int size) : CardContainer(size) {
    handSize = size;
}
/**
     * Public : Print(int columns = 1, bool clear = false)
     * 
     * Description:
     *     prints everything in the hand
     * 
     * Params:
     *      - int columns
     *          number of columns to print the cards in
     *      - bool clear
     *          sets if the screen clears or doesn't
     * 
     * Returns:
     *      - void: none
     */
void Hand::Print(int columns = 1, bool clear = false) {
    int i = 0;
    deque<string> cards;

    if (clear) {
        io << Term::clear;
    }

    for (auto c : Cards) {
        cards.push_back(c->Repr());

        i++;
        if (i == columns) {
            io << Term::fuse(cards) << "\n";
            i = 0;
            cards.clear();
        }
    }

    // any cards left in the deque should be
    // printed out.
    if (cards.size() > 0) {
        io << Term::fuse(cards) << "\n";
    }
}
/**
     * Public : Play()
     * 
     * Description:
     *     plays (removes and returns) card from top
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - Card* : card being played
     */
Card* Hand::Play(){
    Card *temp = Cards.front();
    handSize--;
    Cards.pop_front(); 
    //Cards.resize(handSize);
    return temp;

}
/**
     * Public : Remove()
     * 
     * Description:
     *     removes card from front
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - void : none
     */
void Hand::Remove(){
      Card *temp = Cards.front();
    Cards.pop_front();
    handSize--;
}
/**
     * Public : Size()
     * 
     * Description:
     *     returns size of hand
     * 
     * Params:
     *      - none
     *          
     * 
     * Returns:
     *      - int handSize
     */
int Hand::Size(){
  return handSize;
}
/*
 ██████╗ ███████╗ ██████╗██╗  ██╗
 ██╔══██╗██╔════╝██╔════╝██║ ██╔╝
 ██║  ██║█████╗  ██║     █████╔╝
 ██║  ██║██╔══╝  ██║     ██╔═██╗
 ██████╔╝███████╗╚██████╗██║  ██╗
 ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝
*/
/**
 * class Deck
 * 
 * Description:
 *      represents a deck that serves as basis for the game
 * Protected:
 *      -int deckSize
 *          size of deck
 * Public Methods:
 *      
 *       Deck(int)-makes a deck of size int
 *       Card* Draw()-removes and card from deck
 *       void Print(int, bool)-prints whole deck
 *       void Split(Hand a, Hand b)-splits deck between two hands
 *       friends with Hand
 *      
 * 
 * Usage: 
 * 
 *     -inhertis from CardContainer, creates base deck for game
 *      
 */
class Deck : public CardContainer {
protected:
    int deckSize;

public:
    Deck(int);
    Card *Draw();
    void Print(int, bool);
    void Split(Hand a, Hand b);
    friend Hand;
};
/**
     * Public : Deck(int size)
     * 
     * Description:
     *     constructs deck of size
     * 
     * Params:
     *      - int size
     *          size for the deck to be
     *          
     * 
     * Returns:
     *      - nothing
     */
Deck::Deck(int size) : CardContainer(size) {
    deckSize = size;
}
/**
     * Public : Draw()
     * 
     * Description:
     *     removes card from back of deck and returns it
     * 
     * Params:
     *      - none
     * 
     * Returns:
     *      - Card* temp
     */
Card *Deck::Draw() {
    Card *temp = Cards.back();
    Cards.pop_back();
    return temp;
}
/**
     * Public : Print(int columns = 1, bool clear = false)
     * 
     * Description:
     *     prints everything in the deck
     * 
     * Params:
     *      - int columns
     *          number of columns to print the cards in
     *      - bool clear
     *          sets if the screen clears or doesn't
     * 
     * Returns:
     *      - void: none
     */
void Deck::Print(int columns = 1, bool clear = false) {
    int i = 0;
    deque<string> cards;

    if (clear) {
        io << Term::clear;
    }

    for (auto c : Cards) {
        cards.push_back(c->Repr());

        i++;
        if (i == columns) {
            io << Term::fuse(cards) << "\n";
            i = 0;
            cards.clear();
        }
    }

    // any cards left in the deque should be
    // printed out.
    if (cards.size() > 0) {
        io << Term::fuse(cards) << "\n";
    }
}

/**
     * Public : Split(Hand a, Hand b)
     * 
     * Description:
     *     splits deck between two hands
     * 
     * Params:
     *      - Hand a
     *          hand 1
     *      - Hand b
     *          hand 2
     * 
     * Returns:
     *      - void : none
     */
void Deck::Split(Hand a, Hand b){
  Shuffle();
  Shuffle();
  Shuffle();
  Shuffle();
  for (int i = 0; i < 26; i++) {
      //int j = i + rand() % (Cards.size() - i);
      a.PushCard(Draw());
      //a.Shuffle();
      b.PushCard(Draw());
     // b.Shuffle();
  }

}


/*
  ██████╗  █████╗ ███╗   ███╗███████╗
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
 ██║  ███╗███████║██╔████╔██║█████╗
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
*/
/**
 * class Game
 * 
 * Description:
 *      Game functions
 * 
 * Public Methods:
 *      
 *       int Compare(Card* a, Card* b)- compares cards a and b
 *       bool End(int p1Size, int p2Size) - ends the game
 *       void War(Hand& a, Hand& b, CardContainer& x) - war sequence
 *       void Distribute(int i, Hand& a, Hand& b, CardContainer& x) - puts cards in winner's deck
 *      
 * 
 * Usage: 
 * 
 *     -comparisons and other game unique functions
 *      
 */
class Game {
protected:
public:
  int Compare(Card* a, Card* b);
  bool End(int p1Size, int p2Size);
  void War(Hand& a, Hand& b, CardContainer& x);
  void Distribute(int i, Hand& a, Hand& b, CardContainer& x);
};
/**
     * Public : War(Hand& a, Hand& b, CardContainer& x)
     * 
     * Description:
     *     starts war by making a new container to use for comparing + adds 
     *      the extra cards into it
     * 
     * Params:
     *      - Hand& a
     *          hand 1 by reference
     *      - Hand& b
     *          hand 2 by reference
     *      - CardContainer& x
     *          container used for comparison that lead to war
     * 
     * Returns:
     *      - void : none
     */
void Game::War(Hand& a, Hand& b, CardContainer& x){
    CardContainer j(a.Play(), b.Play());
   if(a.Size() < 3 || b.Size() < 3){
     for(int i = 0; i < 3; i++){
      j.Add(a.Play());
      j.Add(b.Play());
    }
   }else{
      for(int i = 0; i < a.Size(); i++){
          j.Add(a.Play());
      }
      for(int i = 0; i < b.Size(); i++){
          j.Add(b.Play());
      }
   }
    
    j.Add(x.Remove());
    j.Add(x.Remove());

    Compare(j.Get(0), j.Get(1));

}
/**
     * Public : Distribute(int i, Hand& a, Hand& b, CardContainer& x)
     * 
     * Description:
     *     ensures the winner gets the cards
     * Params:
     * 
     *      -int i
     *          code passed in from the comparison
     *      - Hand& a
     *          hand 1 by reference
     *      - Hand& b
     *          hand 2 by reference
     *      - CardContainer& x
     *          container used in comparison that will be giving cards to a hand
     * 
     * Returns:
     *      - void : none
     */
void Game::Distribute(int i, Hand& a, Hand& b, CardContainer& x){
 // io<< x.isEmpty() << " " << x.Size() <<"\n";
  switch(i){
     case 1:{
         for (int i = 0; i < x.Size()+1; i++) {
           a.PushCard(x.Remove());
          }
          io<< x.isEmpty() <<"\n";
        break;
       }
      case 2:{
          for (int i = 0; i < x.Size()+1; i++) {
             b.PushCard(x.Remove());
          }
          io<< x.isEmpty() << " " << x.Size() <<"\n";
        break;
       }
      case 0:{
        War(a, b, x);
        break;
      }  
  }
}
/**
     * Public : Compare(Card* a, Card* b)
     * 
     * Description:
     *     compares two cards and returns a code for distribution
     * Params:
     * 
     *      - Card* a
     *          first card : player one's card
     *      - Card* b
     *          second card : player two's card

     * 
     * Returns:
     *      - int : code for distribution
     */
int Game::Compare(Card* a, Card* b){

  if(*a > *b){
    return 1;
  }else if(*a < *b){
    return 2;
  }else{
   // io<<"WAR\n\n";
    return 0;
  }
}

/**
     * Public : End(int p1Size, int p2Size)
     * 
     * Description:
     *     ends game
     * Params:
     * 
     *      -int p1Size
     *          player 1 size
     *      -int p2Size
     *          player 2 size
     * 
     * Returns:
     *      - bool : game control bool false
     */
bool Game::End(int p1Size, int p2Size){
 io<<" _____ _____ _____ _____    _____ _____ _____ _____ \n"
   <<"|   __|  _  |     |   __|  |     |  |  |   __| __  |\n"
   <<"|  |  |     | | | |   __|  |  |  |  |  |   __|    -|\n"
   <<"|_____|__|__|_|_|_|_____|  |_____|-___/|_____|__|__|\n";
 
 if(p2Size == 0){
     io << " _____ __    _____ __ __ _____ _____    ___      _ _ _ _____ _____ _____ \n"
        <<"|  _  |  |  |  _  |  |  |   __| __  |  |_  |    | | | |     |   | |   __|\n"
        <<"|   __|  |__|     |_   _|   __|    -|   _| |_   | | | |-   -| | | |__   |\n"
        <<"|__|  |_____|__|__| |_| |_____|__|__|  |_____|  |_____|_____|_|___|_____|\n";
 }else{
   io <<" _____ __    _____ __ __ _____ _____    ___    _ _ _ _____ _____ _____ \n"
      <<"|  _  |  |  |  _  |  |  |   __| __  |  |_  |  | | | |     |   | |   __|\n"
      <<"|   __|  |__|     |_   _|   __|    -|  |  _|  | | | |-   -| | | |__   |\n"
      <<"|__|  |_____|__|__| |_| |_____|__|__|  |___|  |_____|_____|_|___|_____|\n";
 }

   return false;                                                                     
}
