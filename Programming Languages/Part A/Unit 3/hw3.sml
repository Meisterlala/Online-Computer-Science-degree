(* Coursera Programming Languages, Homework 3, Provided Code *)

exception NoAnswer

datatype pattern = Wildcard
		 | Variable of string
		 | UnitP
		 | ConstP of int
		 | TupleP of pattern list
		 | ConstructorP of string * pattern

datatype valu = Const of int
	      | Unit
	      | Tuple of valu list
	      | Constructor of string * valu

fun g f1 f2 p =
    let 
	val r = g f1 f2 
    in
	case p of
	    Wildcard          => f1 ()
	  | Variable x        => f2 x
	  | TupleP ps         => List.foldl (fn (p,i) => (r p) + i) 0 ps
	  | ConstructorP(_,p) => r p
	  | _                 => 0
    end

(**** for the challenge problem only ****)

datatype typ = Anything
	     | UnitT
	     | IntT
	     | TupleT of typ list
	     | Datatype of string

(**** you can put all your code here ****)


fun only_capitals sl = 
	List.filter (fn fs => Char.isUpper(String.sub(fs,0))) sl

fun longest_string1 sl =
	foldl (fn (s, acc) => if String.size(s) > String.size(acc)
						   then s
						   else acc) "" sl

fun longest_string2 sl =
	foldl (fn (s, acc) => if String.size(s) >= String.size(acc)
						   then s
						   else acc) "" sl

fun longest_string_helper comparison sl =
	foldl (fn (s, acc) => if comparison(String.size(s) , String.size(acc))
						   then s
						   else acc) "" sl

val longest_string3 = 
	longest_string_helper (fn (i1, i2) => i1>i2)

val longest_string4 = 
	longest_string_helper (fn (i1, i2) => i1>=i2)

val longest_capitalized = 
	longest_string3 o only_capitals

val rev_string = String.implode o rev o String.explode




fun first_answer operation list =
	case list of
		[] 	   => raise NoAnswer
	|	hd::tl => case operation hd of
  					  SOME v => v
				  |	  NONE   => first_answer operation tl

fun all_answers operation list =
	let
		fun helper acc list =
			case list of
				[] 	   => SOME acc
			|	hd::tl => case operation hd of
							  NONE   => NONE
						  |   SOME ans => helper (acc@ans) tl
	in
		helper [] list
	end


val count_wildcards = g (fn _ => 1) (fn _ => 0)

val count_wild_and_variable_lengths = g (fn _ => 1) String.size

fun count_some_var (s, p) = 
	g (fn _ => 0) (fn x => if x = s then 1 else 0) p

fun check_pat p =
	let fun get_string_list p =
			case p of
			  Variable s => [s]
			| TupleP pattern_list => List.foldl (fn (p,i) => (get_string_list p) @ i) [] pattern_list
			| ConstructorP(s, pt) => get_string_list pt
			| _ => []

		fun exist_repetitions list_string =
			case list_string of
			  [] => false
			| head::tail => List.exists (fn s => s = head) tail orelse (exist_repetitions tail)
	in
		not((exist_repetitions o get_string_list) p)
	end

fun match(v, p) =
	case (v, p) of
	  (_, Wildcard) => SOME []
	| (v, Variable s) => SOME [(s, v)]
	| (Unit, UnitP) => SOME []
	| (Const x, ConstP y) => if x = y then SOME [] else NONE
	| (Tuple valu_list, TupleP pattern_list) => if length valu_list = length pattern_list
		then all_answers match (ListPair.zip(valu_list, pattern_list)) else NONE
	| (Constructor(s1, v), ConstructorP(s2, p)) => if s1 = s2 then match(v,p) else NONE
	| (_, _) => NONE

fun first_match v pattern_list =
	SOME(first_answer(fn p => match(v, p)) pattern_list) handle NoAnswer => NONE