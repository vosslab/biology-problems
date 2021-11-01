

autosomal_dominant = [
	("xTo.#To.#T*%"
	+"r+d.r^d.r+d%"
	+"*#xTo.oTx*#%"
	+"..r^d.r^d..%"
	+"*Tx.#=o.*T#%"
	+"r+Tdr+Tdr+d%"
	+"#*x*#o##ox#%"
	),	
	("#T*.oT#.xTo%"
	+"r+d.r^d.r+d%"
	+"x#*T#.oTxo#%"
	+"..r^d.r^d..%"
	+"oT#.x=*.oT#%"
	+"r+drT+Tdr+d%"
	+"#o#x*#o*oo#%"
	),
]
[	("#To.xT*.#To.#To%"
	+"r^d.r^d.r^d.r^d%"
	+"o.oTx.o.#.oT#.#%"
	+"..r^d.....r^d..%"
	+"oTx.*--T--#.oT#%"
	+"r^d.r-T^T-d.r^d%"
	+"#.o.*.x.o.#.#.o%"
	),
]


autosomal_recessive = [
	("#T*.#To.[T(%"
	+"r+d.r^d.r+d%"
	+"([(T#.oTx[(%"
	+"..r^d.r^d..%"
	+"oT#.(=[.(T#%"
	+"r+drT+Tdr+d%"
	+"##o*#(x[o[#%"
	),
	("[To.(T[.#To%"
	+"r+d.r^d.r+d%"
	+"oo(Tx.(T###%"
	+"..r^d.r^d..%"
	+"oT*.[=(.oT#%"
	+"r+drT+Tdr+d%"
	+"o#o[(*oxoo#%"
	),	
]
[	("#To.#To.#To.#To%"
	+"r^d.r^d.r^d.r^d%"
	+"o.*T#.o.#.oTx.#%"
	+"..r^d.....r^d..%"
	+"oT#.o--T--#.oT#%"
	+"r^d.r-T^T-d.r^d%"
	+"#.o.o.x.*.#.#.o%"
	),
]

x_linked_dominant = [
	("#To.#T*.#To%"
	+"r+d.r^d.r+d%"
	+"o#oTx.*T##o%"
	+"..r^d.r^d..%"
	+"xT*.#=*.oT#%"
	+"r+drT+Tdr+d%"
	+"#***xo*#o##%"
	),
	("xT*.oT#.#T*%"
	+"r+d.r^d.r+d%"
	+"#**T#.oTx##%"
	+"..r^d.r+d..%"
	+"oT#.#=*#*T#%"
	+"r+drT+Tdr+d%"
	+"#oo##*oo*##%"
	),
]
[
	("#To..xTo%"
	+"r^d...|.%"
	+"#.x-T-*.%"
	+"r-T-+-d.%"
	+"*.*.#.*.%"
	),
	("#To.xTo%"
	+"r^d..|.%"
	+"#.xT-*.%"
	+"r-T^T-d%"
	+"*.*.#.*%"
	),
]

x_linked_recessive = [
	("xTo.#To.#T*%"
	+"r+d.r^d.r+d%"
	+"(#(T#.oTxxo%"
	+"..r^d.r^d..%"
	+"#To.x=(.(T#%"
	+"r+drT+Tdr+d%"
	+"##oox*x#ox#%"
	),
	("xTo.oT#.#T*%"
	+"r+d.r^d.r+d%"
	+"(#(T#.oTx(x%"
	+"..r^d.r^d..%"
	+"oT#.x=(.#To%"
	+"r+drT+Tdr+d%"
	+"oo#*ox#*#o#%"
	),
]
[	("#To..xTo%"
	+"r^d...|.%"
	+"#.x-T-*.%"
	+"r-T-+-d.%"
	+"x.o.x.x.%"
	),
]





y_linked = [
	("#To.#To.xTo%"
	+"r+d.r^d.r+d%"
	+"o#oT#.oTxxo%"
	+"..r^d.r^d..%"
	+"oT#.o=x.oT#%"
	+"r+drT+Tdr+d%"
	+"##ooxoxxo##%"
	),
	("#To.oTx.#To%"
	+"r+d.r^d.r+d%"
	+"o#oTx.oT#oo%"
	+"..r^d.r^d..%"
	+"oTx.x=o.#To%"
	+"r+drT+Tdr+d%"
	+"oxoxxoxo#o#%"
	),
]
[
	("#To.#To.#To%"
	+"r+d.r^d.r+d%"
	+"o#oT#.oT##o%"
	+"..r^d.r^d..%"
	+"oT#.o=x.oTx%"
	+"r+drT+Tdr+d%"
	+"##oo#o#xo#x%"
	),	
	("#To.#To.#To.xTo%"
	+"r^d.r^d.r^d.r^d%"
	+"o.oT#.o.#.oTx.x%"
	+"..r^d.....r^d..%"
	+"oT#.o--T--x.oT#%"
	+"r^d.r-T^T-d.r^d%"
	+"#.o.o.x.o.x.#.o%"
	),
]

if __name__ == '__main__':
	for i in autosomal_dominant:
		print("autosomal_dominant")
		print(autosomal_dominant)
		print("autosomal_dominant")
	for i in autosomal_recessive:
		print("autosomal_recessive")
		print(autosomal_recessive)
		print("autosomal_recessive")
	for i in x_linked_dominant:
		print("x_linked_dominant")
		print(x_linked_dominant)
		print("x_linked_dominant")
	for i in x_linked_recessive:
		print("x_linked_recessive")
		print(x_linked_recessive)
		print("x_linked_recessive")
	for i in y_linked:
		print("y-linked")
		print(y_linked)
		print("y-linked")
