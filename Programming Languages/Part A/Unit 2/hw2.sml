(* Dan Grossman, Coursera PL, HW2 Provided Code *)

(* if you use this function to compare two strings (returns true if the same
   string), then you avoid several of the functions in problem 1 having
   polymorphic types that may be confusing *)
fun same_string(s1 : string, s2 : string) =
    s1 = s2

(* put your solutions for problem 1 here *)


fun all_except_option (s, sl) =
   case sl of
      [] => NONE
      | hd::sl' =>
         if same_string(s,hd)
         then SOME sl'
         else case all_except_option(s, sl') of
                NONE => NONE
              | SOME ls => SOME (hd :: ls)

fun get_substitutions1 (sll, s) =
   case sll of
      [] => []
      | hd::sll' =>
         case all_except_option(s,hd) of
         NONE => get_substitutions1(sll',s)
         | SOME sl => sl @ get_substitutions1(sll',s)


fun get_substitutions2 (sll, s) =
    let
        fun helper(sll, s, acc) =
            case sll of
               [] => acc
             | hd :: sll' => case all_except_option(s, hd) of
                NONE => helper(sll', s, acc)
              | SOME ls => helper(sll', s, ls @ acc)
    in
        helper(sll, s, [])
    end


fun similar_names (sll,name) =
    let 
         val {first=f, middle=m, last=l} = name
	      fun make_names xs =
	         case xs of
		         [] => []
	         | x::xs' => {first=x, middle=m, last=l}::(make_names(xs'))
    in
	      name::make_names(get_substitutions2(sll,f))
    end  



(* you may assume that Num is always used with values 2, 3, ..., 10
   though it will not really come up *)
datatype suit = Clubs | Diamonds | Hearts | Spades
datatype rank = Jack | Queen | King | Ace | Num of int 
type card = suit * rank

datatype color = Red | Black
datatype move = Discard of card | Draw 

exception IllegalMove

(* put your solutions for problem 2 here *)


fun card_color card = 
   case card of 
      (Clubs,_)  => Black
   |  (Spades,_) => Black
   |  (_,_)      => Red

fun card_value card =
   case card of
      (_,Jack)  => 10
   |  (_,Queen) => 10
   |  (_,King)  => 10
   |  (_,Ace)   => 11
   |  (_,Num n) => n

fun remove_card (cs, c, e) =
   case cs of
      [] => raise IllegalMove
   |  card::rest => 
         if card=c 
         then rest
         else card::remove_card(rest, c, e)

fun all_same_color cards =
   case cards of
      [] => true
   |  card::rest =>
      case rest of
         [] => true
      | card'::rest' => card_color(card) = card_color(card') andalso all_same_color(rest)

fun sum_cards cards =
   let 
      fun helper(cards, acc) =
         case cards of
            [] => acc
         | card::rest => helper(rest, card_value(card) + acc)
   in
      helper(cards,0)
   end

fun score (cards, goal) =
    let
        val sum = sum_cards(cards)
        fun pre_score(sum, goal) =
            if sum > goal
            then 3 * (sum - goal)
            else goal - sum
    in
        if all_same_color(cards)
        then pre_score(sum, goal) div 2
        else pre_score(sum, goal)
    end


fun officiate (cards, moves, goal) =
   let
      fun helper (cards, moves, held_cards) =
         case moves of
            [] => held_cards
         |  move::rest => case move of
               Discard card => helper(cards,rest, remove_card(held_cards, card, IllegalMove))
            |  Draw => case cards of
                 [] => held_cards
               | topcard::stack => 
                    if sum_cards (topcard::held_cards) > goal
                    then topcard::held_cards
                    else helper(stack, rest, topcard::held_cards)                 
   in
      score(helper(cards,moves,[]),goal)
   end

