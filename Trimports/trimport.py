import re
from Trimports import utils


class Trimport:
    def __init__(self, file_path):
        self.file_path = file_path
        self.module_dict = dict()
        self.duplicate_imports_line_num = []
        self.import_lines_num = set()
        self.dir_mod = dict()
        self.dir_line = dict()
        print(f"[INFO] File Path: {self.file_path}")

    def _get_file_lines(self):
        return utils.get_file_lines(self.file_path)

    def push_element(self, module_, index, to_remove_str, from_dir=False):
        if module_ in self.module_dict:
            lineArr = self.module_dict[module_][1]
            if index + 1 in lineArr:
                return
            self.duplicate_imports_line_num.append(index + 1)
            self.module_dict[module_] = [False, +[index + 1], to_remove_str, from_dir]
        else:
            self.module_dict[module_] = [False, [index + 1], to_remove_str, from_dir]
            self.import_lines_num.add(index + 1)

    def _get_modules(self, lines):
        pattern = r"import .+"
        for index, line in enumerate(lines):
            to_remove_str = None
            modules = re.findall(pattern, line)
            if len(modules) > 0:
                modules = modules[0].replace("import", "")
                module_list = modules.split(",")
                if len(module_list) == 1:
                    to_remove_str = line
                for ind in range(len(module_list)):
                    module = module_list[ind]
                    if to_remove_str == None:
                        to_remove_str = module
                    module_ = module.strip()
                    pat = r" +as +(.*)"
                    match = re.search(pat, module_)
                    if match:
                        module_ = match.group(1)
                    if module_ == "*":
                        module_ = (
                            re.search(r"from\s*(.*)\s*import", line).group(1).strip()
                        )
                        module__ = __import__(module_)
                        modules_list = dir(module__)
                        for m in modules_list:
                            self.dir_mod[m] = [index + 1, f"from {module_} import"]
                            to_remove_str = " "
                            self.push_element(m, index, to_remove_str, True)
                    else:
                        self.push_element(module_, index, to_remove_str, False)
                        to_remove_str = (
                            None if to_remove_str == module else to_remove_str
                        )

    def checks(self, module, line):
        check = re.search(r"%s\s*\(" % module, line)
        check1 = re.search(r"\=\s*%s" % module, line)
        check2 = not re.search(r"import .+", line)
        check3 = not re.search(r"%s\s*=" % module, line)
        check4 = re.search(r"%s\s*\." % module, line)
        return check, check1, check2, check3, check4

    def _check_for_modules(self, lines):
        for index, line in enumerate(lines):
            ind = line.find("#")
            ind = len(line) if ind == -1 else ind
            line = line[:ind]
            for module in self.module_dict:
                is_available, line_nums, to_remove_str, var = self.module_dict[module]
                if is_available:
                    continue
                if index + 1 in line_nums:
                    is_available = False
                check, check1, check2, check3, check4 = self.checks(module, line)
                if (check or check1 or check4) and check2 and check3:
                    if is_available is not None:
                        is_available = True
                elif check3 == False and is_available == False:
                    is_available = None
                self.module_dict[module] = [is_available, line_nums, to_remove_str, var]

    def process_import(self, import_arr):
        for ind, import_str in enumerate(import_arr):
            prefix, string1 = import_str.split("import")
            string2 = [s for s in string1.split(",") if s.strip() != ""]
            string3 = (prefix + " import " + ",".join(string2)).strip() + "\n"
            final_string = re.sub(r" +", " ", string3)
            import_arr[ind] = final_string
        return import_arr

    def remove_unused_imports(self, lines):
        remove_lines = {}
        import_lines = []
        for module in self.module_dict:
            is_available, line_nums, to_remove_str, var = self.module_dict[module]
            minL = min(line_nums)
            if is_available and var:
                lineN = self.dir_mod[module][0]
                self.dir_line[lineN] = (
                    self.dir_line.get(lineN, self.dir_mod[module][1] + " ")
                    + module
                    + ", "
                )
            elif not is_available and not var:
                remove_lines[minL] = remove_lines.get(minL, []) + [to_remove_str]
        edited_lines = []
        dir_arr = []
        for index, line in enumerate(lines):
            check1 = index + 1 in self.duplicate_imports_line_num
            if check1:
                continue
            if index + 1 in remove_lines:
                to_remove = remove_lines[index + 1]
                for string in to_remove:
                    line = line.replace(string, " ")
                if re.search(r"import .+", line):
                    if index + 1 in self.import_lines_num:
                        import_lines.append(line.strip(" "))
                    else:
                        edited_lines.append(line.strip(" "))
            else:
                if index + 1 in self.dir_line:
                    dir_arr.append(
                        self.dir_line[index + 1].strip(" ").strip(",") + "\n"
                    )
                elif index + 1 in self.import_lines_num:
                    import_lines.append(line.strip(" "))
                else:
                    edited_lines.append(line.strip(" "))
        import_lines = self.process_import(import_lines)
        return dir_arr + import_lines + edited_lines

    def write_file(self, output_file_lines):
        utils.write_file(self.file_path, output_file_lines)

    def main(self):
        lines = self._get_file_lines()
        self._get_modules(lines)
        self._check_for_modules(lines)
        output_lines = self.remove_unused_imports(lines)
        self.write_file(output_lines)


def run(file_path=None):
    if file_path == None:
        raise Exception("File path not found.")
    s = Trimport(file_path)
    s.main()


if __name__ == "__main__":
    run(file_path="/home/amit/Documents/hello.py")
