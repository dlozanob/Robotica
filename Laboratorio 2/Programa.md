
```SPEL+
Global Integer Out_11, Out_12, altura

Function main
	Motor On
	Power High

	Speed 40
	Accel 40, 40

	Out_11 = 11; Out_12 = 12
	altura = 587 + 100
	
	Home

    Do
		Call paletizado_z
		Call paletizado_s
		Call paletizado_externo
	Loop
	
Fend
Function paletizado_z
	#define estado_paletizado_z 11
	Pallet 1, Origen, Ejey, Ejex, 3, 3
	On estado_paletizado_z
	Integer i
	For i = 1 To 9
		Go Pallet(1, i) :Z(altura)
		Go Pallet(1, i)
		Go Pallet(1, i) :Z(altura)
	Next
	i = 0
	Off estado_paletizado_z
Fend
Function paletizado_s
	#define estado_paletizado_s 11
	Pallet 2, Origen, Ejey, Ejex, 3, 3
	On estado_paletizado_s
	Integer i
	Integer k
	k = 0
	
	For i = 1 To 9
		If i = 4 Then
			k = i + 2
		ElseIf i = 6 Then
			k = i - 2
		Else
			k = i
		EndIf
		
		Go Pallet(1, k) :Z(altura)
		Go Pallet(1, k)
		Go Pallet(1, k) :Z(altura)
	Next
	i = 0
	Off estado_paletizado_z
Fend
Function paletizado_externo
	Integer i, j
	Pallet Outside, 3, Origen, Ejey, Ejex, 3, 3
	
	For i = 1 To 4
		For j = 1 To 4
			Go Pallet(3, i, j) :Z(altura)
			Go Pallet(3, i, j)
			Go Pallet(3, i, j) :Z(altura)
		Next
	Next
	
	i = 0
	j = 0
Fend
```

