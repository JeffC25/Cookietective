# Info
The purpose of the Comparator is to quickly identify if domain names are present in either or both the the Majestic Million and NoTracking lists for easy comparison.

## Functions
#### comparator(*stringsin)
This function is called with a list of domain names and outputs a table indicating if passed domain names are present (1) or not (0) in the Majestic Million and NoTracking lists.

#### Command Line
The comparator() function can also be called in the command line by running comparator.py with domain names as arguments.
For example:
```
python3 comparator.py google.com pokenoms.com youtube.com polandki.pl bmwgroup.com

Output:
        Address  MajesticMillion  NoTracking
0    google.com                1           0
1  pokenoms.com                0           1
2   youtube.com                1           0
3   polandki.pl                0           1
4  bmwgroup.com                1           0
```

