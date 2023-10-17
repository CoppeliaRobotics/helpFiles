import os
import sys
import re
import shutil

def main():
    currentDir = os.path.dirname(os.path.abspath(__file__))
    inputFile = currentDir + '/regularApi.txt'
    regApiDir = currentDir + '/en/regularApi'
    try:
        shutil.rmtree(regApiDir)
    except Exception as e:
        pass    
    os.makedirs(regApiDir)
    temp = currentDir + '/templates/regularApi_cpp.htm'
    with open(temp, 'r') as file_r:
        template_cpp = file_r.read()
    temp = currentDir + '/templates/regularApi_pythonLua.htm'
    with open(temp, 'r') as file_r:
        template = file_r.read()
    with open(inputFile, 'r') as file_r:
        all = file_r.read()
        
        pos = 0
        allCpp = {}
        allPythonLua = {}
        while pos!= None:
            apiFunc, pos = getTxt(all, 'apiFunctionName', pos)
            _, posEnd = getTxt(all, 'apiFunctionName', pos)
            if apiFunc:
                apiSynopsisCpp, *_ = getTxt(all, 'apiSynopsisCpp', pos, posEnd)
                apiSynopsisPython, *_ = getTxt(all, 'apiSynopsisPython', pos, posEnd)
                apiSynopsisLua, *_ = getTxt(all, 'apiSynopsisLua', pos, posEnd)
                if apiSynopsisCpp:
                    allCpp[getCppName(apiFunc)] = True
                if apiSynopsisPython or apiSynopsisLua:
                    allPythonLua[getPythonLuaName(apiFunc)] = True
        pos = 0
        cnt = 0
        while pos!= None:
            apiFunc, pos = getTxt(all, 'apiFunctionName', pos)
            _, posEnd = getTxt(all, 'apiFunctionName', pos)
            if apiFunc:
                cnt += 1
                apiDescription, *_ = getTxt(all, 'apiDescription', pos, posEnd)
                apiSeeAlso, *_ = getTxt(all, 'apiSeeAlso', pos, posEnd)
                if apiSeeAlso != None:
                    apiSeeAlsoCpp = prepSeeAlso(apiSeeAlso, allCpp, allPythonLua, 'cpp')
                    apiSeeAlsoPythonLua = prepSeeAlso(apiSeeAlso, allCpp, allPythonLua, 'pythonLua')
                else:
                    apiSeeAlsoCpp = ''
                    apiSeeAlsoPythonLua = ''
                apiSynopsisCpp, *_ = getTxt(all, 'apiSynopsisCpp', pos, posEnd)
                apiInputCpp, *_ = getTxt(all, 'apiInputCpp', pos, posEnd)
                apiOutputCpp, *_ = getTxt(all, 'apiOutputCpp', pos, posEnd)
                apiMoreCpp, *_ = getTxt(all, 'apiMoreCpp', pos, posEnd)
                if apiMoreCpp == None:
                    apiMoreCpp = ''
                apiSynopsisPython, *_ = getTxt(all, 'apiSynopsisPython', pos, posEnd)
                apiSynopsisLua, *_ = getTxt(all, 'apiSynopsisLua', pos, posEnd)
                apiInputPythonLua, *_ = getTxt(all, 'apiInputPythonLua', pos, posEnd)
                apiOutputPythonLua, *_ = getTxt(all, 'apiOutputPythonLua', pos, posEnd)
                apiMorePythonLua, *_ = getTxt(all, 'apiMorePythonLua', pos, posEnd)
                if apiMorePythonLua == None:
                    apiMorePythonLua = ''
                hasPythonLuaVersion = False
                if apiSynopsisPython or apiSynopsisLua:
                    hasPythonLuaVersion = True
                    nm = currentDir + '/en/regularApi/' + getCppName(apiFunc) + '.htm'
                    with open(nm, 'w') as file_w:
                        a = template
                        a = a.replace('__funcName__', apiFunc)
                        a = a.replace('__funcDescription__', apiDescription)
                        a = a.replace('__seeAlso__', apiSeeAlsoPythonLua)
                        a = a.replace('__pythonSynopsis__', addCodeSection(formatSynopsis(apiSynopsisPython, 100), 'python'))
                        a = a.replace('__luaSynopsis__', addCodeSection(formatSynopsis(apiSynopsisLua, 100), 'lua'))
                        if apiInputPythonLua:
                            a = a.replace('__input__', apiInputPythonLua)
                            a = a.replace('__inputVisibility__', '')
                        else:
                            a = a.replace('__inputVisibility__', 'style="display: none;"')
                        if apiOutputPythonLua:
                            a = a.replace('__output__', apiOutputPythonLua)
                            a = a.replace('__outputVisibility__', '')
                        else:
                            a = a.replace('__outputVisibility__', 'style="display: none;"')
                        a = a.replace('__more__', apiMorePythonLua)
                        file_w.write(a)
                if apiSynopsisCpp:
                    nm = currentDir + '/en/regularApi/' + getCppName(apiFunc) + '_cpp' + '.htm'
                    with open(nm, 'w') as file_w:
                        a = template_cpp
                        a = a.replace('__funcName__', getCppName(apiFunc))
                        a = a.replace('__funcDescription__', apiDescription)
                        a = a.replace('__seeAlso__', apiSeeAlsoCpp)
                        a = a.replace('__cppSynopsis__', formatSynopsis(apiSynopsisCpp, 100))
                        if apiInputCpp:
                            a = a.replace('__input__', apiInputCpp)
                            a = a.replace('__inputVisibility__', '')
                        else:
                            a = a.replace('__inputVisibility__', 'style="display: none;"')
                        if apiOutputCpp:
                            a = a.replace('__output__', apiOutputCpp)
                            a = a.replace('__outputVisibility__', '')
                        else:
                            a = a.replace('__outputVisibility__', 'style="display: none;"')
                        a = a.replace('__more__', apiMoreCpp)
                        file_w.write(a)
        print(f'\nTotal generated: {cnt}')

def getTxt(string, item, spos, posEnd = None):
    itemName_s = '==================== ' + item + ' ====================<'
    p1 = string.find(itemName_s, spos)
    if p1 != -1:
        if posEnd == None or p1 < posEnd:
            p1 += len(itemName_s)
            itemName_e = '==================== ' + item + ' ====================>'
            p2 = string.find(itemName_e, p1)
            return string[p1:p2].strip(), p2
    return None, None

def addCodeSection(string, lang):
    s = ''
    if string != None and len(string) > 0:
        s = '<code class="hljs language-' + lang + ' coppelia-coppeliasim-script">' + string + '</code>'
    return s
    
def getCppName(s):
    def repl(match):
        return match.group(1).upper()
    return re.sub(r'\.([a-zA-Z])', repl, s)
    
def getPythonLuaName(s):
    if s.find('.') !=-1 :
        return s
    if not s.startswith('sim') or len(s) < 5:
        return s
    s = s[:3] + '.' + s[3:]
    s = s[:4] + s[4].lower() + s[5:]
    return s
    
def prepSeeAlso(items, allCpp, allPythonLua, lang):
    ret = ''
    lines = items.splitlines()
    bullets = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            if line.startswith('<'):
               bullets.append(line)
            else:
                if lang == 'cpp':
                    if getCppName(line) in allCpp:
                        bullets.append('<a href="' + getCppName(line) + '_cpp.htm">' + getCppName(line) + '</a>')
                    else:
                        if getPythonLuaName(line) in allPythonLua:
                            bullets.append('<a href="' + getCppName(line) + '.htm">' + getPythonLuaName(line) + '</a>')
                        else:
                            print("Error with cpp 'see also' item " + line)
                else: 
                    if getPythonLuaName(line) in allPythonLua:
                        bullets.append('<a href="' + getCppName(line) + '.htm">' + getPythonLuaName(line) + '</a>')
                    #else:
                    #    print("Error with python/lua 'see also' item " + line)
    if len(bullets) > 0:
        ret = '<br>See also:\n<ul>\n'
        for l in bullets:
            ret += '<li>' + l + '</li>\n'
        ret += '</ul>\n'
    return ret
    
def formatSynopsis(s, maxLength):
    if s == None:
        return s
    
    s = s.replace(' = ','##_##')
    s = s.replace('= ','_##')
    s = s.replace(' =','##_')
    s = s.replace('=',' = ')
    s = s.replace('##_##',' = ')
    s = s.replace('##_',' =')
    s = s.replace('_##','= ')
    
    s = s.replace(' , ','_##')
    s = s.replace(', ','_##')
    s = s.replace(' ,','_##')
    s = s.replace(',',', ')
    s = s.replace('_##',', ')
    
    if s.find('<div>') != -1:
        return s
        
    if s.find('\n') != -1:
        return s

    if len(s) <= maxLength:
        return s

    # Function to format the content inside parentheses
    def replacer(match):
        contents = match.group(1).split(',')

        # Determine the amount of padding needed
        indent = match.start() + 1
        indent_str = ' ' * indent

        # Split and join the content based on the maxLength
        line = ''
        formatted_contents = []
        for content in contents:
            if line and len(line + ', ' + content.strip()) + indent > maxLength:
                formatted_contents.append(line)
                line = content.strip()
            elif not line:
                line = content.strip()
            else:
                line += ', ' + content.strip()
        if line:
            formatted_contents.append(line)

        return '(' + ('\n' + indent_str).join(formatted_contents) + ')'

    # Regular expression to match content inside parentheses
    pattern = r'\(([^)]+)\)'

    # Format the content inside parentheses
    formatted_string = re.sub(pattern, replacer, s)

    return formatted_string

if __name__ == "__main__":
    main()




                