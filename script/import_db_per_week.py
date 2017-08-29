from dep_statistics import DepartmentStatis

Department = DepartmentStatis()
base_static = Department.get_base_static()
Department.insert_dep_weekly_person(base_static)
