set autoscale 
set border 3 
set ylabel 'Word Count'
set xr[0:30]
set xtics border in scale 1,0.5 nomirror rotate by -90 offset character 0, -5, 0
set xlabel 'Words'
unset key
plot "listedData2.txt" using 1:xticlabels(2) with lines
set term postscript
set output 'NSTEMIfrequencies.ps'
replot
set term png
set output 'NSTEMIfrequencies.png'
replot
set term x11
