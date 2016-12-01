python 3

usuage: python parsefile file

Input is lines of formats:

Lastname, Firstname, (703)-742-0996, Blue, 10013

Firstname Lastname, Red, 11237, 703 955 0373

Firstname, Lastname, 10013, 646 111 0101, Green

"The program should write a valid, formatted JSON object out to result.out. The JSON representation should be indented with two spaces and the keys should be sorted in ascending order. Successfully processed lines should result in a normalized addition to the list associated with the “entries” key. For lines that were unable to be processed, a line number i (where 0 ≤ i < n) for each faulty line should be appended to the list associated with the “errors” key. The “entries” list should be sorted in ascending alphabetical order by (last name, first name)."
