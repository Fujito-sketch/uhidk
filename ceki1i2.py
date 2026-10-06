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

def prog():
    CheckVal = float(input("Input Nilai Jurnal : "))

    if is_final_grade_valid(CheckVal):
        print("Nilai Aman")
    else:
        print("Nilai Tidak Valid")

    prog()

prog()