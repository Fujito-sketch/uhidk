import csv
from pathlib import Path
import os
os.system('cls' if os.name == 'nt' else 'clear')

script_dir = Path(__file__).parent

GradeComp = {"Kehadiran" : 0, "TP" : 0, "TA" : 0, "Praktikum" : 0, "Jurnal" : 0}
FileLines = []

def prog():
    filename = input("\nInput file name to check for anomalies,\nor enter 'exit' to end the program : ")
    skipformat = False

    if filename.upper() == "EXIT":
        print("Process ended.")
        return
    
    TAReport = []
    PracReport = []
    JourReport = []
    
    modulecount : int

    with open(script_dir/filename, mode='r', encoding='utf-8') as file:
        counter : int = 0
        for line in file:
            if "Jurnal2" in line:
                skipformat = True
            if counter < 1:
                counter = counter + 1
                continue
            FileLines.append(line)
            counter = counter + 1

    if not skipformat:
        with open(script_dir/filename, mode='w', encoding='utf-8') as file:
                file.seek(0)
                counter : int = 0
                for line in FileLines:
                    counter += 1
                    if counter > 1:
                        file.write(line)
                    else:
                        headers = line.split(",")
                        for i, header in enumerate(headers):
                            header = header.strip()
                            if header in GradeComp:
                                print(headers[i])
                                GradeComp[header] = GradeComp[header] + 1
                                headers[i] = header + str(GradeComp[header])
                        joinedheaders = ",".join(headers)
                        joinedheaders = joinedheaders + '\n'
                        file.write(joinedheaders)


    try:

        with open(script_dir/filename, mode='r', encoding='utf-8') as file:
            file.seek(0)
            reader = csv.DictReader(file)

            for row in reader:
                stop = False

                AttArray = []
                TAArray = []
                PracArray = []
                JourArray = []

                try:
                    for x in range(10):
                        AttArray.append(row["Kehadiran" + str(x+1)])
                        TAArray.append(row["TA" + str(x+1)])
                        PracArray.append(row["Praktikum" + str(x+1)])
                        JourArray.append(row["Jurnal" + str(x+1)])
                        modulecount = x+1
                except KeyError:
                    pass

                for i in range(len(TAArray)):
                    if not TAArray[i] and row["Kehadiran" + str(i+1)] != "Absen":
                        TAReport.append("Empty Module " + str(i+1) + " TA value detected at " + row["Nim"] + '!')
                        stop = True
                    if not PracArray[i] and row["Kehadiran" + str(i+1)] != "Absen":
                        PracReport.append("Empty Module " + str(i+1) + " Prac value detected at " + row["Nim"] + '!')
                        stop = True
                    if not JourArray[i] and row["Kehadiran" + str(i+1)] != "Absen":
                        JourReport.append("Empty Module " + str(i+1) + " Jour value detected at " + row["Nim"] + '!')
                        stop = True

                if stop:
                    continue
                for i in range(len(TAArray)):
                    if not check_ta(int(TAArray[i])):
                        TAReport.append("Anomalous Module " + str(i+1) + " TA value detected at " + row["Nim"] + '!')
                        TAReport.append("The Anomalous value in question : " + TAArray[i])
                    if not is_valid_4_value_average(float(PracArray[i]), AttArray[i]):
                        PracReport.append("Anomalous Module " + str(i+1) + " Prac value detected at " + row["Nim"] + '!')
                        PracReport.append("The Anomalous value in question : " + PracArray[i])

                    if not is_final_grade_valid(float(JourArray[i])):
                        JourReport.append("Anomalous Module " + str(i+1) + " Jour value detected at " + row["Nim"] + '!')
                        JourReport.append("The Anomalous value in question : " + JourArray[i])
    except FileNotFoundError:
        print("\nFile not found\nMake sure the file is in the same directory\nas the program and try again.\n")
        prog()
        return

    if not TAReport and not PracReport and not JourArray:
        print("No anomaly detected\n")
        return

    print("\n////Displaying data from", modulecount, "Modules ////\n")

    if not TAReport:
        print("\nNo anomalous TA value detected\n")
    else:
        print("///////////// TA REPORT /////////////")
        for message in TAReport:
            print(message)
        print("///////////// TA REPORT /////////////\n\n")

    if not PracReport:
        print("No anomalous Prac value detected\n")
    else:
        print("//////////// PRAC REPORT ////////////")
        for message in PracReport:
            print(message)
        print("//////////// PRAC REPORT ////////////\n\n")

    if not JourReport:
        print("No anomalous Jour value detected\n")
    else:
        print("//////////// JOUR REPORT ////////////")
        for message in JourReport:
            print(message)
        print("//////////// JOUR REPORT ////////////\n\n")
    
    return 0

VALID_SUMS_OF_4 = {
    180, 200, 215, 220, 230, 235, 240, 250, 255, 260, 265, 270,
    275, 280, 285, 290, 300, 305, 315, 320, 330, 335, 350, 365, 380
}

def is_valid_4_value_average(avg: float, att: str) -> bool:
    if avg == 0 and att == "Absen":
        return True

    if avg < 45.0 or avg > 95.0:
        return False
        
    candidate_sum = avg * 4
    if not candidate_sum.is_integer():
        return False
        
    return int(candidate_sum) in VALID_SUMS_OF_4

VALID_B_VALUES = [0, 45, 65, 80, 95]

def is_final_grade_valid(final_grade: float) -> bool:
    if final_grade < 0 or final_grade > 97.5:
        return False
    
    double_f = final_grade * 2
    if not double_f.is_integer():
        return False
    
    double_f = int(double_f)
    
    if double_f % 10 not in (0, 5):
        return False
    
    for b in VALID_B_VALUES:
        a = double_f - b
        if 0 <= a <= 100 and a % 10 == 0:
            return True
            
    return False

def check_ta(ta: int = 55) -> bool:
    if ta < 0 or ta > 100:
        return False

    if ta % 10 != 0:
        return False

    return True

prog()