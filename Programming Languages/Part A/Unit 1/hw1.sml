
fun is_older (a : int*int*int, b : int*int*int) =
    if (#1 a) < (#1 b)
    then true
    else if (#2 a) < (#2 b)
    then true
    else if (#3 a) < (#3 b)
    then true
    else false

fun number_in_month (l : (int * int * int) list, m : int) =
    if null l
    then 0
    else 
	let val sum = number_in_month(tl l, m)
	in
	    if ((#2 (hd l)) = m)
	    then sum + 1
	    else sum
	end

fun number_in_months (l : (int * int * int) list, m : int list) =
    if null m orelse null l 
    then 0
    else number_in_month(l, (hd m)) + number_in_months(l, (tl m))

fun dates_in_month (l : (int * int * int) list, m : int) = 
    if null l
    then []
    else if ((#2 (hd l)) = m)
    then hd l :: dates_in_month(tl l,m)
    else dates_in_month(tl l,m)

fun dates_in_months (l : (int * int * int) list, m : int list) =     
    if null l orelse null m
    then []
    else dates_in_month(l, (hd m)) @ dates_in_months(l, (tl m))

fun get_nth (los: string list, n: int) =
    if n = 1
    then hd los
    else get_nth(tl los, n - 1) 


fun date_to_string (d: int*int*int) =
    let val month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    in get_nth(month, (#2 d)) ^ " " ^ Int.toString((#3 d)) ^ ", " ^ Int.toString((#1 d))
    end

fun number_before_reaching_sum (sum : int, l: int list) =
    if sum <= hd l
    then 0
    else 1 + number_before_reaching_sum(sum - hd l, tl l)

fun what_month(day: int) =
    let val month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    in number_before_reaching_sum(day, month_lengths) + 1
    end

fun month_range (d1 : int, d2 : int) =
    if d1 > d2
    then []
    else what_month(d1) :: month_range(d1 + 1, d2)

fun oldest(dates : (int * int * int) list) =
    if null dates
    then NONE
    else if null (tl dates)
    then SOME(hd dates)
    else
        let val val_ans = oldest(tl dates)
        in
            if is_older(hd dates, valOf val_ans)
            then SOME(hd dates)
            else val_ans
        end

