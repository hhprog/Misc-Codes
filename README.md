=TRANSPOSE(UNIQUE('Raw Data'!A:A))
=SORT(UNIQUE(FILTER('Raw Data'!C:C, 'Raw Data'!B:B="Y Angle")))
=INDEX('Raw Data'!$D:$D, MATCH(1, ('Raw Data'!$A:$A=B$1)*('Raw Data'!$B:$B="Y Angle")*('Raw Data'!$C:$C=$A2), 0))
=INDEX($A:$A, XMATCH(MAX(IF(ISNUMBER(B:B), B:B))/2, IF(ISNUMBER(B:B), B:B), 1, 1))
=INDEX($A:$A, XMATCH(MAX(IF(ISNUMBER(B:B), B:B))/2, IF(ISNUMBER(B:B), B:B), 1, -1))
=N9-N8
