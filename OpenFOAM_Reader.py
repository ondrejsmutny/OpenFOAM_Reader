# Tool for monitoring the progress of residues from water level simulation outputs
# Outputs are from open-source simulation tool OpenFOAM
# /*---------------------------------------------------------------------------*\
# | =========                 |                                                 |
# | \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
# |  \\    /   O peration     | Version:  v1906                                 |
# |   \\  /    A nd           | Web:      www.OpenFOAM.com                      |
# |    \\/     M anipulation  |                                                 |
# \*---------------------------------------------------------------------------*/

# Python 3.10.2

# You need to import:
import matplotlib.pyplot as plt
    # Matplotlib 3.5.1
import csv

class CheckResidual:
    # Loads the log in .run formate
    # Finds the time steps in log
    # Finds the last Final residuals for quantities p_rgh, omega and k in time steps
    # Plots the graph
    # Saves processed log in .csv formate
    def __init__(self, log):
        log = open(log, "r")
        lines = log.readlines()
        list_residual = []

        def quantity(list_quantity):
            # Finds last line with Final residual, separates the string with number from it and convert it to float
            return float((list_quantity[-1]).split(", ")[2][17:])

        def axe(list_axe, position):
            # Creates axe from list of lists
            return [i[position] for i in list_axe]

        for line in lines:
            if line.startswith("Time = ") == True:
                # Finds step start
                line_time = lines.index(line)
                time_end = lines[line_time].index("\n")
                time = float(lines[line_time][7:time_end])
            if line.startswith("ExecutionTime = ") == True:
                # Finds step end and do actions for step
                line_executiontime = lines.index(line)
                log = open("log.run", "r")
                lines_step = log.readlines()[line_time:line_executiontime + 1]
                list_p_rgh = []
                list_omega = []
                list_k = []
                for line_step in lines_step:
                    if line_step.startswith("GAMG:") == True:
                        # Finds lines with Final resiudal for p_rgh
                        line_p_rgh = lines_step.index(line_step)
                        list_p_rgh.append(lines_step[line_p_rgh])
                    if line_step.startswith("smoothSolver:  Solving for omega") == True:
                        # Finds lines with Final resiudal for omega
                        line_omega = lines_step.index(line_step)
                        list_omega.append(lines_step[line_omega])
                    if line_step.startswith("smoothSolver:  Solving for k") == True:
                        # Finds lines with Final resiudal for k
                        line_k = lines_step.index(line_step)
                        list_k.append(lines_step[line_k])            
                p_rgh = quantity(list_p_rgh)
                omega = quantity(list_omega)
                k = quantity(list_k)
                list_residual.append([time,p_rgh,omega,k])

        # Plots graph
        axe_time = axe(list_residual, 0)
        axe_p_rgh = axe(list_residual, 1)
        axe_omega = axe(list_residual, 2)
        axe_k = axe(list_residual, 3)
        fig = plt.figure()
        plt.plot(axe_time, axe_p_rgh, label = "p_rgh")
        plt.plot(axe_time, axe_omega, label = "omega")
        plt.plot(axe_time, axe_k, label = "k")
        plt.xlabel("Time (s)")
        plt.legend()
        plt.show()

        # Saves processed log to a csv file
        with open("processed_log.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Time","p_rgh","omega","k"])
            writer.writerows(list_residual)
            file.close()

        log.close()

if __name__ == "__main__":
    CheckResidual(log="log.run")
