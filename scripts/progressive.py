from csv import reader
from matplotlib import pyplot


def run():
    with open("progressive.csv", "r") as data:
        rows = [line[1:] for line in reader(data, delimiter=",")]
        rows = rows[1:]

        # For every size, calculate the average number of clauses, literals and solve time.
        # Plot the result.
        sizes = [int(row[1]) for row in rows]
        min_size = min(sizes)
        max_size = max(sizes)

        sizes = range(min_size, max_size + 1)
        average_literals_ibsc = {s: [] for s in sizes}
        average_literals_gac = {s: [] for s in sizes}
        average_clauses_ibsc = {s: [] for s in sizes}
        average_clauses_gac = {s: [] for s in sizes}
        average_solve_time_ibsc = {s: [] for s in sizes}
        average_solve_time_gac = {s: [] for s in sizes}

        for row in rows:
            size = int(row[1])

            average_literals_ibsc[size].append(int(row[2]))
            average_literals_gac[size].append(int(row[3]))
            average_clauses_ibsc[size].append(int(row[4]))
            average_clauses_gac[size].append(int(row[5]))
            average_solve_time_ibsc[size].append(float(row[6]))
            average_solve_time_gac[size].append(float(row[7]))

        for size in sizes:
            average_literals_ibsc[size] = sum(average_literals_ibsc[size]) / len(average_literals_ibsc[size])
            average_literals_gac[size] = sum(average_literals_gac[size]) / len(average_literals_gac[size])
            average_clauses_ibsc[size] = sum(average_clauses_ibsc[size]) / len(average_clauses_ibsc[size])
            average_clauses_gac[size] = sum(average_clauses_gac[size]) / len(average_clauses_gac[size])
            average_solve_time_ibsc[size] = sum(average_solve_time_ibsc[size]) / len(average_solve_time_ibsc[size])
            average_solve_time_gac[size] = sum(average_solve_time_gac[size]) / len(average_solve_time_gac[size])

        literals_ibsc = average_literals_ibsc.items()
        literals_gac = average_literals_gac.items()
        clauses_ibsc = average_clauses_ibsc.items()
        clauses_gac = average_clauses_gac.items()
        solve_time_ibsc = average_solve_time_ibsc.items()
        solve_time_gac = average_solve_time_gac.items()

        pyplot.plot([item[0] for item in literals_ibsc], [item[1] for item in literals_ibsc])
        pyplot.xlabel("Numero di intervalli di tempo")
        pyplot.ylabel("Number of literals")
        pyplot.title("Numero di letterali per intervalli di tempo con IBSC")
        pyplot.show()
        pyplot.plot([item[0] for item in clauses_ibsc], [item[1] for item in clauses_ibsc])
        pyplot.xlabel("Numero di intervalli di tempo")
        pyplot.ylabel("Number of clauses")
        pyplot.title("Numero di clausole per intervalli di tempo con IBSC")
        pyplot.show()
        pyplot.plot([item[0] for item in solve_time_ibsc], [item[1] for item in solve_time_ibsc])
        pyplot.xlabel("Numero di intervalli di tempo")
        pyplot.ylabel("Tempo di risoluzione in secondi")
        pyplot.title("Tempo di risoluzione con IBSC")
        pyplot.show()

        pyplot.plot([item[0] for item in literals_gac], [item[1] for item in literals_gac])
        pyplot.xlabel("Numero di intervalli di tempo")
        pyplot.ylabel("Numero di letterali")
        pyplot.title("Numero di letterali per intervalli di tempo con GAC")
        pyplot.show()
        pyplot.plot([item[0] for item in clauses_gac], [item[1] for item in clauses_gac])
        pyplot.xlabel("Numero di intervalli di tempo")
        pyplot.ylabel("Numero di clausole")
        pyplot.title("Numero di clausole per intervalli di tempo con GAC")
        pyplot.show()
        pyplot.plot([item[0] for item in solve_time_gac], [item[1] for item in solve_time_gac])
        pyplot.xlabel("Numero di intervalli di tempo")
        pyplot.ylabel("Tempo di risoluzione in secondi")
        pyplot.title("Tempo di risoluzione con GAC")
        pyplot.show()

        pyplot.plot([item[0] for item in solve_time_ibsc], [item[1] for item in solve_time_ibsc], [item[0] for item in solve_time_gac], [item[1] for item in solve_time_gac])
        pyplot.xlabel("Numero di intervalli di tempo")
        pyplot.ylabel("Tempo di risoluzione in secondi")
        pyplot.title("Tempo di risoluzione con IBSC e GAC")
        pyplot.legend(["IBSC", "GAC"])
        pyplot.show()

        # Graph every combination.
        # pyplot.plot(literals_ibsc, solve_time_ibsc, color="red")
        # pyplot.title("Tempo di risoluzione in base ai letterali per IBSC")
        # pyplot.xlabel("Numero di letterali")
        # pyplot.ylabel("Tempo di risoluzione")
        # pyplot.show()
        #
        # pyplot.plot(clauses_ibsc, solve_time_ibsc, color="green")
        # pyplot.title("Tempo di risoluzione in base alle clausole per IBSC")
        # pyplot.xlabel("Numero di clausole")
        # pyplot.ylabel("Tempo di risoluzione")
        # pyplot.show()
        #
        # pyplot.plot(literals_gac, solve_time_gac, color="blue")
        # pyplot.title("Tempo di risoluzione in base ai letterali per GAC")
        # pyplot.xlabel("Numero di letterali")
        # pyplot.ylabel("Tempo di risoluzione")
        # pyplot.show()
        #
        # pyplot.plot(clauses_gac, solve_time_gac, color="black")
        # pyplot.title("Tempo di risoluzione in base alle clausole per GAC")
        # pyplot.xlabel("Numero di clausole")
        # pyplot.ylabel("Tempo di risoluzione")
        # pyplot.show()


if __name__ == "__main__":
    run()
