import os
import csv
import codecs
import unicodedata
import shutil
import distutils.dir_util

run_loop = True
dat_dir = ''
dat_dir_stat = []
found_keys = []
cwd = os.getcwd() + '\\'
var_0 = ''
sz_total_0 = 0


def create_datdir():
    global dat_dir
    subdirs = [x[0] for x in os.walk('.')]
    for _ in subdirs:
        if _.startswith('.\\data_'):
            var = _.replace('.\\data_', '')
            if var.isdigit():
                var_int = int(var)
                dat_dir_stat.append(var_int)
    if len(dat_dir_stat) > 0:
        data_int = int(max(dat_dir_stat) + 1)
        var_str = 'data_'+str(data_int)
        print(112 * '-')
        print('creating extra data directory:', var_str)
        print(112 * '-')
        distutils.dir_util.mkpath(var_str)
        dat_dir = var_str
    elif len(dat_dir_stat) == 0:
        print(112 * '-')
        print('creating initial data directory:', 'data_0')
        print(112 * '-')
        distutils.dir_util.mkpath('.\\data_0')
        dat_dir = '.\\data_0'


def NFD(text):
    return unicodedata.normalize('NFD', text)


def canonical_caseless(text):
    return NFD(NFD(text).casefold())


def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def prnt_title():
    print("\n", 50 * "-", "[HARVEST]", 50 * "-", "\n")


def main():
    global found_keys, var_0, sz_total_0
    clear_console()
    prnt_title()
    var_0 = input('Enter Path: ')
    var_1 = input('Enter Key: ')
    clear_console()
    prnt_title()
    print('\nPATH:   ', var_0)
    print('KEYWORD:', var_1)
    print('\n1. Scan Keyword In Paths')
    print('2. Scan Keyword In File Contents')
    print('3. Scan Keyword In Paths & File Contents')
    print(112 * '-')
    var_2 = input('Select: ')
    mode_bool = [False, False, False]
    clear_console()
    prnt_title()
    if var_2 == '1':
        print('\n[Scan Keyword In Paths]')
        mode_bool= [True, False]
    elif var_2 == '2':
        print('\n[Scan Keyword In File Contents]')
        mode_bool = [False, True]
    elif var_2 == '3':
        print('\n[Scan Keyword In Paths & File Contents]')
        mode_bool = [True, True]
    if os.path.exists(var_0):
        print(112 * '-')
        print('\nPATH:', var_0)
        print('KEYWORD:', var_1)
        print('\n-- scanning -->')
        print(112 * '-')
        st = 0
        for dirName, subdirList, fileList in os.walk(var_0):
            for fname in fileList:
                fullpath = os.path.join(dirName, fname)
                st = st + os.path.getsize(fullpath)
        st = convert_bytes(st)
        s = 0
        i = 0
        for dirName, subdirList, fileList in os.walk(var_0):
            for fname in fileList:
                fullpath = os.path.join(dirName, fname)
                s = s + os.path.getsize(fullpath)
                print('analyzing:', convert_bytes(s), '/', st, fullpath)

                if mode_bool[0] is True:
                    if canonical_caseless(var_1) in canonical_caseless(fullpath):
                        found_keys.append(fullpath)

                if mode_bool[1] is True:
                    try:
                        with codecs.open(fullpath, 'r', encoding="utf-8", errors='ignore') as fo:
                            for line in fo:
                                if canonical_caseless(var_1) in canonical_caseless(line):
                                    found_keys.append(fullpath)
                                    i += 1
                                    break
                    except Exception as e:
                        print(112 * '-')
                        print(e)
                        print(112 * '-')
                print(112 * '-')

        if len(found_keys) > 0:
            clear_console()
            prnt_title()
            print('[SCAN CRITERIA]:')
            print(112 * '-')
            print('PATH:', var_0)
            print('KEYWORD:', var_1)
            print(112 * '-')
            print('\n\n[RESULTS]:')
            sz_total_1 = float()
            for _ in found_keys:
                print(112 * '-')
                print('Key Found:', _)
                sz = convert_bytes(os.path.getsize(_))
                sz_total_1 = os.path.getsize(_) + sz_total_1
                print('Size:', sz)
                print('Selection number:', i)
            print(112 * '-')
            print('Total Scanned:             ', st)
            print('Total Files Containing Key:', len(found_keys))
            print('Total Size of Files Containing Key:', convert_bytes(sz_total_1))
            print(112 * '-')
            harvest()
        elif len(found_keys) == 0:
            print('-- key not found.')


def harvest():
    global run_loop
    print('\n\n[HARVEST OPTIONS]:')
    print(112 * '-')
    print('1. Copy All')
    print('2. Copy Using Selection Number')
    print('3. Compile Index')
    print('\nQ. Quit')
    print(112 * '-')
    var_2 = input('Select: ')
    if var_2 == 'q' or var_2 == 'Q':
        run_loop = False
    elif var_2 == '1':
        create_datdir()
        for _ in found_keys:
            idx = _.find('\\')
            p = cwd + dat_dir + _[idx:]
            try:
                print(112 * '-')
                print('copying:', _, '  --->', p)
                shutil.copyfile(_, p)
                print(112 * '-')
            except Exception as e:
                try:
                    print(112 * '-')
                    print('retrying:', _, '  --->', p)
                    os.makedirs(os.path.dirname(p))
                    shutil.copyfile(_, p)
                    print(112 * '-')
                except Exception as e:
                    print(112 * '-')
                    print('unable to copy file:', e)
                    print(112 * '-')

    elif var_2 == '2':
        var_3 = input('Enter Selection Number: ')
        if var_3.isdigit():
            create_datdir()
            var_3_int = int(var_3)
            idx = found_keys[var_3_int].find('\\')
            p = str(found_keys[var_3_int])
            p = cwd + dat_dir + p[idx:]
            try:
                print(112 * '-')
                print('copying:', found_keys[var_3_int], '  --->', p)
                shutil.copyfile(found_keys[var_3_int], p)
                print(112 * '-')
            except Exception as e:
                try:
                    print(112 * '-')
                    print('retrying:', found_keys[var_3_int], '  --->', p)
                    os.makedirs(os.path.dirname(p))
                    shutil.copyfile(found_keys[var_3_int], p)
                    print(112 * '-')
                except Exception as e:
                    print(112 * '-')
                    print('unable to copy file:', e)
                    print(112 * '-')
        else:
            harvest()

    elif var_2 == '3':
        create_datdir()
        p = cwd + dat_dir + '\\index.csv'
        open(p, 'w').close()
        for _ in found_keys:
            print(112 * '-')
            print('writing key:', _, ' --->', p)
            with codecs.open(p, 'a', encoding="utf-8", errors='ignore') as fo:
                fo.writelines(_)
            print(112 * '-')
        fo.close()

    input('\nPress Any Key To Continue.')


while run_loop is True:
    main()
