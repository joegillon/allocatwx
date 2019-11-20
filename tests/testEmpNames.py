def run_test() :
    import re

    mismatches = 0
    for name in names:
        if not re.match(pattern, name):
            print(name)
            mismatches += 1

    print(len(names), mismatches)


if __name__ == '__main__':
    from models.employee import Employee

    emps = Employee.get_all()
    names = [e['name'] for e in emps]

    pattern = "^[A-Z ,\'\-\(\)]+, ?[A-Z ,\'\-]+ ?[A-Z ,\'\- ]+$"

    run_test()
