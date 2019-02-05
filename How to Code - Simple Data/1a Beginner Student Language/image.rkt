;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname image) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/image)

(define (bulb c)
  (circle 20 "solid" c))

(triangle 50 "solid" "blue")
(round (/ pi 3))


(above (bulb "red")
       (bulb "yellow")
       (bulb "green"))
