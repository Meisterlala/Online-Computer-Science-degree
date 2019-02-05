;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname and_or_not) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/image)

(define width 100)
(define height 100)


(define i1 (rectangle 30 20 "solid" "red"))
(define i2 (rectangle 20 10 "solid" "red"))


(and (> (image-height i1) (image-height i2))
     (> (image-width i1) (image-width i2)))
