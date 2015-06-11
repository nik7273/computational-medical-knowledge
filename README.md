# furry-avenger 
### Comparing representation of medical knowledge across different media

This respository contains Python and BASH code to:

1. acquire data on myocardial infarcation from social media and online medical textbooks
2. analyze how the description of myocardial infarction differs among those media


###Quickstart

```
   git clone https://github.com/mac389/furry-avenger.git
   cd furry-avenger
   chmod +x ./main.sh
   ./main.sh
```
   To acquire data
```
    sh acquire_data.sh
```

   To analyze data
```
     sh analyze_data.sh
```

   To generate all figures from Devraj and Chary (2015)
```
     sh make_figures.sh
```

   To generate the _i_ th figure from Devraj and Chary (2015)
```
     sh make_figure.sh i 
```