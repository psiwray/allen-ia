# Allen's Interval Algebra (Python edition)

Interval algebra is used to describe relationships between time intervals over
a time axis. Constraints are placed between each time interval so that when
boolean expressions are constructed, they can be validated with the help of a SAT
solver.

There are three main input data structures and some algorithms that allow for
the generation of the boolean clauses that describe the constraints between all
the time intervals, and they'll be described in the two following sections.

## Input data structures

All the classes and methods can be found inside the `allen/input` module, so
every reference to Python files will be relative to that.

Since the file format of the input files is briefly described with EBNF, I'll
introduce some basic BNF that can be used to understand the rest of the
specifications (I'm using the format as specified in [here](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form)):

```
ws := ? any ws character ?;
nl := ? newline character ?;
relationship :=
    "<" | ">" | "m" | "mi" | "o" | "oi" | "s" |
    "si" | "d" | "di" | "f" | "fi" | "=";
relationships_list := "(", ws, {relationship, ws}, ")";
```

### Inverse relationships table

The first data structure is the **inverse relationships table**, in particular
found in this repository under `data/inverse_relationships_table.txt`. It's
quite small and its only purpose is to describe, given a specific relationship
between two time intervals *t1* and *t2*, what would the relationship be if the
time intervals were actually the opposite, that is, it specifies the
relationship that would be present between *t2* and *t1*. The order in which we
define the relationships between two or more time intervals matters, since the
time axis is where the intervals reside. The table has a simple structure and is
defined by a number of rows (in particular 13 rows since all the possible
relationship types are actually 13) where each row contains first the normal
relationship (that we defined before as being from *t1* to *t2*), a double
colon and the inverse relationship (that we defined before as being, this time,
from *t2* to *t1*).

The function `read_inverse_relationships_table()` inside `inverse_relationships_table.py`
module provides a quick way to load all the data inside a practical data
structure defined by the `InverseRelationshipsTable` class. This class exactly
mirrors the contents of the file with a list-based data structure where each
item is a tuple.

Each line can briefly be described using BNF as:

```
line := relationship, ws, "::", ws, relationship, nl;
```

### Ternary constraints table

The second data structure is the **ternary constraints table**. Let's say that
we take into account the existence of three time intervals, called *t1*, *t2* 
and *t3*. We also specify that the relationship between *t1* and *t2* is
*r_t1t2* and that the relationship between *t2* and *t3* is *r_t2t3*, then,
because of Allen's interval algebra, only a few select relationships
between *t1* and *t3* will actually make sense, from the whole set. This table thus
defines, for a given pair of relationships *r_t1t2* and *r_t2t3*, what's the set
of possible relationships that can be found between *t1* and *t3* and we could
call that *r_t1t3*.

As with the previous structure, the function `read_ternary_constraints_table()`
inside `ternary_constraints_table.py` quickly reads the table from the given
file path and, as before, returns a data structure that exactly mirrors the 
contents of the file. In particular, the `TernaryConstraintsTable` is the class
instance that is returned by the function. The table contains a series of lines
where each line is composed by the first two relationships *r_t1t2* and *r_t2t3*
separated by a single colon and then a double colon precedes a list enclosed by
round brackets of all the possible *r_t1t3* relationships. This table can be 
found under this repository in the `data/ternary_constraints_table.txt` file.

Each line can briefly be described using BNF as:

```
line := relationship, ws, ":", ws, relationship, ws, "::", ws, relationships_list, nl;
```

### Time intervals groups

The third and last data structure is the list of **time intervals groups**. For each
input file in question, many groups can be contained inside it. A single group
is defined as being a list of relationships between a well known number of time
intervals, where each pair of time intervals might be related by one or multiple
relationships. An example of time intervals groups can be found inside the
`data/time_intervals` folder, with various kinds of data sizes.

The function `read_time_intervals_table()` reads all the time intervals groups
inside the input file and returns a list of `TimeIntervalsGroup` instances
where each one of them represents the exact data provided by the group. As
usual, the file is line-based but the groups have a header that indicates the
number of time intervals, followed by some lines that define the relationships
between two time intervals (each time interval is referenced by a number from zero
up to one less than the total number of time intervals written in the header)
and a final line containing a dot that marks the end of the current group.

Each group can briefly be described with BNF as:

```
intervals_count := ? any positive integer number ?;
time_interval := ? any non-negative integer number less than the intervals count ?;

header := intervals_count, nl;
line := time_interval, ws, time_interval, ws, "::", relationships_list, nl;
end := ".", nl;
group := header, {line}, end;
```

## Clause generators

Given the input data, some algorithms are used to generate boolean clauses whose
satisfiability will be later checked by a SAT solver. In particular, we're
always using:

+ at least one,
+ at most one,
+ inverse implication

and the user gets to choose between:

+ ternary implication, or
+ expression reference.

All the above algorithms will now be explained in the following sections. Before
that, a brief explanation on what a **boolean clause** is. Generally, in the
context of boolean SAT solvers, the input data is a list of clauses. Each clause
is essentially a boolean expression composed by subsequent OR operators on individual
literals, where each literal can be plain or negated. Thus, a single boolean
clause can be for example `x1 x2 -x3` whose actual meaning is `x1 OR x2 OR (NOT x3)`.
In our case, each literal can either represent a relationship between two time
intervals (thus described by a triple: *t1*, *t2*, and *r_t1t2*) or it can be
referring to an expression 

I will also refer to the **configuration**, indicating the current time
intervals group taken into account and whose algorithms are being applied on.

### At least one

Considering the fact that most of the time, in the time intervals group, for
each set of relationships that can be found between a generic *t1* and *t2*, the
size of said set is bigger than one (in other words, it specifies that there can be more than
one relationship between *t1* and *t2*), we want to generate a
clause that expresses the fact that **at least one** of those relationships has
to be found in the given configuration. We express that constraint by ORing
together all the literals into a single clause, where for each clause we work
with time intervals *t1* and *t2* and we compose literals by using, in turn, every
relationship that's possible between *t1* and *t2*.

To give an example, let's say that between time intervals 3 and 4 there can only
be relationships before (`<`), equal (`=`) or overlapping (`o`).
We then generate the **at least one** clause by using three literals, one for
each relationship and all of them using the same pair of time intervals. In the
following code block, the resulting clause is explained:

```
Line describing the relationships in the time intervals group:
    3 4 :: ( < = o )
    
Literals as defined by what's required by the algorithm:
    l1: relationship < between time intervals 3 and 4
    l2: relationship = between time intervals 3 and 4
    l3: relationship o between time intervals 3 and 4
    
Resulting clauses:
    l1 OR l2 OR l3
```

It's pretty clear that for the clause to be true, it's enough to have
one of those literals to be true, that is, to have one of the three possible
relationships to actually be the one specified in the given configuration.

### At most one

This algorithm is pretty similar to the at least one counterpart, but instead
specifies the exact opposite: between two time intervals that can be related by
more than one possible relationship, generate a clause that makes sure at most
one of those relationships is the one given in the configuration and not more.

To do this, we construct not one but a series of clauses each indicating that
it's not possible for two relationships to be specified in the configuration at
the same time. Let's say that we have two time intervals 3 and 4, as before and
that the relationships between them are before (`<`), equal (`=`) or overlapping
(`o`). We know that it's not possible for the configuration to have both
3 and 4 related by relationships before and equal, or by before and overlapping or again by
equal and overlapping. We construct a boolean expression that's an AND of two
negated literals, each one indicating that between 3 and 4 there's a different
relationship. We do that with all the possible combinations of relationships.

Since the resulting clauses aren't in the format required by the SAT solver
that needs all literals ORed together to form a single clause, we need to take
advantage of the properties of boolean algebra and use De Morgan's theorem to
swap the AND of the two negated literals with the same two non-negated literals
ORed together. The code block provides an example:

```
Generic boolean expression:
    !x_{t1, t2, r1} & !x_{t1, t2, r2}

Line describing the relationships in the time intervals group:
    3 4 :: ( < = o )
    
Literals as defined by what's required by the algorithm:
    l1: relationship < between time intervals 3 and 4
    l2: relationship = between time intervals 3 and 4
    l3: relationship o between time intervals 3 and 4
    
Resulting clauses:
    -l1 OR -l2
    -l1 OR -l3
    -l2 OR -l3
```

### Inverse implication

This is quite simpler than the rest of the algorithms as it expresses the fact
that, given time intervals *t1* and *t2*, if the relationship between them is
something, then it should also be true that if we swap the order of the time
intervals, the relationship between them should be the exact inverse of the
previous relationship. Here too we take advantage of the propositional logic's
rules to change an implication into a valid boolean expression that can be used
in a SAT solver.

```
Generic boolean expression:
    x_{t1, t2, r} => x_{t2, t1, inverse_of(r)} which is
    !x_{t1, t2, r} | x_{t2, t1, inverse_of(r)}

Line describing the relationships in the time intervals group:
    3 4 :: ( < = o )
    
Literals as defined by what's required by the algorithm:
    l1: relationship < between time intervals 3 and 4
    l2: relationship > between time intervals 4 and 3 (the inverse of 3 and 4)
    
Resulting clauses:
    -l1 OR l2
```

### Ternary implication

This is one of the two algorithms that can be used to complete the list of
clauses to be passed to the SAT solver. It puts into practice (actually, boolean
expressions) what has been described in the section that describes the data
structure. The below code block represents an example:

```
Generic boolean expression:
    x_{t1, t2, r1} & x_{t2, t3, r2} => x_{t1, t3, r3} which is
    !(x_{t1, t2, r1} & x_{t2, t3, r2}) | x_{t1, t3, r3} which is
    !x_{t1, t2, r1} | !x_{t2, t3, r2} | x_{t1, t3, r3}

Lines describing the relationships in the time intervals group:
    3 4 :: ( > )
    4 5 :: ( s fi )
    
Lines needed in the ternary constraints table:
    > : s :: ( > d f mi oi )
    > : fi :: ( > )
    
Literals as defined by what's required by the algorithm:
    l1: relationship > between time intervals 3 and 4
    l2: relationship s between time intervals 4 and 5
    l3: relationship fi between time intervals 4 and 5
    
    l4: relationship > between time intervals 3 and 5
    l5: relationship d between time intervals 3 and 5
    l6: relationship f between time intervals 3 and 5
    l7: relationship mi between time intervals 3 and 5
    l8: relationship oi between time intervals 3 and 5
    
    l9: relationship > between time intervals 3 and 5
    
Resulting clauses:
    -l1 OR -l2 OR l4 OR l5 OR l6 OR l7 OR l8
    -l1 OR -l3 OR l9
```

### Expression reference

To be done.

## Output data structures

Once all the required clauses have been generated, the `allen/output` module
will take care of everything that's required to generate proper SAT input.
Essentially, each literal for every clause will be identified by a single 
positive integer number thus the `number_dict.py` provides facilities to uniquely
identify literals across clauses.

When two literals are found in two different clauses,
the same integer number is used. Each clause is written by separating each
contained literal with a space, eventually negating the integer number that
represents the literal if it's negated and adding a zero at the end of the line
to mark the end of the clause. Subsequent clauses are written in a separate 
line.
