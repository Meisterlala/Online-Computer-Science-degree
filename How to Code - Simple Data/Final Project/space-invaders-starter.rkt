;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-abbr-reader.ss" "lang")((modname space-invaders-starter) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/universe)
(require 2htdp/image)

;; Space Invaders


;; Constants:

(define WIDTH  300)
(define HEIGHT 500)

(define INVADER-X-SPEED 1.5)  ;speeds (not velocities) in pixels per tick
(define INVADER-Y-SPEED 1.5)
(define -INVADER-Y-SPEED (- 0 INVADER-Y-SPEED))
(define TANK-SPEED 5)
(define MISSILE-SPEED 10)

(define HIT-RANGE 10)

(define INVADE-RATE 980)

(define BACKGROUND (empty-scene WIDTH HEIGHT))

(define INVADER
  (overlay/xy (ellipse 10 15 "outline" "blue")              ;cockpit cover
              -5 6
              (ellipse 20 10 "solid"   "blue")))            ;saucer

(define TANK
  (overlay/xy (overlay (ellipse 28 8 "solid" "black")       ;tread center
                       (ellipse 30 10 "solid" "green"))     ;tread outline
              5 -14
              (above (rectangle 5 10 "solid" "black")       ;gun
                     (rectangle 20 10 "solid" "black"))))   ;main body

(define TANK-HEIGHT/2 (/ (image-height TANK) 2))

(define MISSILE (ellipse 5 15 "solid" "red"))



;; Data Definitions:

(define-struct game (invaders missiles tank))
;; Game is (make-game  (listof Invader) (listof Missile) Tank)
;; interp. the current state of a space invaders game
;;         with the current invaders, missiles and tank position

;; Game constants defined below Missile data definition

#;
(define (fn-for-game s)
  (... (fn-for-loinvader (game-invaders s))
       (fn-for-lom (game-missiles s))
       (fn-for-tank (game-tank s))))



(define-struct tank (x dir))
;; Tank is (make-tank Number Integer[-1, 1])
;; interp. the tank location is x, HEIGHT - TANK-HEIGHT/2 in screen coordinates
;;         the tank moves TANK-SPEED pixels per clock tick left if dir -1, right if dir 1

(define T0 (make-tank (/ WIDTH 2) 0))   ;center going right
(define T1 (make-tank 50 1))            ;going right
(define T2 (make-tank 50 -1))           ;going left


(define (move-tank t)
  (cond [(or (< WIDTH (+ (tank-x t) (tank-dir t)))  (> 0 (+ (tank-x t) (tank-dir t)))) t]
        [else (make-tank (+ (tank-x t) (tank-dir t)) (tank-dir t))]))



(define-struct invader (x y dx))
;; Invader is (make-invader Number Number Number)
;; interp. the invader is at (x, y) in screen coordinates
;;         the invader along x by dx pixels per clock tick
;
;(define I1 (make-invader 150 100 12))           ;not landed, moving right
;(define I2 (make-invader 150 HEIGHT -10))       ;exactly landed, moving left
;(define I3 (make-invader 150 (+ HEIGHT 10) 10)) ;> landed, moving right


(define I1 (make-invader 30 0 -INVADER-Y-SPEED))
(define I2 (make-invader 60 -20 INVADER-Y-SPEED))
(define I3 (make-invader 150 100 INVADER-Y-SPEED))


(define Invaders (list I1 I2 I3))





(define (move-invaders i)
  (cond [(empty? i) empty]
        [(> (invader-y (first i)) (+ HEIGHT 30)) empty]     
        [else (cons (make-invader (+ (invader-x (first i)) (invader-dx (first i))) (+ (invader-y (first i)) INVADER-Y-SPEED)
                          (cond [(>= (+ (invader-x (first i)) INVADER-X-SPEED INVADER-X-SPEED) WIDTH) (- 0 INVADER-X-SPEED)]
                                [(<= (+ (invader-x (first i)) INVADER-X-SPEED INVADER-X-SPEED) 0) INVADER-X-SPEED]
                                [else (invader-dx (first i))])
                          ) (move-invaders (rest i)))]
      )
  )






(define-struct missile (x y))
;; Missile is (make-missile Number Number)
;; interp. the missile's location is x y in screen coordinates

(define M1 (make-missile 150 300))                       ;not hit U1
(define M2 (make-missile (invader-x I1) (+ (invader-y I1) 10)))  ;exactly hit U1
(define M3 (make-missile (invader-x I1) (+ (invader-y I1)  5)))  ;> hit U1



(define (move-missiles m)
  (cond [(empty? m) empty]
        [(< (missile-y (first m)) -50) empty]
        [else (cons (make-missile (missile-x (first m)) (- (missile-y (first m)) MISSILE-SPEED)) (move-missiles (rest m)))]  
      )
  )



(define G0 (make-game empty empty T0))
(define G1 (make-game empty empty T1))
(define G2 (make-game (list I1) (list M1) T1))
(define G3 (make-game Invaders empty T0))


; Functions:


;; game -> game
;; start the world with (main 0)
;; 
(define (main g)
  (big-bang g               ; game
    (on-tick   tick) ; game -> game
    (to-draw   render)      ; game -> Image
    (on-key handle-key) ; game Keyevent -> game
    (on-release hande-release))) ; game Keyevent -> game  


;; game -> game
(define (tick g) (collison-m  (move-missiles (game-missiles g)) (addInvader (make-game (move-invaders (game-invaders g)) (move-missiles (game-missiles g)) (move-tank (game-tank g))))))

(define (addInvader g) (if (> (random 1000) INVADE-RATE)
                           (make-game (cons (make-invader (random WIDTH) -10 (if (= (random 2) 1) INVADER-Y-SPEED -INVADER-Y-SPEED)) (game-invaders g)) (game-missiles g) (game-tank g))
                           g))


(define (collison-m m g) (cond [(empty? m) g]

                                 [else (collison-m (rest m) (make-game (collison-i (game-invaders g) (missile-x (first m)) (missile-y (first m))) (game-missiles g) (game-tank g)) ) ]))



(check-expect (collison-i (list I1 I2) 30 0) false)


(define (collison-i m x y) (cond [(empty? m) empty]
                                 [(and (and (>= x (- (invader-x (first m)) 50)) (<= x (+ (invader-x (first m)) 50)))
                                       (and (>= y (- (invader-y (first m)) 50)) (<= y (+ (invader-y (first m)) 50))))
                                  (rest m)]
                                 [else (cons (first m) (rest m))]))


;; game -> Image
;; render the pic
(define (render g) (render-invaders (game-invaders g)
                    (render-missiles (game-missiles g)
                     (place-image TANK  (tank-x (game-tank g)) (- HEIGHT TANK-HEIGHT/2) BACKGROUND)
                   )))



(define (render-missiles m i) (if (empty? m)
                                  i
                                  (place-image MISSILE
                                               (missile-x (first m))
                                               (missile-y (first m))
                                               (render-missiles (rest m) i)))
                                         )


(define (render-invaders m i) (if (empty? m)
                                  i
                                  (place-image INVADER
                                               (invader-x (first m))
                                               (invader-y (first m))
                                               (render-invaders (rest m) i)))
                                         )


;; game Keyevent -> game
(define (handle-key g ke)
  (cond [(or (key=? ke "w") (key=? ke " ")) (make-game (game-invaders g) (cons (make-missile (tank-x (game-tank g)) (- HEIGHT (image-height TANK)))  (game-missiles g)) (game-tank g))]
        [(or (key=? ke "a") (key=? ke "left"))  (make-game (game-invaders g) (game-missiles g) (make-tank (tank-x (game-tank g)) (- 0 TANK-SPEED)))]
        [(or (key=? ke "d") (key=? ke "right")) (make-game (game-invaders g) (game-missiles g) (make-tank (tank-x (game-tank g)) TANK-SPEED))]
        [else g]
        ))

;; game Keyevent -> game
(define (hande-release g ke)
  (cond 
        [(or (key=? ke "a") (key=? ke "left"))  (make-game (game-invaders g) (game-missiles g) (make-tank (tank-x (game-tank g)) 0))]
        [(or (key=? ke "d") (key=? ke "right")) (make-game (game-invaders g) (game-missiles g) (make-tank (tank-x (game-tank g)) 0))]
        [else g]
        ))


(main G3)










