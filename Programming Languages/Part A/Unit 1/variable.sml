(* This is a comment *)

val x = 34;
(* dynamic enviorment: x--> 34*)

val y = 17;

(* dynamic enviorment: x--> 34  y--> 17*)
val z = (x + y) + (y + 2);

val q = z + 1;

val absz = if z < 0 then 0 - z else z;

val abs2 = abs(z);