;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname Test) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/image)

;; Image Image -> Boolean
;; Produces true if image1 > image2

(check-expect (bigger?
               (rectangle 10 20 "solid" "red")
               (rectangle 20 20 "solid" "red"))
              false)

(check-expect (bigger?
               (rectangle 30 30 "solid" "red")
               (rectangle 20 20 "solid" "red"))
              true)

(check-expect (bigger?
               (rectangle 20 20 "solid" "red")
               (rectangle 20 20 "solid" "red"))
              false)

(define (bigger? i1 i2)
  (and   (> (image-height i1) (image-height i2))
         (> (image-width i1) (image-width i2))))