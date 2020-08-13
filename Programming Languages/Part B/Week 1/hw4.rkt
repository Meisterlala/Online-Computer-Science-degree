
#lang racket

(provide (all-defined-out)) ;; so we can put tests in a second file

;; put your code below


(define (sequence low high stride)
  (if (> low high)
      null
      (cons low (sequence (+ low stride) high stride))))


(define (string-append-map xs suffix)
  (map (lambda (x) (string-append x suffix)) xs))

(define (list-nth-mod xs n)
  (cond [(< n 0) (error "list-nth-mod: negative number")]
        [(empty? xs) (error "list-nth-mod: empty list")]
        [#t (car (list-tail xs (remainder n (length xs))))]))


(define (stream-for-n-steps s n)
  (if (= n 0)
      null
      (let ([pair (s)])
        (cons (car pair)
              (stream-for-n-steps (cdr pair) (- n 1))))))

(define funny-number-stream
  (letrec ([f (lambda (x) (cons (if (= (remainder x 5) 0) (- 0 x) x) (lambda () (f (+ x 1)))))])
    (lambda () (f 1))))

(define dan-then-dog
  (letrec ([f (lambda (x) (cons x (lambda () (f (if (string=? x "dog.jpg") "dan.jpg" "dog.jpg")))))])
    (lambda () (f "dan.jpg"))))

(define (stream-add-zero s)
  (letrec ([f (lambda (s)
                (let ([pr (s)])
                  (cons (cons 0 (car pr)) (lambda () (f (cdr pr))))))])
    (lambda () (f s))))


(define (cycle-lists xs ys)
  (letrec ([f (lambda (x)
                (cons
                 (cons (list-nth-mod xs x) (list-nth-mod ys x))
                 (lambda () (f (+ x 1)))))])
    (lambda () (f 0))))


(define (vector-assoc v vec)
  (letrec ([f (lambda (i)
                (cond
                  [(equal? (vector-length vec) i) #f]
                  [(not (pair? (vector-ref vec i))) (f (+ i 1))]
                  [(equal? (car (vector-ref vec i)) v) (vector-ref vec i)]
                  [else (f (+ i 1))]))])
    (f 0)))


(define (cached-assoc xs n)
  (letrec ([memo (make-vector n #f)]
           [iter 0]
           [f (lambda (val)
               (let ([ans (vector-assoc val memo)])
                 (if ans
                     (cdr ans)
                     (let ([new-ans (assoc val xs)])
                       (begin
                         (vector-set! memo iter (cons val new-ans))
                         (set! iter (if (= (+ 1 iter) n) 0 (+ iter 1)))
                             new-ans)))))])
    (lambda (v) (f v))))



