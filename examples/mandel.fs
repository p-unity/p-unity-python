( https://github.com/zevv/zForth/blob/master/forth/mandel.zf )

( calculate and draw mandelbrot fracal )

: chars    s" .--=o+*#% " ;
: output   5 / chars drop + @ emit ;

( Ar Ai Br Bi -- Cr Ci : Add two complex numbers )

: c+       rot + rot rot + swap ;

( Ar Ai -- Ar Ai : Square a complex number )

: c2       swap dup dup * rot dup dup * rot swap - rot rot 2 * * ;

( Ar Ai -- abs A  : absolute value of complex number )

: abs      * 2 pick dup * + ;

( Cr Ci n Zr Ci -- Cr Ci n Zr Ci : do one iteration of complex Z+C  )

: iter
	c2
	4 pick 4 pick c+
	rot 1 + rot rot ;

( Cr Ci -- n : find number of iterations before complex point C goes out of bounds )

: point
	0 0 0
	begin
		iter
		over over abs 4 >
		3 pick 48 >
		+
	until
	drop drop rot rot drop drop ;

: rows   ;
: mandel 0.5 -2.0 do
           1.0 -1.0 do
             j i point output
           0.040 loop+ cr
         0.08 loop+ ;

mandel


